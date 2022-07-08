import json

from src.file_sytem.File_Generator import FileGenerator
from src.package_migration.Folder_Output_Generator import FolderOutputGenerator
from src.package_migration.Package_Migration_Service import PackageMigrationService
from src.package_migration.Package_Process_Factory import PackageProcessFactory
from src.utils.arguments.Package_Creation_Arguments import PackageCreationArguments
from src.utils.arguments.Package_Import_Rollback_Arguments import PackageImportRollbackArguments


class PackageAPI:

    @staticmethod
    def create_package(args):
        try:
            main_config = json.load(
                open("./config/package_creation_config.json"))  # Read configuration for Package Creation script
            package_creation_args = PackageCreationArguments(args)  # plain object which holds the input arguments
            # Initialize folder output and logs
            folder_path, object_list_path = FolderOutputGenerator.generate_creation_folder_output(main_config,
                                                                                                  package_creation_args.source_connection_params)
            try:
                # Create process which creates a package
                binary_path = PackageProcessFactory.create_package_process(package_creation_args, folder_path,
                                                                           object_list_path)
                return "Package Creation finished successfully. Package path: " + binary_path
            except Exception as e:
                raise e
            finally:
                FileGenerator.generate_manifest(folder_path,
                                                args)  # Generate manifest with all the data about the package creation
        except Exception as e:
            raise e

    @staticmethod
    def import_rollback_package(args):
        try:
            main_config = json.load(open(
                "./config/package_import_rollback_config.json"))  # Read configuration for Package Import Rollback script
            package_import_args = PackageImportRollbackArguments(args)  # plain object which holds the input arguments
            # Initialize folder output and logs
            folder_path = FolderOutputGenerator.generate_import_rollback_folder_output(main_config,
                                                                                       package_import_args.import_type,
                                                                                       package_import_args.target_connection_params)
            try:
                # Create process which imports/rollbacks a package
                undo_binary_path = PackageProcessFactory.create_import_rollback_process(package_import_args,
                                                                                        folder_path,
                                                                                        main_config["autoRollback"])
                return "Package" + args["type"] + "finished successfully. Undo Package path: " + undo_binary_path
            except Exception as e:
                raise e
            finally:
                FileGenerator.generate_manifest(folder_path,
                                                args)  # Generate manifest with all the data about the package creation
        except Exception as e:
            raise e

    @staticmethod
    def migrate_package(args):
        try:
            main_config = json.load(
                open("./config/package_migration_config.json"))  # Read configuration for Package Migration script
            package_creation_args = PackageCreationArguments(
                args)  # plain object which holds the input arguments for package creation
            package_import_args = PackageImportRollbackArguments(
                args)  # plain object which holds the input arguments for package import
            # Initialize folder output and logs
            folder_path, object_list_path = FolderOutputGenerator.generate_migration_folder_output(main_config,
                                                                                                   package_creation_args.source_connection_params,
                                                                                                   package_import_args.target_connection_params)
            try:
                # Create process which migrates a package
                binary_path, undo_binary_path = PackageMigrationService(package_creation_args, package_import_args, folder_path).migrate_package(
                    object_list_path, main_config["autoRollback"])
                return "Package Migration finished successfully.\n\tPackage path: " + binary_path + "\n\tUndo Package path: " + undo_binary_path
            except Exception as e:
                raise e
            finally:
                FileGenerator.generate_manifest(folder_path,
                                                args)  # Generate manifest with all the data about the package creation
        except Exception as e:
            raise e
