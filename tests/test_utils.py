import pytest

from dateutil.parser import parse

from briefme_invoices.utils import extract_invoice_data

pytestmark = pytest.mark.django_db


def test_extract_invoice_data(statement):
    # GIVEN / WHEN
    response = extract_invoice_data(statement)

    # THEN
    assert "product" in response
    assert response.get("payment_date") == parse(statement["settled_at"])
    assert response.get("price_paid") == statement.get("total_in_cents") / 100
    assert response.get("statement_id") == statement.get("id")


@pytest.mark.parametrize("key", ["settled_at", "total_in_cents"])
def test_extract_invoice_data_payment_not_settled(key, statement):
    # GIVEN / WHEN
    statement.pop(key, None)
    response = extract_invoice_data(statement)

    # THEN
    assert response is None


def test_extract_invoice_data_with_statement_on_later_statement(
    statement_on_later_statement,
):
    # GIVEN / WHEN
    response = extract_invoice_data(statement_on_later_statement)

    # THEN
    assert "product" in response
    assert response.get("payment_date") == parse(
        statement_on_later_statement["settled_at"]
    )
    assert (
        response.get("price_paid")
        == statement_on_later_statement.get("total_in_cents") / 100
    )
    assert response.get("statement_id") == statement_on_later_statement.get("id")
