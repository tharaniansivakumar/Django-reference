# -*- coding: utf-8 -*-

from django.conf.urls import url

from myapp.views import index, detail, indexs, details, register, login, logout, reset_password, mail_verification, \
    forgot_password, csv_open, csv_read, total_price, total, insert, lout, xml_read, xml_zeep, xml_fetch, image_store, \
    image_fetch, pdf_generator, excel_rec, html_pdf, query_join
from myapp import views

urlpatterns =[
     #url(r'^myapp$', indexs, name="index"),
     #url(r'^myapp/(?P<id>[\w]+)/$', indexs, name="index"),
    #url(r'^myapp/(?P<name>[\w]+)/$', details, name="details"),
     #url(r'^myapp/register$', register, name="register"),
     #url(r'^myapp/login$', login, name="login"),
     #url(r'^myapp/logout$', logout, name="logout"),
     #url(r'^myapp/reset$',reset_password,name="reset"),
    #url(r'^myapp/forgot$', forgot_password, name="forgot"),
     #url(r'^myapp/mail/(?P<name>.*)/(?P<id>[\w]+)$', mail_verification, name="mail"),
    url(r'^csvread', csv_open, name="csvread"),
    url(r'^csvfetch', csv_read, name="csvfetch"),
    url(r'^price', total_price, name="price"),
    url(r'^total', total, name="total"),
    url(r'^insert', insert, name="insert"),
    url(r'^login', login, name="login"),
    url(r'^lout', lout, name="lout"),
    url(r'^xml$', xml_read, name="xml"),
    url(r'^zeep', xml_zeep, name="zeep"),
    url(r'^xml_fetch$', xml_fetch, name="xml_fetch"),
    url(r'^img_load',image_store,name="img_load"),
    url(r'^img_fetch', image_fetch, name="img_fetch"),
    url(r'^pdf$', pdf_generator, name="pdf"),
    url(r'^excel', excel_rec, name="excel"),
    url(r'^pdfcheck', html_pdf, name="pdfcheck"),
    url(r'^query', query_join, name="query"),

]