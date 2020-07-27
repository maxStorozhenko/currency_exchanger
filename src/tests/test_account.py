from account.models import Contact

from django.conf import settings
from django.core import mail
from django.urls import reverse


def test_contact_us_get_form(client):
    url = reverse('account:contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_empty_payload(client):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0
    url = reverse('account:contact-us')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 3
    assert errors['email_from'] == ['This field is required.']
    assert errors['subject'] == ['This field is required.']
    assert errors['message'] == ['This field is required.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_incorrect_email(client):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0
    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail',
        'subject': 'hello world',
        'message': 'hello world',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email_from'] == ['Enter a valid email address.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_correct_payload(client, fake):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0
    email = fake.email()
    url = reverse('account:contact-us')
    payload = {
        'email_from': email,
        'subject': 'hello world',
        'message': 'hello world',
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert Contact.objects.count() == initial_count + 1
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == payload['subject']
    assert email.body == payload['message']
    assert email.from_email == payload['email_from']
    assert email.to == [settings.DEFAULT_FROM_EMAIL]


def test_login_get_form(client):
    url = reverse('account:login')
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name == ['registration/login.html']


def test_login_empty_fields(client):
    url = reverse('account:login')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 2
    assert errors['username'] == ['This field is required.']
    assert errors['password'] == ['This field is required.']


def test_login_incorrect_data(client):
    url = reverse('account:login')
    payload = {
        'username': 'admin',
        'password': '123456',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['__all__'] == ['Please enter a correct username and password. Note that both fields may be '
                                 'case-sensitive.']


def test_login_correct_data(admin_client):
    url = reverse('account:login')
    payload = {
        'username': 'admin',
        'password': 'password',
    }
    response = admin_client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_superuser is True
    assert response.wsgi_request.user.username == 'admin'
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.id == 1
    assert response.url == reverse('index')


def test_logout(admin_client):
    url = reverse('account:logout')
    response = admin_client.get(url)
    assert response.wsgi_request.user.is_authenticated is False
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_signup_form(client, fake):
    url = reverse('account:sign-up')
    email = fake.email()
    password = fake.word()
    payload = {
        'email': email,
        'password1': password,
        'password2': password + 'wrong',
    }

    # passwords doesn't match
    response = client.post(url, payload)
    assert response.status_code == 200

    # correct payload
    payload['password2'] = password
    response = client.post(url, payload)
    assert response.status_code == 302

    # user exists
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email'] == ['User with given email exists!']


def test_change_password_form(client, django_user_model, fake):
    url = reverse('password_change')
    username = fake.name()
    password = 'Notcommonpassword'
    new_password = 'Newcommonpassword'
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # empty payload
    response = client.post(url)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 3
    assert errors['old_password'] == ['This field is required.']
    assert errors['new_password1'] == ['This field is required.']
    assert errors['new_password2'] == ['This field is required.']

    # incorrect password
    payload = {
        'old_password': fake.word(),
        'new_password1': new_password,
        'new_password2': new_password,
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['old_password'] == ['Your old password was entered incorrectly. Please enter it again.']

    # correct payload
    payload['old_password'] = password
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.username == username
