from celery import shared_task

import lxml.html

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }

    for item in response.json():

        if item['ccy'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['ccy']]

        # buy
        rate = to_decimal(item['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            rate_type=mch.RATE_TYPE_BUY,
            ).last()

        if last is None or last.rate != rate:
            Rate.objects.create(
                rate=rate,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_BUY,
            )

        # sale
        rate = to_decimal(item['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            rate_type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.rate != rate:
            Rate.objects.create(
                rate=rate,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    currency_type_mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
    }

    for item in response.json():
        if item['currencyCodeA'] not in currency_type_mapper:
            continue

        if item['currencyCodeB'] == 980:

            currency_type = currency_type_mapper[item['currencyCodeA']]

            # buy
            rate = to_decimal(item['rateBuy'])

            last = Rate.objects.filter(
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_BUY,
            ).last()

            if last is None or last.rate != rate:
                Rate.objects.create(
                    rate=rate,
                    source=mch.SOURCE_MONOBANK,
                    currency_type=currency_type,
                    rate_type=mch.RATE_TYPE_BUY,
                )

            # sale

            rate = to_decimal(item['rateSell'])

            last = Rate.objects.filter(
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_SALE,
            ).last()

            if last is None or last.rate != rate:
                Rate.objects.create(
                    rate=rate,
                    source=mch.SOURCE_MONOBANK,
                    currency_type=currency_type,
                    rate_type=mch.RATE_TYPE_SALE,
                )


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url).json()

    currency_type_mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }

    for item in response:
        if item not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item]

        # buy
        rate = to_decimal(response[item]['buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            rate_type=mch.RATE_TYPE_BUY,
            ).last()

        if last is None or last.rate != rate:
            Rate.objects.create(
                rate=rate,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_BUY,
            )

        # sale
        rate = to_decimal(response[item]['sale'][:-1])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            rate_type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.rate != rate:
            Rate.objects.create(
                rate=rate,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                rate_type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_o_o_kharkiv():
    url = 'https://opanki-obmenka-kharkov.kursvalut.com/'
    api = requests.get(url)
    html_tree = lxml.html.document_fromstring(api.text)

    # buy
    usd_buy = to_decimal(html_tree.xpath('//*[@id="retail"]/div[2]/div[2]/div/text()')[0])

    last = Rate.objects.filter(
        source=mch.SOURCE_O_O_KHARKIV,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != usd_buy:
        Rate.objects.create(
            source=mch.SOURCE_O_O_KHARKIV,
            rate=usd_buy,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_BUY
        )

    eur_buy = to_decimal(html_tree.xpath('//*[@id="retail"]/div[3]/div[2]/div/text()')[0])

    last = Rate.objects.filter(
        source=mch.SOURCE_O_O_KHARKIV,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != eur_buy:
        Rate.objects.create(
            source=mch.SOURCE_O_O_KHARKIV,
            rate=eur_buy,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_BUY
        )

    # sale
    usd_sale = to_decimal(html_tree.xpath('//*[@id="retail"]/div[2]/div[3]/div/text()')[0])

    last = Rate.objects.filter(
        source=mch.SOURCE_O_O_KHARKIV,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != usd_sale:
        Rate.objects.create(
            source=mch.SOURCE_O_O_KHARKIV,
            rate=usd_sale,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_SALE
        )

    eur_sale = to_decimal(html_tree.xpath('//*[@id="retail"]/div[3]/div[3]/div/text()')[0])

    last = Rate.objects.filter(
        source=mch.SOURCE_O_O_KHARKIV,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != eur_sale:
        Rate.objects.create(
            source=mch.SOURCE_O_O_KHARKIV,
            rate=eur_sale,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_SALE
        )


@shared_task
def parse_credit_dnipro():
    url = 'https://creditdnepr.com.ua/currency'
    api = requests.get(url)
    html_tree = lxml.html.document_fromstring(api.text)

    # buy
    usd_buy = to_decimal(html_tree.xpath('//*[@id="all"]/div/main/main/div/div/div/table/tbody/tr[2]/td[2]')[0].text)

    last = Rate.objects.filter(
        source=mch.SOURCE_CREDIT_DNIPRO,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != usd_buy:
        Rate.objects.create(
            source=mch.SOURCE_CREDIT_DNIPRO,
            rate=usd_buy,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_BUY
        )

    eur_buy = to_decimal(html_tree.xpath('//*[@id="all"]/div/main/main/div/div/div/table/tbody/tr[3]/td[2]')[0].text)

    last = Rate.objects.filter(
        source=mch.SOURCE_CREDIT_DNIPRO,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != eur_buy:
        Rate.objects.create(
            source=mch.SOURCE_CREDIT_DNIPRO,
            rate=eur_buy,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_BUY
        )

    # sale
    usd_sale = to_decimal(html_tree.xpath('//*[@id="all"]/div/main/main/div/div/div/table/tbody/tr[2]/td[3]')[0].text)

    last = Rate.objects.filter(
        source=mch.SOURCE_CREDIT_DNIPRO,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != usd_sale:
        Rate.objects.create(
            source=mch.SOURCE_CREDIT_DNIPRO,
            rate=usd_sale,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_SALE
        )

    eur_sale = to_decimal(html_tree.xpath('//*[@id="all"]/div/main/main/div/div/div/table/tbody/tr[3]/td[3]')[0].text)

    last = Rate.objects.filter(
        source=mch.SOURCE_CREDIT_DNIPRO,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != eur_sale:
        Rate.objects.create(
            source=mch.SOURCE_CREDIT_DNIPRO,
            rate=eur_sale,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_SALE
        )


@shared_task
def parse_alfabank():
    url = 'https://alfabank.ua/currency-exchange'
    api = requests.get(url)
    html_tree = lxml.html.document_fromstring(api.text)

    # buy
    usd_buy = to_decimal(html_tree.xpath(
        '/html/body/main/section[4]/div/div[4]/div[1]/div[2]/div[1]/div[2]/span')[0].text.strip('\t\n '))

    last = Rate.objects.filter(
        source=mch.SOURCE_ALFA_BANK,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != usd_buy:
        Rate.objects.create(
            source=mch.SOURCE_ALFA_BANK,
            rate=usd_buy,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_BUY
        )

    eur_buy = to_decimal(html_tree.xpath(
        '/html/body/main/section[4]/div/div[4]/div[2]/div[2]/div[1]/div[2]/span')[0].text.strip('\t\n ')
                         )

    last = Rate.objects.filter(
        source=mch.SOURCE_ALFA_BANK,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_BUY,
    ).last()

    if last is None or last.rate != eur_buy:
        Rate.objects.create(
            source=mch.SOURCE_ALFA_BANK,
            rate=eur_buy,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_BUY
        )

    # sale
    usd_sale = to_decimal(html_tree.xpath(
        '/html/body/main/section[4]/div/div[4]/div[1]/div[2]/div[2]/div[2]/span')[0].text.strip('\t\n ')
                          )

    last = Rate.objects.filter(
        source=mch.SOURCE_ALFA_BANK,
        currency_type=mch.CURRENCY_TYPE_USD,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != usd_sale:
        Rate.objects.create(
            source=mch.SOURCE_ALFA_BANK,
            rate=usd_sale,
            currency_type=mch.CURRENCY_TYPE_USD,
            rate_type=mch.RATE_TYPE_SALE
        )

    eur_sale = to_decimal(html_tree.xpath(
        '/html/body/main/section[4]/div/div[4]/div[2]/div[2]/div[2]/div[2]/span')[0].text.strip('\t\n ')
                          )

    last = Rate.objects.filter(
        source=mch.SOURCE_ALFA_BANK,
        currency_type=mch.CURRENCY_TYPE_EUR,
        rate_type=mch.RATE_TYPE_SALE,
    ).last()

    if last is None or last.rate != eur_sale:
        Rate.objects.create(
            source=mch.SOURCE_ALFA_BANK,
            rate=eur_sale,
            currency_type=mch.CURRENCY_TYPE_EUR,
            rate_type=mch.RATE_TYPE_SALE
        )


@shared_task
def parse():
    parse_privatbank.delay()
    parse_monobank.delay()
    parse_vkurse.delay()
    parse_o_o_kharkiv.delay()
    parse_credit_dnipro.delay()
    parse_alfabank.delay()
