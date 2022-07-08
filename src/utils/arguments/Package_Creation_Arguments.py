from src.mstr.Connection_Params import ConnectionParams


# Plain class used to store arguments for Package Creation
class PackageCreationArguments:

    def __init__(self, args):
        self.source_connection_params = ConnectionParams(args["sourceUsername"],
                                                         args["sourcePassword"],
                                                         args["sourceProject"],
                                                         args["sourceEnvironment"])
        self.mstr_objects = args["mstrObjects"] if "mstrObjects" in args else None
        self.search_object = args["searchObject"] if "searchObject" in args else None
        self.dependency = args["dependency"]
        self.action_rule = args["actionRule"] if "actionRule" in args else None

