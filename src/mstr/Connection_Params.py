
# Plain class to store data required to establish a session (Session class).
class ConnectionParams:

    def __init__(self, username, password, project, environment):
        self.username = username
        self.password = password
        self.project = project
        self.environment = environment
