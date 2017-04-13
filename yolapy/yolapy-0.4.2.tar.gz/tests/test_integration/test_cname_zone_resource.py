from uuid import uuid4

from demands import HTTPServiceError

from tests.test_integration.test_case import YolaServiceTestCase


class TestYolaSubscription(YolaServiceTestCase):
    """Yola: Subscription resource"""

    def test_cname_zone_creation_api_is_called(self):
        self.assertRaisesHttpServiceError(
            400, '["zone is already taken by different user"]',
            self.service.create_cname_zone,
            '{}.example.org'.format(uuid4().hex),
            'WL_BOTTOMLINE_YOLA'
        )

    def assertRaisesHttpServiceError(
            self, status_code, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except HTTPServiceError, exc:
            self.assertEqual(exc.response.status_code, status_code)
            self.assertEqual(
                exc.response.content,
                '["zone is already taken by different user"]'
            )
