
# Hold details from a MicroStrategy session
class Session:

    def __init__(self, auth_token, environment, environment_url, project, project_id):
        self.auth_token = auth_token
        self.environment = environment
        self.environment_url = environment_url
        self.project = project
        self.project_id = project_id
