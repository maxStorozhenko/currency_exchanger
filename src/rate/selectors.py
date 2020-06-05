import hashlib

from django.core.cache import cache

import rate.model_choices as mch
from rate.models import Rate


def rate_cache_key(source, currency, rate_type) -> str:
    return hashlib.md5(
        f'{source}_{currency}_{rate_type}'.encode()
    ).hexdigest()


def get_latest_rates() -> list:
    object_list = []

    for source in mch.SOURCE_CHOICES:  # source
        source = source[0]
        for currency in mch.CURRENCY_TYPE_CHOICES:  # currency_type
            currency = currency[0]
            for rate_type in mch.RATE_TYPE_CHOICES:  # rate_type
                rate_type = rate_type[0]

                key = rate_cache_key(source, currency, rate_type)
                cached_rate = cache.get(key)

                if cached_rate is None:
                    rate = Rate.objects.filter(source=source,
                                               currency_type=currency,
                                               rate_type=rate_type).latest('created')
                    if rate is not None:
                        cache.set(key, rate, 1800)
                        object_list.append(rate)
                else:
                    object_list.append(cached_rate)

    return object_list
