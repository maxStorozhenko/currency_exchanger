import csv

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView, View

from rate.models import Rate
from rate.selectors import get_latest_rates
from rate.utils import display

import xlsxwriter


class RateList(ListView):
    paginate_by = 24
    queryset = Rate.objects.all()
    template_name = 'rate-list.html'


class RateDownloadCSV(View):
    HEADERS = (
        'id',
        'created',
        'rate',
        'source',
        'currency_type',
        'rate_type',
    )

    queryset = Rate.objects.all().iterator()

    def get(self, request):
        response = self.get_response

        writer = csv.writer(response)
        writer.writerow(self.__class__.HEADERS)

        for rate in self.queryset:

            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))

            writer.writerow(values)
        return response

    @property
    def get_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        return response


class RateDownloadXLSX(View):
    HEADERS = (
        'id',
        'created',
        'rate',
        'source',
        'currency_type',
        'rate_type',
    )

    queryset = Rate.objects.all()

    def get(self, request):
        response = self.get_response

        book = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet = book.add_worksheet()

        for i, column in enumerate(self.__class__.HEADERS):
            sheet.write(0, i, column)

        for i, rate in enumerate(self.queryset, start=1):
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))

            for j, value in enumerate(values):
                sheet.write(i, j, value)

        book.close()

        return response

    @property
    def get_response(self):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=rates.xlsx"
        return response


class LatestRatesView(TemplateView):
    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_latest_rates()
        return context


def superuser_check(user):
    return user.is_superuser


class EditRate(UserPassesTestMixin, UpdateView):
    template_name = 'edit-rate.html'
    model = Rate
    fields = 'rate', 'source', 'currency_type', 'rate_type'
    success_url = reverse_lazy('rate:list')

    def test_func(self):
        return self.request.user.is_superuser


class DeleteRate(UserPassesTestMixin, DeleteView):
    model = Rate
    success_url = reverse_lazy('rate:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser
