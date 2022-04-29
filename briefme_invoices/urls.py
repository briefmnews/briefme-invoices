from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    InvoicesListView,
    UpdateInvoicingInfoView,
    DisplayInvoiceView,
    DownloadInvoiceView,
)


app_name = "invoices"


urlpatterns = [
    path("", InvoicesListView.as_view(), name="list"),
    path("informations/", UpdateInvoicingInfoView.as_view(), name="update_info"),
    path(
        "<int:transaction_id>/",
        staff_member_required(DisplayInvoiceView.as_view()),
        name="detail",
    ),
    path("<int:transaction_id>/download/", DownloadInvoiceView.as_view(), name="download"),
]
