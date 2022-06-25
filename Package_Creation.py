import json
import sys
import traceback

from src.file_sytem.File_Generator import FileGenerator
from src.package_migration.Folder_Output_Generator import FolderOutputGenerator
from src.package_migration.Package_Process_Factory import PackageProcessFactory
from src.utils.arguments.Argument_Reader import ArgumentReader
from src.utils.arguments.Package_Creation_Arguments import PackageCreationArguments

try:
    main_config = json.load(open("./config/package_creation_config.json"))  # Read configuration for Package Creation script
    args = ArgumentReader(main_config["arguments"]).read_arguments()  # Read script input arguments
    package_creation_args = PackageCreationArguments(args)  # plain object which holds the input arguments
    # Initialize folder output and logs
    folder_path, object_list_path = FolderOutputGenerator.generate_creation_folder_output(main_config, package_creation_args.source_connection_params)
    try:
        # Create process which creates a package
        PackageProcessFactory.create_package_process(package_creation_args, folder_path, object_list_path)
    except Exception as e:
        raise e
    finally:
        FileGenerator.generate_manifest(folder_path, args)  # Generate manifest with all the data about the package creation
except Exception:
    print(traceback.format_exc())
    sys.exit(-1)
sys.exit(0)
