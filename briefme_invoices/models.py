from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from model_utils.models import TimeStampedModel

from subscription.chargify import ChargifyHelper

from .constants import EU_COUNTRIES
from .utils import extract_invoice_data


class InvoiceMismatch(Exception):
    pass


class InvoiceManager(models.Manager):
    def get_or_create_from_chargify(self, statement_id, user):
        try:
            invoice = self.get_queryset().get(statement_id=statement_id, user=user)
        except self.model.DoesNotExist:
            invoice = self.create_from_chargify(statement_id, user)

        return invoice

    def create_from_chargify(self, statement_id, user):
        chargify = ChargifyHelper()
        statement = chargify.get_statement(statement_id)

        # ensure requested statement belongs to the user
        subscription_id = statement["subscription_id"]
        if not user.subscription_set.filter(
            chargifysubscription__uuid=subscription_id
        ).exists():
            raise InvoiceMismatch()

        invoice = self.model(raw_statement=statement, user=user)
        invoice.save()

        return invoice


class Invoice(TimeStampedModel):
    statement_id = models.CharField(max_length=100, unique=True)
    raw_statement = JSONField()
    billing_info = JSONField()
    vat_rate = models.FloatField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=False, null=True
    )
    objects = InvoiceManager()

    @cached_property
    def extracted_data(self):
        """For convenience, locally cache relevant data from raw statement."""
        return extract_invoice_data(self.raw_statement)

    @property
    def price_paid(self):
        return self.extracted_data["price_paid"]

    @property
    def product_name(self):
        return self.extracted_data["product"]

    @property
    def payment_date(self):
        return self.extracted_data["payment_date"]

    def get_sequence(self):
        """Generate unique sequence {INVOICES_PREFIX}-0000001."""
        left_filled_pk = str(self.pk).zfill(10)
        return f"{settings.INVOICES_PREFIX}-{left_filled_pk}"

    @property
    def price_excluding_vat(self):
        return self.price_paid / (1 + self.vat_rate / 100)

    @property
    def vat_amount(self):
        return self.price_paid - self.price_excluding_vat

    def _get_vat_rate(self):
        """Generate VAT rate according to user's address."""
        if self.user.country in EU_COUNTRIES:
            rate = 2.1
        else:
            rate = 0
        return rate

    def _serialize_billing_info(self):
        return {
            "last_name": self.user.last_name,
            "first_name": self.user.first_name,
            "organization": self.user.organization,
            "email": self.user.email,
            "address": self.user.address,
            "zip": self.user.zip,
            "city": self.user.city,
            "country": self.user.country,
        }

    def save(self, *args, **kwargs):
        self.statement_id = self.raw_statement["id"]
        self.billing_info = self._serialize_billing_info()
        self.vat_rate = self._get_vat_rate()
        super().save(*args, **kwargs)
