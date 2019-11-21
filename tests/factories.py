import factory
import json

from django.contrib.auth import get_user_model

from briefme_invoices.models import Invoice


class JSONFactory(factory.DictFactory):
    """
    Use with factory.Dict to make JSON strings.
    """
    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)
        return json.dumps(obj)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: "noel{0}@flantier.com".format(n))
    last_name = factory.Sequence(lambda n: "Flantier".format(n))
    first_name = factory.Sequence(lambda n: "Noel{}".format(n))
    city = "Paris"
    country = "FR"
    address = "22 bis rue des Taillandiers"
    zip = 75011
    organization = "Brief.me"
    expertise = "Journalist"
    is_active = True


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    statement_id = factory.Sequence(lambda n: f"{0}{0}{0}{0}{0}")
    raw_statement = factory.Dict({'id': 1}, dict_factory=JSONFactory)
    user = factory.SubFactory(UserFactory)
