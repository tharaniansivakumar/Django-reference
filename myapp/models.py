# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class sample(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

    class Meta:
        db_table = "detail"


class product(models.Model):
    p_id = models.IntegerField(primary_key=True)
    p_name = models.CharField(max_length=50)
    p_brand = models.CharField(max_length=40)
    p_quantity = models.IntegerField()
    p_price = models.IntegerField()
    p_description = models.CharField(max_length=50)

    class Meta:
        db_table = "product"


class place(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    address = models.CharField(max_length=20)

    class Meta:
        db_table = "place"


class restaurant(models.Model):
    place = models.OneToOneField(place, primary_key=True, on_delete=models.CASCADE)
    juice = models.BooleanField()

    class Meta:
        db_table = "restaurant"


class waiter(models.Model):
    restaurant = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class meta:
        db_table = "waiter"


class Member(models.Model):
    m_id = models.IntegerField(primary_key=True)
    m_username = models.CharField(max_length=50)
    m_password = models.CharField(max_length=100)

    class Meta:
        db_table = "member"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=40)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.first_name


class Thing(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()

    class Meta:
        db_table = "thing"

    def __str__(self):
        return self.product_name


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    order_date = models.DateField()

    class Meta:
        db_table = "sale"


class Saledetail(models.Model):
    saledetail_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale)
    product = models.ForeignKey(Thing)
    price = models.IntegerField()

    class Meta:
        db_table = "saledetail"


class CsvDetail(models.Model):
    roll = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    mail = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)


#
# class Message(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     msg = models.TextField()
#     time = models.TextField(default=None)
#
#     class Meta:
#         db_table = "message"


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    mail = models.TextField()
    image = models.TextField(default=None)

    class Meta:
        db_table = "project"


class Imagetable(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.TextField()

    class Meta:
        db_table = "imagetable"


class Student(models.Model):
    name = models.CharField(max_length=26)

    class Meta:
        db_table = "student"


class Teacher(models.Model):
    name = models.CharField(max_length=26)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "teacher"


class tharani(models.Model):
    first_Name = models.CharField(max_length=255),
    last_name = models.CharField(max_length=255),

    class Meta:
        db_table = "tharani"
