import random

from django.core.cache import cache
from django.urls import reverse

from rate.models import Rate


def test_rate_list(client):
    url = reverse('rate:list')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_csv(client):
    url = reverse('rate:download-csv')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'text/csv')


def test_rate_xlsx(client):
    url = reverse('rate:download-xlsx')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'application/vnd'
                                                                 '.openxmlformats-officedocument.spreadsheetml.sheet')


def test_latest_rates(client):
    url = reverse('rate:latest-rates')
    cache.clear()
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name == ['latest-rates.html']


def test_edit_rate_get_form(admin_client):
    pk = Rate.objects.order_by('?').last().pk
    url = reverse('rate:edit', args=(pk,))
    response = admin_client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['form'].base_fields) == 4


def test_edit_rate_save_empty_form(admin_client):
    obj = Rate.objects.order_by('?').last()
    url = reverse('rate:edit', args=(obj.id,))
    response = admin_client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 4
    assert errors['rate'] == ['This field is required.']
    assert errors['source'] == ['This field is required.']
    assert errors['currency_type'] == ['This field is required.']
    assert errors['rate_type'] == ['This field is required.']


def test_edit_rate_save_form(admin_client):
    count_objects = Rate.objects.count()
    pk = random.randint(1, count_objects)
    url = reverse('rate:edit', args=(pk,))
    data = {
        'rate': random.randint(20, 30),
        'source': random.randint(1, 6),
        'currency_type': random.randint(1, 2),
        'rate_type': random.randint(1, 2),
    }
    response = admin_client.post(url, data)
    assert response.wsgi_request.user.is_superuser is True
    assert response.status_code == 302
    obj = Rate.objects.get(id=pk)
    assert obj.rate == data['rate']
    assert obj.source == data['source']
    assert obj.currency_type == data['currency_type']
    assert obj.rate_type == data['rate_type']


def test_delete_rate(admin_client):
    initial_count = Rate.objects.count()
    pk = random.randint(1, initial_count)
    url = reverse('rate:delete', args=(pk,))
    response = admin_client.get(url)
    assert response.wsgi_request.user.is_superuser is True
    assert response.status_code == 302
    assert response.url == reverse('rate:list')
    assert Rate.objects.count() == initial_count - 1


def test_delete_rate_with_common_user(client, django_user_model):
    username = 'user1'
    password = 'pass'
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    initial_count = Rate.objects.count()
    pk = random.randint(1, initial_count)
    url = reverse('rate:delete', args=(pk,))
    response = client.get(url)
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.is_superuser is False
    assert response.status_code == 403
    assert response.content == b'<h1>403 Forbidden</h1>'
    assert Rate.objects.count() == initial_count


def test_edit_rate_with_common_user(client, django_user_model):
    username = 'user1'
    password = 'pass'
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    objects_count = Rate.objects.count()
    pk = random.randint(1, objects_count)
    url = reverse('rate:edit', args=(pk,))
    response = client.get(url)
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.is_superuser is False
    assert response.status_code == 403
    assert response.content == b'<h1>403 Forbidden</h1>'
