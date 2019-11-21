import pytest

from briefme_invoices.forms import UpdateInvoicingInfoForm

pytestmark = pytest.mark.django_db


class TestUpdateInvoicingInfoForm:
    def test_form_works_properly(self, user):
        # GIVEN
        form_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization": user.organization,
            "address": user.address,
            "zip": user.zip,
            "country": user.country,
            "city": user.city,
        }

        # WHEN
        form = UpdateInvoicingInfoForm(data=form_data)

        # THEN
        assert form.is_valid()

    def test_form_without_organization_or_user_names(self, user):
        # GIVEN
        form_data = {
            "first_name": "",
            "last_name": "",
            "organization": "",
            "address": user.address,
            "zip": user.zip,
            "country": user.country,
            "city": user.city,
        }

        # WHEN
        form = UpdateInvoicingInfoForm(data=form_data)

        # THEN
        assert not form.is_valid()
        assert "Le nom et prénom ou l'organisation doivent être renseignés." in form.errors["__all__"]

    def test_form_without_organization(self, user):
        # GIVEN
        form_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization": "",
            "address": user.address,
            "zip": user.zip,
            "country": user.country,
            "city": user.city,
        }

        # WHEN
        form = UpdateInvoicingInfoForm(data=form_data)

        # THEN
        assert form.is_valid()

    def test_form_without_user_names(self, user):
        # GIVEN
        form_data = {
            "first_name": "",
            "last_name": "",
            "organization": user.organization,
            "address": user.address,
            "zip": user.zip,
            "country": user.country,
            "city": user.city,
        }

        # WHEN
        form = UpdateInvoicingInfoForm(data=form_data)

        # THEN
        assert form.is_valid()
