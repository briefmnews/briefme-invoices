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
def statement():
    with open("tests/fixtures/statement_active_subscription_with_card.json", "r") as json_file:
        return json.loads(json_file.read()).get("statement")


@pytest.fixture
def statement_on_later_statement():
    with open("tests/fixtures/statement_with_payment_on_later_statement.json", "r") as json_file:
        return json.loads(json_file.read()).get("statement")


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
