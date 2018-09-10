# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
import time
@shared_task()
def add():
    print ("hello")