import pytest

from briefme_invoices.apps import BriefmeInvoicesConfig

pytestmark = pytest.mark.django_db


class TestBriefmeInvoicesConfig:
    @staticmethod
    def test_apps():
        assert "briefme_invoices" in BriefmeInvoicesConfig.name
