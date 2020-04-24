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
    ) in user.chargifysubscription_set.all():  # should we filter on certain states ?
        subscription_id = subscription.uuid
        statements = subscription.chargify_helper.get_subscription_statements(
            subscription_id
        )
        for statement in statements:
            try:
                invoice_data = extract_invoice_data(statement)
            except UncoveredInvoicing:
                continue

            if invoice_data:
                invoices.append(invoice_data)

    return invoices


def extract_invoice_data(statement):
    """
    Given a Chargify statement, extract necessary invoice info : price, product, payment date.

    """
    if not statement.get("settled_at") or not (statement.get("total_in_cents", 0) > 0):
        # if statement is not settled (i.e. is unpaid) or has no billed amount, ignore it
        return None

    charges = [t for t in statement["transactions"] if t["type"] == "Charge"]

    statement_id = statement["id"]
    if len(charges) > 1:
        logger.info(f"More than one charge for {statement_id}")
        raise UncoveredInvoicing()

    charge = charges[0]

    if charge["kind"] != "baseline" or not charge["success"]:
        logger.info(f"Unhandled charge in statement {statement_id}")
        raise UncoveredInvoicing()

    return {
        "product": charge["item_name"],
        "payment_date": parse(statement["settled_at"]),
        "price_paid": statement["total_in_cents"] / 100,
        "statement_id": statement["id"],
    }
