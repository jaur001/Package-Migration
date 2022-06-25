import json

import requests


# Generic class to make http requests
# It wraps python requests library
class HttpClient:

    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def process_response(response, process_success=None, process_error=None):
        if 200 <= response.status_code < 300:
            if process_success is not None:
                return process_success(response)
        else:
            if process_error is not None:
                process_error(response)

    def make_get_request(self, httpParams):
        response = self.session.get(httpParams.url, headers=httpParams.headers)
        return self.process_response(response, httpParams.process_success, httpParams.process_error)

    def make_post_request(self, httpParams):
        response = self.session.post(httpParams.url, headers=httpParams.headers, data=json.dumps(httpParams.body))
        return self.process_response(response, httpParams.process_success, httpParams.process_error)

    def make_put_request(self, httpParams):
        response = self.session.put(httpParams.url, headers=httpParams.headers, data=json.dumps(httpParams.body))
        return self.process_response(response, httpParams.process_success, httpParams.process_error)

    def upload_file_put(self, httpParams, files):
        response = self.session.put(httpParams.url, headers=httpParams.headers, data={}, files=files)
        return self.process_response(response, httpParams.process_success, httpParams.process_error)

    def make_delete_request(self, httpParams):
        response = self.session.delete(httpParams.url, headers=httpParams.headers)
        return self.process_response(response, httpParams.process_success, httpParams.process_error)
