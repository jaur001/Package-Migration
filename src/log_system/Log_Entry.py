
# Plain class for storing data required for logging a message
from datetime import datetime


class LogEntry:

    def __init__(self, level, className, method, title, message):
        self.level = level
        self.timestamp = datetime.now()
        self.className = className
        self.method = method
        self.title = title
        self.message = message

    def get_message(self):
        return self.title + ": " + self.message
