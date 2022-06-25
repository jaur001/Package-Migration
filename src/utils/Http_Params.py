# Plain class to store details required to perform an http request
class HttpParams:

    def __init__(self, url, headers, body, process_success, process_error):
        self.url = url
        self.headers = headers
        self.body = body
        self.process_success = process_success
        self.process_error = process_error
