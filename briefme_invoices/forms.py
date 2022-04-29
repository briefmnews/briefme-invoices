from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .countries import COUNTRIES


class UpdateInvoicingInfoForm(ModelForm):
    country = forms.ChoiceField(
        required=True,
        label="Pays",
        choices=COUNTRIES,
        widget=forms.Select(
            attrs={
                "class": "input-inner cursor cursor-pointer close overflow-hidden border border-grey-light bg-grey-verylight pt-8px pb-12px px-10px rounded-6 relative transition duration-300 ease-in-out w-full text-black-light h-48px"
            }
        ),
    )

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
