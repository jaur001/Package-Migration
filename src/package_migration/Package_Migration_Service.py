import inspect
import traceback
from datetime import datetime

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.mstr.Session_Manager import SessionManager
from src.package_migration.Package_Creation_Service import PackageCreationService
from src.package_migration.Package_Import_Rollback_Service import PackageImportRollbackService


class PackageMigrationService:

    def __init__(self, package_creation_args, package_import_args, folder_path):
        self.package_creation_args = package_creation_args
        self.package_import_args = package_import_args
        self.folder_path = folder_path

    def migrate_package(self, object_list_path, autoRollback):
        method = inspect.currentframe().f_code.co_name
        start = datetime.now()
        Log.log(Level.INFO, self.__class__.__name__, method,
                "Migrating package",
                "Package is being migrated")
        print("Package Migration started.")
        source_session = target_session = None
        try:
            source_session = SessionManager.login(
                self.package_creation_args.source_connection_params)  # Login in source environment
            binary_path = PackageCreationService(self.package_creation_args, self.folder_path).create_package(
                source_session, object_list_path)  # Create package in source environment
            if binary_path is not None:
                self.package_import_args.package = binary_path  # Add path to binary file to package import arguments
                target_session = SessionManager.login(
                    self.package_import_args.target_connection_params)  # Login in target environment
                # Import package created
                undo_binary_path = PackageImportRollbackService(self.package_import_args, self.folder_path).import_rollback_package(
                    target_session, autoRollback)
                end = datetime.now()
                message = "Package Migration finished successfully. Finished in " + str(end - start)
                Log.log(Level.INFO, self.__class__.__name__, method,
                        "Package migrated",
                        message)
                print(message)
                return binary_path, undo_binary_path
        except Exception as e:
            Log.add_error_log(Level.ERROR, self.__class__.__name__, method, "Package Migration failed",
                              traceback.format_exc())
            raise e
        finally:  # Close session in both source and target environments
            if source_session is not None:
                SessionManager.logout(source_session)
            if target_session is not None:
                SessionManager.logout(target_session)
