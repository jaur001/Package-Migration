import inspect
import json

from src.log_system.Level import Level
from src.log_system.Log import Log
from src.utils.Http_Client import HttpClient
from src.utils.Http_Params import HttpParams


# NOT USED
# Class used to consume MicroStrategy Task API
class MstrTaskService:
    http_client = HttpClient()
    mstr = json.load(open("./config/mstr_internal_config.json"))
    tasks = mstr["tasks"]

    # Purge element cache from a specific project
    # This task is currently not used in this solution
    # Alert: This is a customer task, the plugin is required to be used.
    @staticmethod
    def purge_element_cache(environment_url, username, password, project, project_id):
        url = environment_url + MstrTaskService.tasks[
            "purgeElementCache"] + username + "&password=" + password + "&projectId=" + project_id
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        method = inspect.currentframe().f_code.co_name

        def process_error(res):
            Log.add_http_error_log(res, MstrTaskService, method,
                                            "Error purging element cache for project " + project + " (" + project_id + ")")

        def process_success(res):
            Log.log(Level.INFO, MstrTaskService, method,
                                           "Purge element cache ended successfully",
                                           "Purge element cache ended successfully for project " + project + " (" + project_id + ")")

        params = HttpParams(url, headers, None, process_success, process_error)
        MstrTaskService.http_client.make_post_request(params)
