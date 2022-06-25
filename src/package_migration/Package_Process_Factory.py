import inspect
import traceback

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.mstr.Session_Manager import SessionManager
from src.package_migration.Package_Migration_Service import PackageMigrationService
from src.package_migration.Package_Creation_Service import PackageCreationService
from src.package_migration.Package_Import_Rollback_Service import PackageImportRollbackService


class PackageProcessFactory:

    # Create a process which creates a MSTR package
    @staticmethod
    def create_package_process(package_creation_args, folder_path, object_list_path):
        Log.log(Level.INFO, PackageProcessFactory.__name__, inspect.currentframe().f_code.co_name,
                "Package creation process started",
                "Package creation process has started")
        session = None
        try:
            session = SessionManager.login(
                package_creation_args.source_connection_params)  # Login in source environment
            # Consumes Service to create the package
            PackageCreationService(package_creation_args, folder_path).create_package(session, object_list_path)
            Log.log(Level.INFO, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name,
                    "Package creation process finished",
                    "Package creation process has finished, the package was successfully created")
        except Exception as e:
            Log.log(Level.ERROR, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name,
                    "Error during package creation", traceback.format_exc())
            raise Exception("Package creation finished with errors", e)
        finally:
            if session is not None:
                SessionManager.logout(session)  # Logout from MicroStrategy Library

    # Create a process which imports/rollbacks a MSTR package
    @staticmethod
    def create_import_rollback_process(package_import_args, folder_path, autoRollback):
        import_type = package_import_args.import_type
        Log.log(Level.INFO, PackageProcessFactory.__name__, inspect.currentframe().f_code.co_name,
                "Package " + import_type + " process started",
                "Package " + import_type + " process has started")
        session = None
        try:
            session = SessionManager.login(package_import_args.target_connection_params)  # Login in target environment
            # Consumes Service to import/rollback the package
            PackageImportRollbackService(package_import_args, folder_path).import_rollback_package(session,
                                                                                                   autoRollback)
            Log.log(Level.INFO, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name,
                    "Package " + import_type + " process finished",
                    "Package " + import_type + " process has finished")
        except Exception as e:
            Log.log(Level.ERROR, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name, "Error during package " + import_type,
                    traceback.format_exc())
            raise Exception("Package " + import_type + " finished with errors.", e)
        finally:
            if session is not None:
                SessionManager.logout(session)  # Logout from MicroStrategy Library

    # Create a process which migrates a MSTR package
    @staticmethod
    def create_migration_process(package_creation_args, package_import_args, folder_path, object_list_path,
                                 autoRollback):
        Log.log(Level.INFO, PackageProcessFactory.__name__, inspect.currentframe().f_code.co_name,
                "Package migration process started",
                "Package migration process has started, proceeding with package creation")
        try:
            # Consumes Service to migrate the package
            PackageMigrationService(package_creation_args, package_import_args, folder_path).migrate_package(
                object_list_path, autoRollback)
            Log.log(Level.INFO, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name,
                    "Package migration process finished",
                    "Package migration process finished, the package was successfully migrated")
        except Exception as e:
            Log.log(Level.ERROR, PackageProcessFactory.__name__,
                    inspect.currentframe().f_code.co_name,
                    "Error during package migration", traceback.format_exc())
            raise Exception("Package migration finished with errors.", e)
