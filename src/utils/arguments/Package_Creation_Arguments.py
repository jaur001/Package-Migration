from src.mstr.Connection_Params import ConnectionParams


# Plain class used to store arguments for Package Creation
class PackageCreationArguments:

    def __init__(self, args):
        self.source_connection_params = ConnectionParams(args["SourceUsername"],
                                                         args["SourcePassword"],
                                                         args["SourceProject"],
                                                         args["SourceEnvironment"])
        self.search_object = args["searchObject"]
        self.dependency = args["dependency"]
        self.action_rule = args["actionRule"]
