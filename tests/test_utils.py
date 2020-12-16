import pytest

from dateutil.parser import parse

from briefme_invoices.utils import extract_invoice_data

pytestmark = pytest.mark.django_db


def test_extract_invoice_data(transaction):
    # GIVEN / WHEN
    response = extract_invoice_data(transaction)

    # THEN
    assert "product" in response
    assert response.get("payment_date") == parse(transaction["created_at"])
    assert response.get("price_paid") == transaction.get("amount_in_cents") / 100
    assert response.get("transaction_id") == transaction.get("id")


def test_extract_invoice_data_payment_not_settled(unsettled_transaction):
    # GIVEN / WHEN
    response = extract_invoice_data(unsettled_transaction)

    # THEN
    assert response is None
