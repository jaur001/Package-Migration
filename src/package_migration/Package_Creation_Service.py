import inspect
import traceback
from datetime import datetime

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.file_sytem.File_Generator import FileGenerator
from src.package_migration.Package_Service import PackageService
from src.package_migration.Search_Object_Service import SearchObjectService
from src.utils.arguments.Action_Rule_Config import ActionRuleConfig


class PackageCreationService:

    def __init__(self, package_creation_args, folder_path):
        self.package_creation_args = package_creation_args
        self.folder_path = folder_path

    def create_package(self, session, object_list_path):
        method = inspect.currentframe().f_code.co_name
        start = datetime.now()
        Log.log(Level.INFO, self.__class__.__name__, method,
                "Creating package",
                "Package is being created. Search Object ID used: " + self.package_creation_args.search_object)
        print("Package Creation in progress...")
        package_service = PackageService(session)
        try:
            action_rule_config = ActionRuleConfig(
                self.package_creation_args.action_rule)  # Holds data about action rule for each object type
            # Obtains objects to be included in package
            mstr_objects, mstr_main_objects, dependents = SearchObjectService.get_objects(session,
                                                                                          self.package_creation_args.search_object,
                                                                                          self.package_creation_args.dependency)
            FileGenerator.generate_object_list(object_list_path, mstr_main_objects,
                                               dependents)  # Generate object list (all mstr objects)
            binary_path = package_service.create_package(mstr_objects, action_rule_config,
                                                         self.folder_path)  # Create package, obtaining path the mmp file
            end = datetime.now()
            message = "Package Creation finished successfully. Finished in " + str(
                end - start) + ". Binary path: " + binary_path
            Log.log(Level.INFO, self.__class__.__name__, method,
                    "Package created",
                    message)
            print(message)
            return binary_path
        except Exception as e:
            Log.add_error_log(Level.ERROR, self.__class__.__name__, method, "Package Creation failed",
                              traceback.format_exc())
            raise e
        finally:
            package_service.finish_process()  # Delete metadata package
