from tests.base_test_case import BaseTestCase

class TestUsersAPI(BaseTestCase):
    def test_get_users(self):
        rv =  self.client.get("/v1/users")
        assert rv.data == b"Got Users"