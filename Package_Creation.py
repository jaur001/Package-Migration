import json
import sys
import traceback

from Package_API import PackageAPI
from src.utils.arguments.Argument_Reader import ArgumentReader

try:
    main_config = json.load(
        open("./config/package_creation_config.json"))  # Read configuration for Package Creation script
    args = ArgumentReader(main_config["arguments"]).read_arguments()  # Read script input arguments
    PackageAPI.create_package(args)
except Exception:
    print(traceback.format_exc())
    sys.exit(-1)
sys.exit(0)
