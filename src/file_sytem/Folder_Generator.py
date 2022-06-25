import os
from datetime import datetime
import re
from functools import reduce


# Generate folder for storing package creation, import, rollback or migration outputs
from src.utils.Configuration import Configuration


class FolderGenerator:
    folderStructures = Configuration.get_property("folderStructures")
    current_folder_suffix = None

    @staticmethod
    def generate_package_migration_folder_structure(source_connection_params, target_connection_params):
        return FolderGenerator.generate_folder_structure_with_object_list_folder([source_connection_params, target_connection_params], FolderGenerator.folderStructures["packageMigration"])

    @staticmethod
    def generate_package_creation_folder_structure(connection_params):
        return FolderGenerator.generate_folder_structure_with_object_list_folder([connection_params], FolderGenerator.folderStructures["packageCreation"])

    # Generate folder structure output with object list folder included
    @staticmethod
    def generate_folder_structure_with_object_list_folder(environments, folder_structure):
        folder_path, log_path = FolderGenerator.generate_folder_structure(environments, folder_structure)
        object_list_path = folder_path + folder_structure["objectListFolderName"] + "/"
        os.makedirs(object_list_path)
        return folder_path, log_path, object_list_path

    @staticmethod
    def generate_package_import_folder_structure(connection_params):
        folder_path, log_path = FolderGenerator.generate_folder_structure([connection_params], FolderGenerator.folderStructures["packageImport"])
        return folder_path, log_path

    @staticmethod
    def generate_package_rollback_folder_structure(connection_params):
        folder_path, log_path = FolderGenerator.generate_folder_structure([connection_params], FolderGenerator.folderStructures["packageRollback"])
        return folder_path, log_path

    # Default method used to generate shared folders: base folder and log folder.
    @staticmethod
    def generate_folder_structure(environments, folder_structure):
        date = datetime.now()
        str_date = str(date).replace(" ", "_").replace(":", "-")
        str_date = re.sub("\.(.*)", "", str_date)
        folder_suffix = "_" + str_date + "_" + FolderGenerator.get_environments(environments)
        FolderGenerator.current_folder_suffix = folder_suffix
        folder_name = folder_structure["baseFolderName"] + folder_suffix
        folder_path = folder_structure["path"] + folder_name + "/"
        log_path = folder_path + folder_structure["logFolderName"] + "/"
        os.makedirs(log_path)
        return folder_path, log_path

    # Retrieve environment and project name from each environment in the array.
    # The method output is a string with concatenated data by underscore (_)
    @staticmethod
    def get_environments(environments):
        env_data = map(lambda conn_params: conn_params.environment + "_" + conn_params.project, environments)
        return reduce(lambda a, b: a+"_"+b, env_data)
