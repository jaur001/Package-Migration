import rsa


class EncryptionService:

    @staticmethod
    def encrypt_key(key, public_key_path):
        public_key = EncryptionService.get_public_key(public_key_path)
        return rsa.encrypt(key.encode(), public_key)

    @staticmethod
    def encrypt_keys(keys, public_key_path):
        public_key = EncryptionService.get_public_key(public_key_path)
        encrypted_keys = []
        for key in keys:
            encrypted_key = rsa.encrypt(key.encode(), public_key)
            encrypted_keys.append(encrypted_key)
        return encrypted_keys

    @staticmethod
    def decrypt_key(encrypted_key, private_key_path):
        private_key = EncryptionService.get_private_key(private_key_path)
        return rsa.decrypt(encrypted_key, private_key).decode()

    @staticmethod
    def decrypt_keys(encrypted_keys, private_key_path):
        private_key = EncryptionService.get_private_key(private_key_path)
        decrypted_keys = []
        for encrypted_key in encrypted_keys:
            decrypted_key = rsa.decrypt(encrypted_key, private_key).decode()
            decrypted_keys.append(decrypted_key)
        return decrypted_keys

    @staticmethod
    def get_public_key(public_key_path):
        with open(public_key_path, 'rb') as public_file:
            public_key_data = public_file.read()
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_data)
        return public_key

    @staticmethod
    def get_private_key(private_key_path):
        with open(private_key_path, 'rb') as private_file:
            private_key_data = private_file.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key_data, 'PEM')
        return private_key
