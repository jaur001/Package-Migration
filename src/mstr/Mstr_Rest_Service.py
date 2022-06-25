import json
import inspect

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.utils.Configuration import Configuration
from src.utils.Http_Client import HttpClient
from src.utils.Http_Params import HttpParams


# Class used to consume MicroStrategy REST API
class MstrRestService:
    http_client = HttpClient()
    mstr = json.load(open("./config/mstr_internal_config.json"))
    endpoints = mstr["endpoints"]

    @staticmethod
    def logout(session):
        url = session.environment_url + MstrRestService.endpoints["closeSession"]
        headers = {
            "Content-type": "application/json",
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method,
                                   "Error closing session " + str(res.status_code),
                                   level=Level.WARNING)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Session Closed",
                    "The MicroStrategy Library session has been closed in " + session.environment)

        params = HttpParams(url, headers, None, process_success, process_error)
        MstrRestService.http_client.make_post_request(params)

    @staticmethod
    def login(username, password, environment_url):
        url = environment_url + MstrRestService.endpoints["login"]
        headers = {"Content-type": "application/json"}
        body = {"username": username, "password": password, "loginMode": Configuration.get_property("loginMode")}
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Login Error " + str(res.status_code))

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Success Login",
                    "The script has authenticated successfully into Library using REST API")
            return res.headers.get("X-MSTR-AuthToken")

        params = HttpParams(url, headers, body, process_success, process_error)
        return MstrRestService.http_client.make_post_request(params)

    @staticmethod
    def get_search_object_result(session, search_object_id):
        url = session.environment_url + MstrRestService.endpoints[
            "searchObject"] + search_object_id + "/results?includeAncestors=true"
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error obtaining results from Search Object")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method,
                    "MicroStrategy objects from Search object retrieved successfully",
                    "The source objects has been retrieved from the Search Object specified in the command")
            return json.loads(res.text)["result"]

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def create_search(session, usedByObject, object_name, include_all_dependencies):
        url = session.environment_url + MstrRestService.endpoints[
            "createSearch"] + usedByObject + "&usedByRecursive=" + str(
            include_all_dependencies)
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method,
                                   "Error Creating search to retrieve dependent objects from " + object_name)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method,
                    "Search to retrieve dependent objects performed successfully",
                    "The search performed to objects used by " + object_name + " was completed, ready to retrieve results.")
            return json.loads(res.text)["id"]

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_post_request(params)

    @staticmethod
    def get_search_result(session, search_id, object_name):
        url = session.environment_url + MstrRestService.endpoints["getSearchResult"] + search_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method,
                                   "Error getting result from search when retrieving dependent objects from " + object_name)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Dependent objects retrieved successfully",
                    "All the objects used by " + object_name + " has been retrieved successfully")
            return json.loads(res.text)

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def create_empty_package(session):
        url = session.environment_url + MstrRestService.endpoints["package"]
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error creating the base metadata package")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Base metadata package created",
                    "The base metadata package has been created and is ready to be populated")
            return json.loads(res.text)["id"]

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_post_request(params)

    @staticmethod
    def get_package_structure(content):
        package_structure = MstrRestService.mstr["packageStructure"]
        package_structure["content"] = content
        return package_structure

    @staticmethod
    def update_package_content(session, package_id, content):
        body = MstrRestService.get_package_structure(content)
        url = session.environment_url + MstrRestService.endpoints["package"] + "/" + package_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token,
            "Prefer": "respond-async"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error updating metadata package content")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Metadata package update process started",
                    "The metadata package is being updated and populated with the MicroStrategy objects (in progress)")

        params = HttpParams(url, headers, body, process_success, process_error)
        MstrRestService.http_client.make_put_request(params)

    @staticmethod
    def delete_package(session, package_id):
        url = session.environment_url + MstrRestService.endpoints["package"] + "/" + package_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token,
            "Prefer": "respond-async"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error deleting metadata package",
                                   level=Level.WARNING)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Metadata package deleted successfully",
                    "The Metadata package has been deleted successfully from MicroStrategy metadata (Binary is already downloaded)")

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_delete_request(params)

    @staticmethod
    def check_status(session, package_id):
        url = session.environment_url + MstrRestService.endpoints["package"] + "/" + package_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error retrieving package status")

        def process_success(res):
            status = json.loads(res.text)["status"]
            if status == "failed":
                Log.add_http_error_log(res, MstrRestService.__name__, method, "Update package process failed")
            return status == "ready"

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def download_binary(session, package_id):
        url = session.environment_url + MstrRestService.endpoints["package"] + "/" + package_id + "/binary"
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token,
            "Accept": "application/octet-stream"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error downloading binary package")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Binary package downloaded successfully",
                    "Binary package file has been downloaded with the objects to migrate")
            return res.content

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def upload_binary(session, package_id, package_path):
        files = [("file", ("package.mmp", open(package_path, "rb"), 'application/octet-stream'))]
        url = session.environment_url + MstrRestService.endpoints["package"] + "/" + package_id + "/binary"
        headers = {
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error uploading binary to metadata package")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Binary upload process started",
                    "The binary file is being uploaded to the metadata package (in progress)")

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.upload_file_put(params, files)

    @staticmethod
    def create_import_process(session, package_id, generate_undo):
        url = session.environment_url + MstrRestService.endpoints["import"] + "?generateUndo=" + str(
            generate_undo) + "&packageId=" + package_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token,
            "Prefer": "respond-async"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error creating import process")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Import process created successfully",
                    "Import process created successfully, the process is running in background (in progress)")
            return json.loads(res.text)["id"]

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_post_request(params)

    @staticmethod
    def close_import_process(session, import_id):
        url = session.environment_url + MstrRestService.endpoints["import"] + "/" + import_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token,
            "Prefer": "respond-async"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error closing import process",
                                   level=Level.WARNING)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Import process closed successfully",
                    "Import process closed successfully")

        params = HttpParams(url, headers, None, process_success, process_error)
        MstrRestService.http_client.make_delete_request(params)

    @staticmethod
    def check_import_status(session, import_id):
        url = session.environment_url + MstrRestService.endpoints["import"] + "/" + import_id
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error retrieving import status")

        def process_success(res):
            result = json.loads(res.text)
            return result["status"], result["undoPackageCreated"]

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def download_undo_binary(session, import_id):
        url = session.environment_url + MstrRestService.endpoints["import"] + "/" + import_id + "/undoPackage/binary"
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method, "Error downloading undo package")

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method,
                    "Binary undo package downloaded successfully",
                    "Binary undo package file has been downloaded with information to rollback if needed")
            return res.content

        params = HttpParams(url, headers, None, process_success, process_error)
        return MstrRestService.http_client.make_get_request(params)

    @staticmethod
    def update_schema(session):
        url = session.environment_url + MstrRestService.endpoints["schema"]
        schema_options = MstrRestService.mstr["schemaOptions"]
        headers = {
            "Content-type": "application/json",
            "X-MSTR-ProjectID": session.project_id,
            "X-MSTR-AuthToken": session.auth_token
        }
        body = {
            "updateTypes": schema_options
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrRestService.__name__, method,
                                   "Error updating schema for project " + session.project + " (" + session.project_id + ")",
                                   level=Level.WARNING)

        def process_success(res):
            Log.log(Level.INFO, MstrRestService.__name__, method, "Schema updated successfully",
                    "Schema updated successfully for project " + session.project + " (" + session.project_id + ")")

        params = HttpParams(url, headers, body, process_success, process_error)
        MstrRestService.http_client.make_post_request(params)
