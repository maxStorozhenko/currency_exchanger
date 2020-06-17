from settings.settings import *

SECRET_KEY = 'fp_grwa77&d75%01dziwslea2*t*(fmas6rrbyg+nbr%k$$wr8'
DEBUG = False
ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = CELERY_TASK_ALWAYS_EAGER = True  # run celery tasks as func

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-test.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.outbox'
