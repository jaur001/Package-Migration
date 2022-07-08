import inspect
import json
import traceback

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.mstr.Mstr_Rest_Service import MstrRestService


class SearchObjectService:
    folder_type = 8
    filtered_types = json.load(open("./config/config.json"))["filteredObjectTypes"]

    # Get all objects from a Search object, retrieving the search result
    # and including dependent objects if needed
    @staticmethod
    def get_objects(session, search_object_id, dependency):
        method = inspect.currentframe().f_code.co_name
        try:
            search_object_result = MstrRestService.get_search_object_result(session, search_object_id)
            mstr_main_objects = SearchObjectService.process_search_object_result(search_object_result)
            dependents = SearchObjectService.get_dependencies(dependency, mstr_main_objects, session, inherit_action=True)
            Log.log(Level.INFO, SearchObjectService.__name__, method,
                    "Mstr objects retrieved successfully",
                    "All the objects (source and dependent ones) were retrieved successfully and are ready to be include in package content")
            return mstr_main_objects, dependents
        except Exception:
            Log.add_error_log(Level.ERROR, SearchObjectService.__name__, method,
                              "Error retrieved mstr objects for package content",
                              traceback.format_exc())

    # Process result obtained from Search object, retrieving all the objects.
    @staticmethod
    def process_search_object_result(search_object_result):
        approved_objects = []
        for obj in search_object_result:
            if not SearchObjectService.is_filtered_type(obj["type"]):
                approved_objects.append(obj)
        return approved_objects

    # Obtain dependent objects from the original objects
    @staticmethod
    def get_dependencies(dependency, mstr_main_objects, session, inherit_action=False):
        dependents = []
        if dependency == "DD" or dependency == "AD":
            include_all_dependencies = dependency == "AD"
            for mstr_object in mstr_main_objects:
                object_tree = SearchObjectService.get_dependent_objects(session, mstr_object["id"], mstr_object["type"],
                                                                        mstr_object["name"], include_all_dependencies)
                parse_objects = SearchObjectService.parse_tree(object_tree, include_current_folder=False)
                for obj in parse_objects:
                    if SearchObjectService.is_valid_object(obj, mstr_main_objects, dependents):
                        if inherit_action:
                            obj["action"] = mstr_object["action"]
                        dependents.append(obj)
        return dependents

    # Get dependent objects from a main object
    @staticmethod
    def get_dependent_objects(session, mstr_object_id, object_type, object_name, include_all_dependencies):
        usedByObject = mstr_object_id + ";" + str(object_type)
        search_id = MstrRestService.create_search(session, usedByObject, object_name, include_all_dependencies)
        return MstrRestService.get_search_result(session, search_id, object_name)

    # Parse tree with objects obtained from REST API
    @staticmethod
    def parse_tree(object_tree, folder="", include_current_folder=True):
        objects = []
        if object_tree["type"] == SearchObjectService.folder_type:
            if include_current_folder:
               folder += object_tree["name"] + "/"
            for child in object_tree["children"]:
                objects += SearchObjectService.parse_tree(child, folder)
        else:
            object_tree["path"] = folder[0:len(folder) - 2]
            objects.append(object_tree)
        return objects

    @staticmethod
    def is_valid_object(object_to_add, mstr_main_objects, dependents):
        return not SearchObjectService.object_is_already_included(object_to_add["id"], mstr_main_objects, dependents) \
            and not SearchObjectService.is_filtered_type(object_to_add["type"])

    # Check if the object was already included to the final list, to avoid duplicates
    @staticmethod
    def object_is_already_included(object_id, mstr_main_objects, dependents):
        all_objects = mstr_main_objects + dependents
        for mstr_object in all_objects:
            if mstr_object["id"] == object_id:
                return True
        return False

    # Check if the object type is banned and needs to be filtered (config.json)
    @staticmethod
    def is_filtered_type(object_type):
        return object_type in SearchObjectService.filtered_types
