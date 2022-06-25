import json
import sys
import traceback

from src.file_sytem.File_Generator import FileGenerator
from src.package_migration.Folder_Output_Generator import FolderOutputGenerator
from src.package_migration.Package_Migration_Service import PackageMigrationService
from src.utils.Configuration import Configuration
from src.utils.arguments.Argument_Reader import ArgumentReader
from src.utils.arguments.Package_Creation_Arguments import PackageCreationArguments
from src.utils.arguments.Package_Import_Rollback_Arguments import PackageImportRollbackArguments

try:
    main_config = json.load(open("./config/package_migration_config.json"))  # Read configuration for Package Migration script
    args = ArgumentReader(main_config["arguments"]).read_arguments()  # Read script input arguments
    package_creation_args = PackageCreationArguments(args)  # plain object which holds the input arguments for package creation
    package_import_args = PackageImportRollbackArguments(args)  # plain object which holds the input arguments for package import
    # Initialize folder output and logs
    folder_path, object_list_path = FolderOutputGenerator.generate_migration_folder_output(main_config, package_creation_args.source_connection_params, package_import_args.target_connection_params)
    try:
        # Create process which migrates a package
        PackageMigrationService(package_creation_args, package_import_args, folder_path).migrate_package(object_list_path, main_config["autoRollback"])
    except Exception as e:
        raise e
    finally:
        FileGenerator.generate_manifest(folder_path, args)  # Generate manifest with all the data about the package creation
except Exception:
    print(traceback.format_exc())
    sys.exit(-1)
sys.exit(0)
