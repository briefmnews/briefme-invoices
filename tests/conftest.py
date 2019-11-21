import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from .factories import InvoiceFactory


@pytest.fixture
def invoice():
    return InvoiceFactory()


@pytest.fixture
def request_builder():
    return RequestBuilder()


class RequestBuilder:
    @staticmethod
    def get(path="/", user=None):
        rf = RequestFactory()
        request = rf.get(path)
        request.user = user if user else AnonymousUser()

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        return request
