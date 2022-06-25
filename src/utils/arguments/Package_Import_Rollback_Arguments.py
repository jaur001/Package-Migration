from src.mstr.Connection_Params import ConnectionParams


# Plain class used to store arguments for Package Import/Rollback
class PackageImportRollbackArguments:

    def __init__(self, args):
        self.target_connection_params = ConnectionParams(args["TargetUsername"],
                                                         args["TargetPassword"],
                                                         args["TargetProject"],
                                                         args["TargetEnvironment"])
        self.package = args["package"] if "package" in args else None
        self.import_type = args["type"] if "type" in args else "Import"
