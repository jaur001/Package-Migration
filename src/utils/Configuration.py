import json

# Class which reads general configuration (config.json)
class Configuration:
    config = json.load(open("./config/config.json"))

    @staticmethod
    def get_property(prop):
        return Configuration.config[prop]
