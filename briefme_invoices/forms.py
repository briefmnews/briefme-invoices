from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model


class UpdateInvoicingInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "organization",
            "address",
            "zip",
            "city",
            "country",
        ]
        required = [
            "address",
            "zip",
            "city",
            "country",
        ]

    def clean(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get("last_name")
        first_name = cleaned_data.get("first_name")
        organization = cleaned_data.get("organization")

        if not (organization or (first_name and last_name)):
            raise forms.ValidationError(
                "Le nom et prénom ou l'organisation doivent être renseignés."
            )
