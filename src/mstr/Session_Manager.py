from src.mstr.Mstr_Rest_Service import MstrRestService
from src.mstr.Session import Session
from src.utils.Configuration import Configuration


class SessionManager:
    environments = Configuration.get_property("environments")
    projects = Configuration.get_property("projects")

    @staticmethod
    def login(connection_params):
        environment_url = Configuration.get_property("environments")[connection_params.environment]
        project_id = Configuration.get_property("projects")[connection_params.project]
        auth_token = MstrRestService.login(connection_params.username, connection_params.password, environment_url)
        return Session(auth_token, connection_params.environment, environment_url, connection_params.project, project_id)

    @staticmethod
    def logout(session):
        MstrRestService.logout(session)

