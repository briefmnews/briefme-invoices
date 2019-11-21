import pytest

from briefme_invoices.views import DisplayInvoiceView

pytestmark = pytest.mark.django_db


class TestDisplayInvoiceView:
    def test_view_works_with_existing_invoice(self, request_builder, invoice):
        # GIVEN
        request = request_builder.get(user=invoice.user)

        # WHEN
        response = DisplayInvoiceView.as_view()(request, statement_id=invoice.statement_id)

        # THEN
        assert response.context_data["object"].id == invoice.id
        assert response.status_code == 200
        assert response.template_name[0] == 'invoices/detail.html'
