import getopt
import sys
from functools import reduce


# Reads arguments passed in script
class ArgumentReader:

    def __init__(self, arguments):
        self.arguments = arguments

    # Main method which is in charge of reading the input arguments. It consumes getopt python library
    def read_arguments(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", longopts=self.arguments["options"])
            opt_json = self.convert_to_json(opts)
            return self.get_arguments(opt_json)
        except getopt.GetoptError as e:
            print(e)
            self.display_help_command()
            sys.exit(-1)

    # Convert the object provided by the getopt library into a JSON
    def convert_to_json(self, opts):
        opt_json = {}
        for opt, arg in opts:
            if opt == '--help':
                self.display_help_command()
                sys.exit(0)
            opt_json[opt] = arg
        return opt_json

    # Retrieve JSON with the values containing only the expected arguments for the script.
    def get_arguments(self, opt_json):
        argument_keys = self.arguments["argMapping"]
        args = {}
        for key in argument_keys:
            args[key] = opt_json["--" + key]
        return args

    # Display help command
    def display_help_command(self):
        argument_keys = self.arguments["argMapping"]
        script_name = self.arguments["scriptName"]
        command_args = map(lambda key: "--" + key + " <" + key.lower() + ">", argument_keys)
        full_command = reduce(lambda a, b: a + " " + b, command_args, script_name)
        print("Help command:")
        print(full_command)

