import logging
from dateutil.parser import parse

from briefme_core.subscription.chargify import ChargifyHelper, PRODUCTS


logger = logging.getLogger(__name__)


class UncoveredInvoicing(Exception):
    pass


def get_invoices_data_for(user):
    """For a given user, generate a list of dict containing invoices information."""

    invoices = []

    chargify = ChargifyHelper()

    chargify_user = chargify.get_customer_by_reference(user.pk)

    for subscription in chargify.get_subscriptions_by_customer_id(
        chargify_user["id"]
    ):  # should we filter on certain states ?
        subscription = subscription["subscription"]
        transactions = chargify.get_subscription_transactions(subscription["id"])
        for transaction in transactions:
            try:
                invoice_data = extract_invoice_data(transaction)
            except UncoveredInvoicing:
                continue

            if invoice_data:
                invoices.append(invoice_data)

    return invoices


def extract_invoice_data(transaction):
    """
    Given a Chargify transaction, extract necessary invoice info : price, product, payment date.

    """
    if not (transaction.get("amount_in_cents", 0) > 0):
        # if transaction is not settled (i.e. is unpaid) or has no billed amount, ignore it
        return None

    transaction_id = transaction["id"]

    if transaction["type"] != "Payment" or not transaction["success"]:
        logger.info(f"Unhandled charge in transaction {transaction_id}")
        raise UncoveredInvoicing()

    product = PRODUCTS.get_by_id(transaction["product_id"], "")
    if product:
        product_name = product.get("name", "")
    else:
        product_name = ""

    return {
        "product": product_name,
        "payment_date": parse(transaction["created_at"]),
        "price_paid": transaction["amount_in_cents"] / 100,
        "transaction_id": transaction["id"],
    }
