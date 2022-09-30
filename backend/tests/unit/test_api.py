# from config import TestConfiguration
# from unittest import mock
# from backend.models.models import Domains as domains
# from app import (
#     app,
#     db
# )
# from datetime import (
#     datetime,
#     timedelta
# )
# from backend.utils.exceptions import (
#     DatabaseError
# )

# # import pdb; pdb.set_trace()

# class TestAPIs():
#     CLIENT = app.test_client()

#     def setup_method(self):
#         pass

#     def teardown_method(self):
#         pass

#     def test_health(self):
#         """
#         Ensure health endpoint happy path works as intended.
#         """
#         expected_status_code = 200
#         expected_text = '{\n  "live": true,\n  "status_code": 200\n}\n'

#         # Tested API
#         resp = self.CLIENT.get(f'{TestConfiguration.API_URI}/health')

#         assert resp.status_code == expected_status_code
#         assert resp.text == expected_text

#     @mock.patch('backend.routes.api.is_db_live', return_value=False)
#     def test_health_db_offline(self, mock_connection):
#         """
#         Ensure health endpoint throws when DB is offline.
#         """
#         expected_json = {
#             "error_reason": "Database is not online.",
#             "exception_type": "DataBaseOffline",
#             "status_code": 400,
#         }

#         # Tested API
#         resp = self.CLIENT.get(f'{TestConfiguration.API_URI}/health')

#         actual_json = resp.json
#         actual_json.pop('traceback', None)
#         assert actual_json == expected_json

#     @mock.patch('backend.routes.api.is_db_live', side_effect = DatabaseError)
#     def test_health_db_error(self, mock_connection):
#         """
#         Ensure health endpoint throws if 
#         backend/utils/utils:is_db_live throws.
#         """
#         expected_json = {
#             'error_reason': 'Database error.',
#             'exception_type': 'DatabaseError',
#             'status_code': 400
#         }

#         # Tested API
#         resp = self.CLIENT.get(f'{TestConfiguration.API_URI}/health')

#         actual_json = resp.json
#         actual_json.pop('traceback', None)
#         assert actual_json == expected_json