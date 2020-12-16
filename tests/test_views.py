import pytest

from django.http import Http404

from briefme_invoices.models import InvoiceMismatch
from briefme_invoices.utils import UncoveredInvoicing
from briefme_invoices.views import (
    DownloadInvoiceView,
    DisplayInvoiceView,
    InvoicesListView,
    UpdateInvoicingInfoView,
)

pytestmark = pytest.mark.django_db


class TestDisplayInvoiceView:
    def test_view_works_with_existing_invoice(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = DisplayInvoiceView.as_view()(request, transaction_id=invoice.transaction_id)

        # THEN
        assert response.context_data["object"].id == invoice.id
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/detail.html"

    def test_view_raises_404(self, mocker, request_builder, invoice):
        # GIVEN
        mocker.patch(
            "briefme_invoices.models.InvoiceManager.get_or_create_from_chargify",
            side_effect=InvoiceMismatch(),
        )
        request = request_builder.get(user=invoice.user)

        # WHEN
        with pytest.raises(Http404):
            DisplayInvoiceView.as_view()(request, transaction_id=invoice.transaction_id)


class TestDownloadInvoiceView:
    def test_view_works_properly(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = DownloadInvoiceView.as_view()(request, transaction_id=invoice.transaction_id)

        # THEN
        assert response.context_data["object"].id == invoice.id
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/detail.html"


class TestInvoicesListView:
    def test_view_works_properly(self, mocker, request_builder):
        # GIVEN
        user = mocker.MagicMock()
        user.chargifysubscription_set.filter = True
        request = request_builder.get(user=user)

        # WHEN
        response = InvoicesListView.as_view()(request)

        # THEN
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/list.html"

    def test_view_catch_uncovered_invoicing(self, mocker, request_builder, invoice):
        # GIVEN
        mocker.patch(
            "briefme_invoices.views.get_invoices_data_for", side_effect=UncoveredInvoicing,
        )
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = InvoicesListView.as_view()(request, transaction_id=invoice.transaction_id)

        # THEN
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/list.html"
        assert (
            "Une erreur est survenue. Merci de bien vouloir nous contacter."
            in response.rendered_content
        )


class TestUpdateInvoicingInfoView:
    def test_view_works_properly(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = UpdateInvoicingInfoView.as_view()(request, transaction_id=invoice.transaction_id)

        # THEN
        assert response.context_data["user"] == invoice.user
        assert response.context_data["form"]
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/update_info.html"

    def test_view_works_with_updating_info(self, request_builder, invoice):
        # GIVEN
        form_data = {
            "first_name": "New first name",
            "last_name": invoice.user.last_name,
            "organization": invoice.user.organization,
            "address": invoice.user.address,
            "zip": invoice.user.zip,
            "country": invoice.user.country,
            "city": invoice.user.city,
        }
        request = request_builder.post(user=invoice.user, data=form_data)

        # WHEN
        response = UpdateInvoicingInfoView.as_view()(request, transaction_id=invoice.transaction_id)

        # THEN
        assert response.status_code == 302
        assert response.url == "/informations/"
        assert invoice.user.first_name == "New first name"
