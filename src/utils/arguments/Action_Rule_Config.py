import json


# Plain class in charge of reading action-rule file passes in parameters
class ActionRuleConfig:

    def __init__(self, file_path):
        self.config = json.load(open(file_path))

    def get_action(self, object_type):
        str_object_type = str(object_type)
        if str_object_type in self.config:
            return self.config[str_object_type]
        return self.config["default"]

