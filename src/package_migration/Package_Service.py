from datetime import datetime
import time

import inspect

from src.file_sytem.File_Generator import FileGenerator
from src.log_system.Level import Level
from src.log_system.Log import Log
from src.mstr.Mstr_Rest_Service import MstrRestService
from src.utils.Configuration import Configuration


class PackageService:

    def __init__(self, session):
        self.package_id = self.import_id = None
        self.session = session

    # Package creation
    # ___________________________

    # Create a MSTR package that can be used to import objects in other environment
    def create_package_with_action_rule(self, mstr_objects, folder_path, action_rule_config):
        package_content = self.map_to_package_content(mstr_objects, action_rule_config)
        return self.create_package(package_content, folder_path)

    def create_package(self, package_content, folder_path):
        self.package_id = MstrRestService.create_empty_package(self.session)
        MstrRestService.update_package_content(self.session, self.package_id, package_content)
        self.monitor_status()
        binary = MstrRestService.download_binary(self.session, self.package_id)
        return self.save_binary_package(binary, folder_path)

    # Map the objects to package structure.
    # The structure contains a JSON array with details required for each object:
    #   ID, Type, Action and IncludeDependents
    # IncludeDependents is always false because the dependent was already retrieved in previous step
    @staticmethod
    def map_to_package_content(objects, action_rule_config):
        content = []
        for obj in objects:
            content.append({
                "id": obj["id"],
                "type": obj["type"],
                "action": action_rule_config.get_action(obj["type"]),
                "includeDependents": False
            })
        return content

    # ____________________________
    # Package import
    # ____________________________

    # Import a package to the MicroStrategy environment passing the path to the package
    def import_package(self, package_file_path, undo_package_folder_path, auto_rollback):
        self.upload_binary_package(package_file_path)
        return self.create_import_process(undo_package_folder_path, auto_rollback)

    # Rollback a previous import passing the undo package path
    def rollback_package(self, undo_package_file_path, update_schema=True):
        self.upload_binary_package(undo_package_file_path)
        try:
            self.create_import_process()
        except Exception as e:
            raise e
        finally:
            if update_schema:
                MstrRestService.update_schema(self.session)

    # Upload binary file (package) to a metadata package in target environment,
    # so it can be later imported.
    def upload_binary_package(self, package_file_path):
        self.package_id = MstrRestService.create_empty_package(self.session)
        MstrRestService.upload_binary(self.session, self.package_id, package_file_path)
        self.monitor_status()

    # Creates the import process, used for normal import and rollback
    def create_import_process(self, undo_package_folder_path=None, auto_rollback=False):
        method = inspect.currentframe().f_code.co_name
        generate_undo = undo_package_folder_path is not None  # Generate undo if there is path for undo
        undo_package_file_path = None
        try:
            # Create the import process
            self.import_id = MstrRestService.create_import_process(self.session, self.package_id, generate_undo)
            if generate_undo:  # Monitor undo generation if there is undo
                Log.log(Level.INFO, self.__class__.__name__, method,
                        "Monitoring undo package generation",
                        "Undo package generation is being monitored")
                undo_package_file_path = self.monitor_undo_generation(undo_package_folder_path)
            Log.log(Level.INFO, self.__class__.__name__, method,
                    "Monitoring import status",
                    "Import status is being monitoring")
            self.monitor_import_status()  # Monitor import process
            return undo_package_file_path
        except Exception as e:
            # If auto_rollback is enabled and the undo was generated
            if auto_rollback and undo_package_file_path is not None:
                self.finish_process()  # Close import process and delete package
                # Rollback package without updating schema (so it will not be updated twice)
                self.rollback_package(undo_package_file_path, update_schema=False)
            raise e
        finally:
            # Update schema no matter if it went good or bad
            MstrRestService.update_schema(self.session)

    def monitor_undo_generation(self, undo_package_folder_path, start=datetime.now()):
        method = inspect.currentframe().f_code.co_name
        status, undo_created = MstrRestService.check_import_status(self.session, self.import_id)
        self.check_if_import_failed(status, "Error generating the undo package",
                                    "The undo package could not be generated, the import process is canceled.")
        if undo_created:
            Log.log(Level.INFO, self.__class__.__name__, method,
                    "Undo package was generated successfully",
                    "Undo package is ready to be download")
            undo_binary = MstrRestService.download_undo_binary(self.session, self.import_id)
            return self.save_binary_undo_package(undo_binary, undo_package_folder_path)
        else:
            self.check_timeout(start, "Timeout reached in undo package generation",
                               "The timeout (" + str(Configuration.get_property(
                                   "timeout")) + " sec) has been reached during the undo package generation")
            return self.monitor_undo_generation(undo_package_folder_path, start)

    def monitor_import_status(self, start=datetime.now()):
        method = inspect.currentframe().f_code.co_name
        status, undo_created = MstrRestService.check_import_status(self.session, self.import_id)
        PackageService.check_if_import_failed(status, "Import process failed",
                                              "Import failed in the middle of the process, it requires manual rollback to delete already imported objects")
        if status == "imported":
            Log.log(Level.INFO, self.__class__.__name__, method,
                    "Import process finished successfully",
                    "The import process finished successfully and the objects has been migrated")
        else:
            self.check_timeout(start, "Timeout reached in package import process",
                               "The timeout (" + str(Configuration.get_property(
                                   "timeout")) + " sec) has been reached during the import process")
            self.monitor_import_status(start)

    @staticmethod
    def check_if_import_failed(status, message, details):
        method = inspect.currentframe().f_code.co_name
        if status == "failed":
            Log.add_error_log(Level.CRITICAL, MstrRestService.__name__, method, message, details)

    # ________________________________
    # Generic methods
    # ________________________________

    def monitor_status(self, start=datetime.now()):
        method = inspect.currentframe().f_code.co_name
        is_ready = MstrRestService.check_status(self.session, self.package_id)
        if is_ready:
            Log.log(Level.INFO, self.__class__.__name__, method, "Metadata package ready",
                    "The Metadata package has been populated successfully")
            return
        self.check_timeout(start, "Timeout reached in package's object population process",
                           "The timeout (" + str(Configuration.get_property(
                               "timeout")) + " sec) has been reached during the package's object population process")
        self.monitor_status(start)

    @staticmethod
    def check_timeout(start, message, details):
        method = inspect.currentframe().f_code.co_name
        time.sleep(Configuration.get_property("interval"))
        current = datetime.now()
        diff = current - start
        if diff.seconds > Configuration.get_property("timeout"):
            Log.add_error_log(Level.ERROR, PackageService.__name__, method, message, details)

    @staticmethod
    def save_binary_package(binary, folder_path):
        return FileGenerator.save_binary(binary, folder_path, is_undo=False)

    @staticmethod
    def save_binary_undo_package(undo_binary, folder_path):
        return FileGenerator.save_binary(undo_binary, folder_path, is_undo=True)

    def finish_process(self):
        if self.import_id is not None:
            try:
                MstrRestService.close_import_process(self.session, self.import_id)
            except Exception:
                pass
        if self.package_id is not None:
            try:
                MstrRestService.delete_package(self.session, self.package_id)
            except Exception:
                pass
