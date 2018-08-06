# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
import time
@shared_task()
def add():
    time.sleep(15)
    for i in range(1,1000):
        print("i am tharanian"+""+str(i))