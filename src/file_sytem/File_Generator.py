import configparser
import inspect
import json
import traceback
from functools import reduce
from src.log_system.Level import Level
from src.log_system.Log import Log
from src.utils.Configuration import Configuration


class FileGenerator:
    binary_config = json.load(open("./config/binary_config.json"))

    config = configparser.ConfigParser()
    config.read("./config/logging.cfg")
    object_list_config = config["objectList"]
    manifest_config = config["manifest"]

    # Get filename for binary.
    @staticmethod
    def get_binary_filename(is_undo):
        filename = FileGenerator.binary_config["undofileBasename"] \
            if is_undo \
            else FileGenerator.binary_config["fileBasename"]
        file_extension = FileGenerator.binary_config["fileExtension"]
        return filename + "." + file_extension

    # Store binary in local machine
    @staticmethod
    def save_binary(binary, folder_path, is_undo):
        binary_name = FileGenerator.get_binary_filename(is_undo)
        method = inspect.currentframe().f_code.co_name
        undo_text = " undo " if is_undo else " "
        mmp = ""
        try:
            binary_path = folder_path + binary_name
            mmp = open(binary_path, "xb")
            mmp.write(binary)
            Log.log(Level.INFO, FileGenerator.__name__, method,
                              "Binary" + undo_text + "package saved successfully in local machine",
                              "Binary file " + binary_name + " has been saved in " + folder_path + " in local machine")
            return folder_path + binary_name
        except Exception:
            Log.add_error_log(Level.ERROR, FileGenerator.__name__, method,
                              "Error saving binary " + undo_text + " package file in local machine",
                              traceback.format_exc())
        finally:
            mmp.close()

    # Generate and store manifest file
    @staticmethod
    def generate_manifest(folder_path, properties):
        method = inspect.currentframe().f_code.co_name
        filename = FileGenerator.manifest_config["filename"] + "." + FileGenerator.manifest_config["fileExtension"]
        manifest = ""
        try:
            manifest_path = folder_path + filename
            manifest = open(manifest_path, "x")
            FileGenerator.write_properties(manifest, properties)
            Log.log(Level.INFO, FileGenerator.__name__, method,
                              "Manifest created successfully in local machine",
                              "Manifest has been saved in " + folder_path + " in local machine")
        except Exception:
            Log.add_error_log(Level.WARNING, FileGenerator.__name__, method,
                              "Error creating manifest in local machine",
                              traceback.format_exc())
        finally:
            manifest.close()

    # Write the properties to the file
    # The content includes version and key-value pair from properties object
    @staticmethod
    def write_properties(manifest, properties):
        ignored_props = FileGenerator.manifest_config["ignoredProps"].split(",")
        FileGenerator.write_property(manifest, "version", Configuration.get_property("version"))
        for key in properties:
            if key not in ignored_props:
                FileGenerator.write_property(manifest, key, properties[key])

    @staticmethod
    def write_property(manifest, key, value):
        if value is not None:
            manifest.write(key + ": " + value + "\n")

    # Generate object list (CSV), which holds the objects included in a created package
    @staticmethod
    def generate_object_list(object_list_path, mstr_main_objects, dependents):
        method = inspect.currentframe().f_code.co_name
        filename = FileGenerator.object_list_config["filename"] + "." + FileGenerator.object_list_config[
            "fileExtension"]
        file = None
        try:
            file = open(object_list_path + filename, "x")
            headers = FileGenerator.object_list_config["headers"].split(",")
            header = ",".join(headers)
            file.write(header + "\n")
            FileGenerator.add_objects(file, mstr_main_objects, True)
            FileGenerator.add_objects(file, dependents, False)
        except Exception:
            Log.add_error_log(Level.WARNING, FileGenerator.__name__, method,
                              "Error generating Object List with the package content",
                              traceback.format_exc())
        finally:
            file.close()

    # Add objects to object list file
    @staticmethod
    def add_objects(file, mstr_objects, is_source):
        for mstr_object in mstr_objects:
            mstr_object["source"] = "main" if is_source else "dependent"
            object_info = FileGenerator.add_object(mstr_object)
            file.write(object_info + "\n")

    @staticmethod
    def add_object(obj):
        props = FileGenerator.object_list_config["objectProps"].split(",")
        row = map(lambda prop: obj[prop], props)
        return reduce(lambda a, b: str(a) + "," + str(b), row)
