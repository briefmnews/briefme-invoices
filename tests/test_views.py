import pytest

from briefme_invoices.views import (
    DownloadInvoiceView,
    DisplayInvoiceView,
    UpdateInvoicingInfoView,
)

pytestmark = pytest.mark.django_db


class TestDisplayInvoiceView:
    def test_view_works_with_existing_invoice(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = DisplayInvoiceView.as_view()(
            request, statement_id=invoice.statement_id
        )

        # THEN
        assert response.context_data["object"].id == invoice.id
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/detail.html"


class TestDownloadInvoiceView:
    def test_view_works_properly(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = DownloadInvoiceView.as_view()(
            request, statement_id=invoice.statement_id
        )

        # THEN
        assert response.context_data["object"].id == invoice.id
        assert response.status_code == 200
        assert response.template_name[0] == "invoices/detail.html"


class TestUpdateInvoicingInfoView:
    def test_view_works_properly(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = UpdateInvoicingInfoView.as_view()(
            request, statement_id=invoice.statement_id
        )

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
        response = UpdateInvoicingInfoView.as_view()(
            request, statement_id=invoice.statement_id
        )

        # THEN
        assert response.status_code == 302
        assert response.url == "/informations/"
        assert invoice.user.first_name == "New first name"
