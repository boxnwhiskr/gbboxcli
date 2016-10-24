import json
import unittest
from unittest.mock import Mock, MagicMock

from gbboxcli.api import API, HttpRemoteError


class APITest(unittest.TestCase):
    def setUp(self):
        self._expected_headers = {'gbbox-secret': 'SECRET',
                                  'content-type': 'application/json'}
        self._expected_error = {'error_type': 'E', 'message': 'M'}

    def test_get_config(self):
        mock_req = self.build_get(200, {})
        api = self.build_api(mock_req)

        config = api.get_config('goog')

        self.assertDictEqual({}, config)
        mock_req.get.assert_called_with(
            '/metadata/services/goog',
            headers=self._expected_headers
        )

    def test_get_config_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.get_config('goog')

        self.assertEqual('M', ctx.exception.message)
        self.assertEqual('E', ctx.exception.error_type)

    @staticmethod
    def build_api(req):
        return API.get_test_api(req, 'SECRET')

    @staticmethod
    def build_get(res_status_code, res_body):
        mock_req = MagicMock()
        mock_res = MagicMock()
        mock_res.status_code = res_status_code
        mock_res.data = json.dumps(res_body).encode('utf-8')
        mock_req.get = Mock(return_value=mock_res)
        return mock_req


if __name__ == '__main__':
    unittest.main()
