import configparser
import logging

from src.log_system.Level import Level
from src.log_system.Log_Entry import LogEntry


# Class for logs, it uses python logging library
class Log:
    config = configparser.ConfigParser()
    config.read("./config/logging.cfg")
    log_config = config["Log"]

    # Configure default settings for the logs
    # Executed at the beginning of the process after folder output is generated.
    @staticmethod
    def configure_log(log_path, filename):
        full_filename = log_path + filename + "." + Log.log_config["fileExtension"]
        logging.basicConfig(
            format=Log.log_config["format"],
            level=Level[Log.log_config["level"]].value,
            filename=full_filename,
            filemode=Log.log_config["filemode"]
        )

    @staticmethod
    def get_entry_details(log_entry):
        extra = {}
        for header in Log.log_config["extra"].split(","):
            extra[header] = log_entry.__dict__[header]
        return extra

    # Generic method to log messages
    # It expects LogEntry instances.
    @staticmethod
    def add_log_entry(log_entry):
        if isinstance(log_entry, LogEntry):
            extra = Log.get_entry_details(log_entry)
            logging.log(level=log_entry.level.value, msg=log_entry.message, extra=extra)

    # Method to log passing Log entry parameters without instance
    @staticmethod
    def log(level, class_name, method, message, details):
        log_entry = LogEntry(level, class_name, method, message, details)
        Log.add_log_entry(log_entry)
        return log_entry

    # Add error log, throw exceptions
    @staticmethod
    def add_error_log(level, class_name, method, message, details, throw_error=True):
        log_entry = Log.log(level, class_name, method, message, details)
        if throw_error:
            raise Exception(log_entry.get_message())

    # Add error log for http requests
    @staticmethod
    def add_http_error_log(response, class_name, method, message, level=Level.ERROR, throw_error=True):
        Log.add_error_log(level, class_name, method, message, response.text, throw_error)
