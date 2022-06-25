import json
import sys
import traceback

from src.file_sytem.File_Generator import FileGenerator
from src.package_migration.Package_Process_Factory import PackageProcessFactory
from src.package_migration.Folder_Output_Generator import FolderOutputGenerator
from src.utils.Configuration import Configuration
from src.utils.arguments.Argument_Reader import ArgumentReader
from src.utils.arguments.Package_Import_Rollback_Arguments import PackageImportRollbackArguments

try:
    main_config = json.load(open("./config/package_import_rollback_config.json"))  # Read configuration for Package Import Rollback script
    args = ArgumentReader(main_config["arguments"]).read_arguments()  # Read script input arguments
    package_import_args = PackageImportRollbackArguments(args)  # plain object which holds the input arguments
    # Initialize folder output and logs
    folder_path = FolderOutputGenerator.generate_import_rollback_folder_output(main_config, package_import_args.import_type, package_import_args.target_connection_params)
    try:
        # Create process which imports/rollbacks a package
        PackageProcessFactory.create_import_rollback_process(package_import_args, folder_path, main_config["autoRollback"])
    except Exception as e:
        raise e
    finally:
        FileGenerator.generate_manifest(folder_path, args) # Generate manifest with all the data about the package creation
except Exception:
    print(traceback.format_exc())
    sys.exit(-1)
sys.exit(0)
