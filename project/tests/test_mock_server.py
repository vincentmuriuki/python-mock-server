# # third party imports...
# from nose.tools import assert_true
# import requests
#
#
# def test_request_response():
#     url = 'http://localhost:{port}/users'.format(port=mock_server_port)
#
#     # send a request to the mock API server and store the response
#     response = requests.get(url)
#
#     # confirm that the request-response cycle completed successfully
#     assert_true(response.ok)


# # standard library iports...
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import socket
# from threading import Thread
#
# # third-party imports...
# from nose.tools import assert_true
# import requests
#
#
# class MockServerRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # process an HTTP GET request and return a response with an HTTP 200 STATUS
#         self.send_response(requests.codes.ok)
#         self.end_headers()
#         return
#
#
# def get_free_port():
#     s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
#     s.bind(('localhost', 0))
#     address, port = s.getsockname()
#     s.close()
#     return port
#
#
# class TestMockServer(object):
#     @classmethod
#     def setup_class(cls):
#         # configure mock server
#         cls.mock_server_port = get_free_port()
#         cls.mock_server = HTTPServer(('localhost', cls.mock_server_port), MockServerRequestHandler)
#
#         # start running mock server in a separate thread.
#         # Daemon threads automatically shut down when the main process exits.
#         cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
#         cls.mock_server_thread.setDaemon(True)
#         cls.mock_server_thread.start()
#
#     def test_request_response(self):
#         url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
#
#         # send a request to the mock API server and store the response.
#         response = requests.get(url)
#
#         # confirm that the request-repsonse cycle completed successfully.
#         print(response)
#         assert_true(response.ok)


# Third-party imports...
from unittest.mock import patch
from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

# Local imports...
from project.services import get_users
from project.tests.mocks import get_free_port, start_mock_server


class TestMockServer(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        mock_users_url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)

        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
        with patch.dict('project.services.__dict__', {'USERS_URL': mock_users_url}):
            response = get_users()

        assert_dict_contains_subset({'Content-Type': 'application/json; charset=utf-8'}, response.headers)
        assert_true(response.ok)
        assert_list_equal(response.json(), [])
