import json
from unittest import mock

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase


class JSSetLikeViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(JSSetLikeViewTest, cls).setUpClass()

        cls.group = Group.objects.create(
            name="Editors",
        )

        cls.content_type = ContentType.objects.get_for_model(Group)

        cls.superuser = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )

    @classmethod
    def tearDownClass(cls):
        super(JSSetLikeViewTest, cls).tearDownClass()
        cls.group.delete()
        cls.superuser.delete()

    def test_authenticated_json_set_like(self):
        from ..views import json_set_like

        mock_request = mock.Mock()
        mock_request.user = self.superuser
        mock_request.method = "POST"

        response = json_set_like(mock_request, self.content_type.pk, self.group.pk)

        expected_result = json.dumps(
            {"success": True, "action": "add", "count": Location.objects.count()}
        )

        self.assertJSONEqual(response.content, expected_result)

    @mock.patch("django.contrib.auth.models.User")
    def test_anonymous_json_set_like(self, MockUser):
        from ..views import json_set_like

        anonymous_user = MockUser()
        anonymous_user.is_authenticated = False

        mock_request = mock.Mock()
        mock_request.user = anonymous_user
        mock_request.method = "POST"

        response = json_set_like(mock_request, self.content_type.pk, self.group.pk)

        expected_result = json.dumps({"success": False})

        self.assertJSONEqual(response.content, expected_result)
