from datetime import datetime
from itertools import product
from math import prod
from turtle import title
import pytest
from rest_framework import status
from model_bakery import baker

from store.models import Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product


@pytest.mark.django_db
class TestCreatCollection:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({
            'title': 'title',
            'slug': 'glug',
            'description': 'description',
            'unit_price': 4,
            'last_update': 'new_date',
            'collection': 1,
            'promotions': 'none'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_admin_returns_403(self, authenticate, create_product):
        authenticate(is_staff=False)

        response = create_product({
            'title': 'title',
            'slug': 'glug',
            'description': 'description',
            'unit_price': 4,
            'last_update': 'new_date',
            'collection': 1,
            'promotions': 'none'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({
            'title': '',
            'slug': '',
            'description': '',
            'unit_price': 0,
            'last_update': '',
            'collection': 0,
            'promotions': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_isvalid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({
            'title': 'title',
            'slug': 'glug',
            'description': 'description',
            'unit_price': 4,
            'last_update': datetime.now(),
            'collection': 1,
            'inventory': 2,
            'promotions': 'promotions'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product)

        response = api_client.post(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert status.data == {
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'unit_price': product.unit_price,
            'last_update': product.last_update,
            'collection': product.collection,
            'inventory': product.inventory,
            'promotions': product.promotions
        }
