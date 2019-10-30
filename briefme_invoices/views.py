from django.views.generic import TemplateView, UpdateView, DetailView
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings
from django.http import Http404

from .models import Invoice, InvoiceMismatch
from .forms import UpdateInvoicingInfoForm
from .utils import get_invoices_data_for, UncoveredInvoicing


class DisplayInvoiceView(LoginRequiredMixin, DetailView):
    """Given a Chargify statement, get (or create) an invoice object and display it."""

    template_name = "invoices/detail.html"

    def get_object(self, queryset=None):
        user = self.request.user
        statement_id = self.kwargs.get("statement_id")
        try:
            return Invoice.objects.get_or_create_from_chargify(statement_id, user)
        except InvoiceMismatch:
            raise Http404


class DownloadInvoiceView(WeasyTemplateResponseMixin, DisplayInvoiceView):
    """Render a PDF version of an invoice, out of HTML."""

    pdf_attachment = settings.INVOICES_PDF_ATTACHMENT

    def get_pdf_filename(self):
        sequence = self.object.get_sequence()
        return f"facture-{sequence}.pdf"


class InvoicesListView(LoginRequiredMixin, TemplateView):
    """Display a list of downloadable paid invoices."""

    template_name = "invoices/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context["invoices"] = get_invoices_data_for(user)
        except UncoveredInvoicing:
            messages.error(
                self.request,
                "Une erreur est survenue. Merci de bien vouloir nous contacter.",
            )
        return context


class UpdateInvoicingInfoView(LoginRequiredMixin, UpdateView):
    """Update billing information."""

    template_name = "invoices/update_info.html"
    form_class = UpdateInvoicingInfoForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(
            self.request, "Vos informations de facturation ont été mises à jour."
        )
        return reverse("invoices:update_info")
