import logging
from dateutil.parser import parse


logger = logging.getLogger(__name__)


class UncoveredInvoicing(Exception):
    pass


def get_invoices_data_for(user):
    """For a given user, generate a list of dict containing invoices information."""

    invoices = []

    for (
        subscription
    ) in user.subscription_set.all():  # should we filter on certain states ?
        subscription_id = subscription.chargify_subscription["id"]
        statements = subscription.chargify_helper.get_subscription_statements(
            subscription_id
        )
        for statement in statements:
            invoice_data = extract_invoice_data(statement)
            if invoice_data:
                invoices.append(invoice_data)

    return invoices


def extract_invoice_data(statement):
    """
    Given a Chargify statement, extract necessary invoice info : price, product, payment date.

    Note : only the common case is handled : a statement with a single "charge" transaction
    and a single "payment" transaction. More complicated payment's scenario must be handled
    manually.
    """

    if not (statement.get("total_in_cents", 0) > 0):
        # ignore statement with no billed amount
        return None

    payments = [t for t in statement["transactions"] if t["type"] == "Payment"]
    charges = [t for t in statement["transactions"] if t["type"] == "Charge"]
    if not (payments and charges):
        # invoice only what have been paid
        return None

    statement_id = statement["id"]
    if len(charges) > 1:
        logger.error(f"More than one charge for {statement_id}")
        raise UncoveredInvoicing()
    if len(payments) > 1:
        logger.error(f"More than one payment for {statement_id}")
        raise UncoveredInvoicing()

    charge = charges[0]
    payment = payments[0]

    if charge["kind"] != "baseline" or not charge["success"]:
        logger.error(f"Unhandled charge in statement {statement_id}")
        raise UncoveredInvoicing()
    if not payment["success"]:
        logger.error(f"Unhandled payment in statement {statement_id}")
        raise UncoveredInvoicing()

    return {
        "product": charge["item_name"],
        "payment_date": parse(payment["created_at"]),
        "price_paid": payment["amount_in_cents"] / 100,
        "statement_id": statement["id"],
    }
