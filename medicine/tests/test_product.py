from medicine.tests.test_setup import TestBaseSetup
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

"""
Testing the product model endpoints.
"""


class TestProduct(TestBaseSetup):
    def test_get_product(self):
        response = self.client.get(self.url)
        response.render()
        self.assertEqual(200, response.status_code)

    def test_post_product(self):
        data = dict(name='product name', image='', quantity=10, unit_price=23, expired_on='2029-09-09', product_info='')
        response = self.client.post(self.url, encode_multipart(data=data, boundary=BOUNDARY),
                                    content_type=MULTIPART_CONTENT)
        self.prId = response.data['id']
        self.assertEqual(201, response.status_code)

    def test_retrieve_product(self):
        response = self.client.get(self.url + self.prId + '/')
        self.assertEqual(200, response.status_code)

    def test_retrieve_product_invalid_id(self):
        response = self.client.get(self.url + '0/')
        self.assertEqual(404, response.status_code)
