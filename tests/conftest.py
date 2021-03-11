import json
import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from .factories import InvoiceFactory, UserFactory


@pytest.fixture
def invoice():
    return InvoiceFactory()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def request_builder():
    return RequestBuilder()


@pytest.fixture
def transaction():
    with open(
        "tests/fixtures/transaction_active_subscription_with_card.json", "r"
    ) as json_file:
        return json.loads(json_file.read())


@pytest.fixture
def unsettled_transaction():
    with open("tests/fixtures/unsettled_transaction.json", "r") as json_file:
        return json.loads(json_file.read())


class RequestBuilder:
    @staticmethod
    def get(path="/", user=None):
        rf = RequestFactory()
        request = rf.get(path)
        request.user = user if user else AnonymousUser()

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        return request

    @staticmethod
    def post(path="/", user=None, data=None):
        rf = RequestFactory()
        request = rf.post(path, data=data)
        request.user = user if user else AnonymousUser()

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        return request
