from src.log_system.Log import Log
from src.file_sytem.Folder_Generator import FolderGenerator


class FolderOutputGenerator:

    # Generate output folder and configure logs for package creation processes
    @staticmethod
    def generate_creation_folder_output(main_config, connection_params):
        folder_path, log_path, object_list_path = FolderGenerator.generate_package_creation_folder_structure(connection_params)
        Log.configure_log(log_path, main_config["log_file_Basename"])
        return folder_path, object_list_path

    # Generate output folder and configure logs for package import/rollback processes
    @staticmethod
    def generate_import_rollback_folder_output(main_config, process_type, connection_params):
        if process_type != "Import" and process_type != "Rollback":
            raise Exception("Error: Invalid type provided, type must be one of the following:\n- Import\n- Rollback")
        folder_path, log_path = \
            FolderGenerator.generate_package_import_folder_structure(connection_params) \
            if process_type == "Import" \
            else FolderGenerator.generate_package_rollback_folder_structure(connection_params)
        Log.configure_log(log_path, main_config["log_file_Basename"])
        return folder_path

    # Generate output folder and configure logs for package migration processes
    @staticmethod
    def generate_migration_folder_output(main_config, source_connection_params, target_connection_params):
        folder_path, log_path, object_list_path = FolderGenerator.generate_package_migration_folder_structure(source_connection_params, target_connection_params)
        Log.configure_log(log_path, main_config["log_file_Basename"])
        return folder_path, object_list_path
