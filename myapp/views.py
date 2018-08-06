# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from PyPDF2.pdf import BytesIO
from django.template.loader import get_template

import dicttoxml as dicttoxml
import xlwt
import zeep
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
import json

from weasyprint import HTML
from xhtml2pdf import pisa

from firstproject.settings import SALT_KEY, PROJECT
from myapp.tasks import add
from .models import *
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
import uuid
import csv
from django.db import connection
from rest_framework.decorators import api_view
import xmltodict
import base64
from reportlab.pdfgen import canvas


# Create your views here.

def succes(di):
    dic = dict()
    dic['content'] = di
    d = {}
    d['status_code'] = 200
    d['sys-msg'] = ""
    d['error'] = "no error"
    d['message'] = "validated successfully"
    dic['response'] = d
    return dic


def failure():
    dic = dict()
    dic['content'] = "no content found"
    d = {}
    d['status_code'] = 400
    d['sys-msg'] = "compiled"
    d['error'] = "error"
    d['message'] = "content not found"
    dic['response'] = d
    return dic


@api_view(['GET'])
def detail(request):
    result = list(sample.objects.all().values())
    d = failure()
    return JsonResponse(d)


@api_view(['POST'])
def index(request):
    js = json.loads(request.body)
    obj = sample()
    obj.email = js['email']
    obj.firstname = js['firstname']
    obj.lastname = js['lastname']
    obj.save()
    return JsonResponse(js, safe=False, status=200)


@api_view(['GET'])
def indexs(request, id=None):
    if (id != None):
        result = list(product.objects.filter(p_id=id).values())
    else:
        result = list(product.objects.all().values())
    return JsonResponse(result, safe=False)


@api_view(['GET'])
def details(request, name=None):
    print name
    if (name != None):
        result = list(product.objects.filter(p_brand=name).values())
    else:
        result = list(product.objects.all().values())
    return JsonResponse(result, safe=False)


@api_view(['POST'])
def register(request):
    js = json.loads(request.body)
    obj = Member()
    obj.m_id = js['id']
    obj.m_username = js['username']
    obj.m_password = make_password(js['password'], salt=SALT_KEY)
    obj.save()
    return HttpResponse("<h2> Registered successfully</h2>")


def login(request):
    js = json.loads(request.body)
    if request.session._session:
        return HttpResponse("<h1> u r already login </h2>")
    else:
        if (Member.objects.filter(m_username=js['username'], m_password=make_password(js['password'], salt=SALT_KEY))):
            request.session["username"] = js['username']
            request.session.set_expiry(12 * 60 * 60)
            return HttpResponse("<h3> lOGIN SUCCESSFULLY</h3>")
        else:
            return HttpResponse("</h4> Invalid username and password</h4>")


@api_view(['GET'])
def logout(request):
    request.session.flush()
    return HttpResponse("<h3> you are logged out </h3>")


@api_view(['POST'])
def reset_password(request):
    j = json.loads(request.body)
    name = request.session['username']
    if name:
        Member.objects.filter(m_username=name).update(m_password=make_password(j['confirm_password'], salt=SALT_KEY))
        return HttpResponse("<h5> password updated successfully<h5>")
    else:
        return HttpResponse("<h4> Invalid User</h4>")


n = uuid.uuid1()
check = n.int


@api_view(['POST'])
def forgot_password(request):
    j = json.loads(request.body)
    request.session.flush()
    request.session['c_id'] = check
    name = j['username']
    e = EmailMessage("hai", "127.0.0.1:8001/project/myapp/mail/" + name + "/" + str(check), to=[name])
    e.send()
    return HttpResponse("<h1> open your gmail<h1>")


def mail_verification(request, name=None, id=None):
    print name
    if check == request.session['c_id']:
        print("valid")
    else:
        print("invalid")
    j = json.loads(request.body)
    val = list(Member.objects.filter(m_username=name).values())
    if (len(val)):
        Member.objects.filter(m_username=name).update(m_password=make_password(j['confirm_password'], salt=SALT_KEY))
        return HttpResponse("<h5> password updated successfully<h5>")
    else:
        return HttpResponse("<h3> Invalid user</h2>")


def csv_open(request):
    with open(os.path.join(PROJECT, 'tharani.csv'), 'r') as op:
        row = []
        di = csv.DictReader(op)
        for i in di:
            ob = CsvDetail()
            ob.mail = i['Mail']
            ob.name = i['Name']
            ob.age = i['Age']
            ob.roll = i['Roll']
            ob.gender = i['Gender']
            ob.save()
            row.append(i)
    return JsonResponse(row, safe=False)


def csv_read(request):
    add.delay()
    with open(os.path.join(PROJECT, "output.csv"), 'w+') as op:
        obj = list(CsvDetail.objects.values().all())
        # return JsonResponse(obj,safe=False)
        head = ['mail', 'age', 'gender', 'roll', 'name']
        di = csv.DictWriter(op, fieldnames=head)
        di.writeheader()
        di.writerows(obj)
        res = HttpResponse(op, content_type='application/force-download')
        res['Content-Disposition'] = 'attachment;filename="datas.csv"'
        return res


def total_price(request):
    val = " select c.first_name,p.product_name,sum(sd.price*p.product_price) as total_price  from customer c join sale s on c.customer_id=s.customer_id join saledetail sd on s.sale_id=sd.sale_id join thing p on sd.product_id=p.product_id group by c.first_name,p.product_name;"
    with connection.cursor() as cursor:
        cursor.execute(val)
        rows = cursor.fetchall()
        li = []
        for i in rows:
            di = dict()
            di["first_aname"] = i[0]
            di["product_name"] = i[1]
            di["total_price"] = int(i[2])
            li.append(di)
        print(li)
    return JsonResponse(li, safe=False)


def total(request):
    saledetail = list(Saledetail.objects.all().values())
    main = []
    for sal in saledetail:
        dic = {}
        f = 0
        sale = list(Sale.objects.filter(sale_id=sal['sale_id']).values())[0]
        prod = list(Thing.objects.filter(product_id=sal['product_id']).values())[0]
        customer = list(Customer.objects.filter(customer_id=sale['customer_id']).values())[0]
        dic["product_name"] = prod["product_name"]
        dic["firstname"] = customer["first_name"]
        dic["amount"] = int(sal['price']) * int(prod['product_price'])
        for i in range(len(main)):
            if dic["product_name"] == main[i]["product_name"] and dic["firstname"] == main[i]["firstname"]:
                main[i]['amount'] += dic["amount"]
                f = 1
                break
        if f != 1:
            main.append(dic)
    return JsonResponse(main, safe=False)


def insert(request):
    f = 0
    if 'username' in request.session:
        if 'msg' in request.POST:
            name = request.session['username']
            msg = request.POST.get('msg')
            # request.POST['name'].value=None
            print(msg)
            t = datetime.datetime.now().time()
            tme = str(t.hour) + ":" + str(t.minute)

            m = Message()
            m.name = name
            m.msg = msg
            m.time = tme
            m.save()

        ob = list(Message.objects.all().values())
        ob.reverse()
        sample = {"name": ob}
        return render(request, 'index.html', sample)
    else:
        return render(request, 'login.html', {})


def login(request):
    try:
        if 'user' in request.POST:
            username = request.POST.get('user')
            password = request.POST.get('pass')
            if (Member.objects.filter(m_username=username, m_password=password)):
                request.session["username"] = username
                print(username)
                sample = {"temp": "http://192.168.1.117:8000/project/insert"}
                # request.sesion.set_expiry(12 * 60 * 60)
                return render(request, 'index.html', {})
        else:
            return render(request, 'login.html', {})
    except Exception as e:
        return HttpResponse(e)


def lout(request):
    del request.session['username']
    return render(request, 'login.html', {})


def xml_read(request):
    # with open(os.path.join(PROJECT, "demo.xml"), 'r') as op:
    x = request.body.decode('utf-8')
    doc = dict(xmltodict.parse(x))
    print(type(doc))
    x = doc['content']
    d = dict(x)
    li = []
    del d['#text']
    for j in range(len(d['name'])):
        dic = {}
        for i in d:
            dic[i] = d[i][j]
            print(d[i][j])
        li.append(dic)
    for i in li:
        prd = Project()
        prd.name = i['name']
        prd.id = i['id']
        prd.mail = i['mail']
        prd.save()
    return JsonResponse(li, safe=False)


def xml_fetch(request):
    add.delay()
    li = list(Project.objects.all().values())
    xml = dicttoxml.dicttoxml(li)
    return HttpResponse(xml)


def xml_zeep(request):
    wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
    client = zeep.Client(wsdl=wsdl)
    print(client.service.Method1('Zeep', 'is cool'))
    print(client)
    return HttpResponse("success")


def image_store(request):
    fil = request.FILES['file']
    file_system = FileSystemStorage()
    filePath = "media/temp/" + str(fil)
    file = file_system.save(filePath, fil)
    print(file)
    with open(filePath, 'r') as imgFile:
        s = base64.b64encode(imgFile.read())
        os.remove(filePath)
        img = Imagetable()
        img.image = s;
        img.save()
    return HttpResponse("SUCCESS")


def image_fetch(request):
    img = list(Imagetable.objects.all().values())
    image = base64.b64decode(img[0]['image'])
    return HttpResponse(image, content_type="image/png")


def pdf_generator(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "attachement;filename=tharani.pdf"
    obj = list(Message.objects.all().values())
    p = canvas.Canvas(response)
    k = 800
    for i in range(len(obj)):
        val = obj[i]['name']
        c = obj[i]['msg']
        t = obj[i]['time']
        p.drawString(100, k, "Name: " + val)
        p.drawString(100, k - 20, "Message:" + c)
        p.drawString(100, k - 40, "Time :" + t)
        k = k - 80
        if (k <= 0):
            print(k)
            p.showPage()
            k = 800
    p.save()
    return response


def excel_rec(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = "attachment; filename=message.xls"

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Message')
    wm = wb.add_sheet('customer')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    column = ['id', 'name', 'message', 'time']
    col = ['id', 'name', 'last_name']
    for col_num in range(len(column)):
        ws.write(row_num, col_num, column[col_num], font_style)

    for col_no in range(len(col)):
        wm.write(row_num, col_no, col[col_no], font_style)
    font_style = xlwt.XFStyle()

    rows = Message.objects.all().values_list('id', 'name', 'msg', 'time')
    print rows
    r = Customer.objects.all().values_list('customer_id', 'first_name', 'last_name')
    print(r)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num = 0
    for i in r:
        row_num += 1
        for cl in range(len(i)):
            wm.write(row_num, cl, i[cl], font_style)
    wb.save(response)
    return response


#
def render(path=None, params=None):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)


def html_pdf(request):
    m = list(Message.objects.all().values())
    val = {"content": m}
    return render('demo.html', val)
