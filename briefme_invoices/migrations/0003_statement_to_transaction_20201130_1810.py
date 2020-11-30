from django.db import migrations


def move_statement_to_transaction(apps, schema_editor):
    Invoice = apps.get_model("briefme_invoices", "Invoice")
    for invoice in Invoice.objects.all():
        if invoice.raw_statement:
            payment = [
                p
                for p in invoice.raw_statement["transactions"]
                if p["type"] == "Payment" and p["success"] == True
            ]
            if payment:
                invoice.raw_transaction = payment[0]
                invoice.transaction_id = invoice.raw_transaction["id"]
                invoice.save()


class Migration(migrations.Migration):

    dependencies = [
        ("briefme_invoices", "0002_auto_20201130_1808"),
    ]

    operations = [migrations.RunPython(move_statement_to_transaction)]
