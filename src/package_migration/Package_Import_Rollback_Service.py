import inspect
import traceback
from datetime import datetime

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.package_migration.Package_Service import PackageService


class PackageImportRollbackService:

    def __init__(self, package_import_args, folder_path):
        self.package_import_args = package_import_args
        self.folder_path = folder_path

    def import_rollback_package(self, session, autoRollback):
        method = inspect.currentframe().f_code.co_name
        start = datetime.now()
        import_type = self.package_import_args.import_type
        Log.log(Level.INFO, self.__class__.__name__, method,
                import_type + " package",
                import_type + " package. Binary path: " + self.package_import_args.package)
        print("Package " + import_type + " in progress...")
        package_service = PackageService(session)
        success_message = "Package " + import_type + " finished successfully."
        error_message = "Package " + import_type + " finished with errors."
        try:
            if import_type == "Import":  # Perform Import process
                # Import package, obtaining path to undo package
                undo_binary_path = package_service.import_package(self.package_import_args.package, self.folder_path, autoRollback)
                end = datetime.now()
                finish_message = " Finished in " + str(end - start) + "."
                if undo_binary_path is None:  # Import process failed
                    raise Exception(error_message + finish_message)
                binary_message = " Undo binary path: " + undo_binary_path
                message = success_message + finish_message + binary_message
                print(message)
                Log.log(Level.INFO, self.__class__.__name__, method,
                        "Package Import finished", message)
                return undo_binary_path
            else:  # Perform Rollback process
                package_service.rollback_package(self.package_import_args.package, update_schema=True)
                end = datetime.now()
                message = "Package Rollback finished successfully. Finished in " + str(end - start)
                Log.log(Level.INFO, self.__class__.__name__, method,
                        "Package Rollback finished",
                        message)
                print(message)
        except Exception as e:
            Log.add_error_log(Level.ERROR, self.__class__.__name__, method, "Package Import/Rollback failed", traceback.format_exc())
            raise e
        finally:
            package_service.finish_process()  # Close import process and delete package.
