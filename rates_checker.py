import os
import sys
import time
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wish_swap.settings')
import django
django.setup()

from wish_swap.rates.models import UsdRate
from wish_swap.settings import RATES_CHECKER_TIMEOUT


if __name__ == '__main__':
    while True:
        rate = UsdRate.objects.first() or UsdRate()
        try:
            rate.update()
            rate.save()
            print('RATES CHECKER: rates updated', flush=True)
        except Exception as e:
            print('RATES CHECKER EXCEPTION: ')
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
        time.sleep(RATES_CHECKER_TIMEOUT)
