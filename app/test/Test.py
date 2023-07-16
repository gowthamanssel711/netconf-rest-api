import json
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from main import app

class NetConfTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_connect_client_successful(self):
        client_details = {
            'host': 'localhost',
            'password': '12345',
            'user': 'gowthaman',
            'port': 830
        }
        response = self.app.post('/connect_client', json=client_details)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['connected'], 'True')


    def test_ssh_connect_successful(self):
        client_details = {
            'host': 'localhost',
            'password': '12345',
            'user': 'gowthaman',
            'port': 22
        }
        response = self.app.post('/connect_client', json=client_details)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['connected'], 'True')


if __name__ == '__main__':
    unittest.main()
