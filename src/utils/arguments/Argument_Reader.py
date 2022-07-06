import base64
import getopt
import json
import sys
from functools import reduce


# Reads arguments passed in script
from src.utils.Configuration import Configuration
from src.utils.Encryption_Service import EncryptionService


class ArgumentReader:
    decryption_config = json.load(open("./config/encryption/config.json"))["decryption"]

    def __init__(self, arguments):
        self.arguments = arguments

    # Main method which is in charge of reading the input arguments. It consumes getopt python library
    def read_arguments(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", longopts=self.arguments["options"])
            opt_json = self.convert_to_json(opts)
            args = self.get_arguments(opt_json)
            if Configuration.get_property("decryptCredentials"):
                self.decrypt_args(args)
            return args
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
            args[key] = self.get_argument(opt_json, key)
        return args

    def get_argument(self, opt_json, key):
        if "--" + key in opt_json:
            return opt_json["--" + key]
        if self.key_is_required(key):
            raise Exception("Error: Argument --" + key + " is required")
        return None

    def key_is_required(self, key):
        return key not in self.arguments["nonRequired"]

    def decrypt_args(self, args):
        private_key_path = self.decryption_config["privateKey"]
        args_to_decrypt = self.get_args_to_decrypt(args)
        encrypted_keys = list(map(lambda arg_name: self.get_and_decode_key(arg_name, args), args_to_decrypt))
        decrypted_keys = EncryptionService.decrypt_keys(encrypted_keys, private_key_path)
        for index, arg_to_decrypt in enumerate(args_to_decrypt):
            args[arg_to_decrypt] = decrypted_keys[index]

    @staticmethod
    def get_and_decode_key(arg_name, args):
        return base64.b64decode(args[arg_name])

    def get_args_to_decrypt(self, args):
        args_to_decrypt = self.decryption_config["argumentsToDecrypt"]
        return list(filter(lambda arg_to_decrypt: arg_to_decrypt in args, args_to_decrypt))

    # Display help command
    def display_help_command(self):
        argument_keys = self.arguments["argMapping"]
        script_name = self.arguments["scriptName"]
        command_args = map(lambda key: "--" + key + " <" + key.lower() + ">", argument_keys)
        full_command = reduce(lambda a, b: a + " " + b, command_args, script_name)
        print("Help command:")
        print(full_command)

