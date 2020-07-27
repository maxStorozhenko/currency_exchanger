import os

from django.conf import settings

from rate.models import Rate
from rate.tasks import (
    parse_alfabank,
    parse_credit_dnipro,
    parse_monobank,
    parse_o_o_kharkiv,
    parse_privatbank,
    parse_vkurse,
    )


class Response:
    pass


def test_privatbank(mocker):
    def mock():
        response = Response()
        res = [
            {"ccy": "USD",
             "base_ccy": "UAH",
             "buy": "27.55000",
             "sale": "27.95000"},
            {"ccy": "EUR",
             "base_ccy": "UAH",
             "buy": "31.95000",
             "sale": "32.60000"},
            {"ccy": "RUR",
             "base_ccy": "UAH",
             "buy": "0.36600",
             "sale": "0.39600"},
            {"ccy": "BTC",
             "base_ccy": "USD",
             "buy": "9710.3166",
             "sale": "10732.4552"}
        ]
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + 4


def test_alfabank(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'alfabank.html')
        with open(path) as file:
            res = file.read()
        response = Response()
        response.text = res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_alfabank()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_alfabank()
    assert Rate.objects.count() == initial_rate_count + 4


def test_monobank(mocker):
    def mock():
        response = Response()
        res = [
            {"currencyCodeA": 840,
             "currencyCodeB": 980,
             "date": 1595843408,
             "rateBuy": 27.65,
             "rateSell": 27.933},
            {"currencyCodeA": 978,
             "currencyCodeB": 980,
             "date": 1595844008,
             "rateBuy": 32.15,
             "rateSell": 32.5733},
            {"currencyCodeA": 643,
             "currencyCodeB": 980,
             "date": 1595797808,
             "rateBuy": 0.37,
             "rateSell": 0.395},
            {"currencyCodeA": 978,
             "currencyCodeB": 840,
             "date": 1595830808,
             "rateBuy": 1.159,
             "rateSell": 1.175},
        ]
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + 4


def test_vkurse(mocker):
    def mock():
        response = Response()
        res = {
            "Dollar": {
                "buy": "27.60",
                "sale": "27.80"
            },
            "Euro": {
                "buy": "32.15",
                "sale": "32.40"
            },
            "Rub": {
                "buy": "0.380",
                "sale": "0.388"
            }
        }
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + 4


def test_o_o_kharkiv(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'o_o_kharkiv.html')
        with open(path) as file:
            res = file.read()
        response = Response()
        response.text = res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_o_o_kharkiv()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_o_o_kharkiv()
    assert Rate.objects.count() == initial_rate_count + 4


def test_credit_dnipro(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'credit_dnipro.html')
        with open(path) as file:
            res = file.read()
        response = Response()
        response.text = res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    initial_rate_count = Rate.objects.count()
    parse_credit_dnipro()
    assert Rate.objects.count() == initial_rate_count + 4
    parse_credit_dnipro()
    assert Rate.objects.count() == initial_rate_count + 4
