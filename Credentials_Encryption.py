import base64
import json
import sys
import traceback

from src.utils.Encryption_Service import EncryptionService
from src.utils.arguments.Argument_Reader import ArgumentReader


def encode_credentials(encrypted_username, encrypted_password):
    encoded_encrypted_username = base64.b64encode(encrypted_username)
    encoded_encrypted_password = base64.b64encode(encrypted_password)
    print("Encrypted and base 64 encoded username: ", encoded_encrypted_username.decode())
    print("Encrypted and base 64 encoded password: ", encoded_encrypted_password.decode())


def encrypt_credentials(username, password, public_key_path):
    print("Original username: ", username)
    print("Original password: ", password)
    encrypted_keys = EncryptionService.encrypt_keys([username, password], public_key_path)
    print("Encrypted username: ", encrypted_keys[0])
    print("Encrypted password: ", encrypted_keys[1])
    encode_credentials(encrypted_keys[0],encrypted_keys[1])


try:
    encryption_config = json.load(open("./config/encryption/config.json"))[
        "encryption"]  # Read encryption configuration
    args = ArgumentReader(encryption_config["arguments"]).read_arguments()  # Read script input arguments
    encrypt_credentials(args["Username"], args["Password"], args["PublicKey"])

except Exception:
    print(traceback.format_exc())
    sys.exit(-1)
sys.exit(0)
