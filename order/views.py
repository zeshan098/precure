# -*- coding: utf-8 -*-
import sys
import json
from io import BytesIO
import datetime
from django.shortcuts import render, redirect
from random import choice
from string import ascii_lowercase, digits
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage  
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import connection
from django.contrib.auth.models import User as DjangoUser 
from users.models import StaffUser as User, StaffUser 
from buyer.models import BuyerInquiry, BuyerEmails
from order.models import OrderInfo 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
# from .utils import render_to_pdf  
from django.template.loader import get_template
from xhtml2pdf import pisa 

# Create your views here.
@login_required(login_url='/users/login')
def create_order(request):
    
    today = datetime.datetime.now() 
    
    if request.is_ajax(): 
        title = request.POST.get('title') 
        reference_no = request.POST.get('reference_no') 
        to_email = request.POST.getlist('buyer_emails')   
        quotation = request.POST.get('quotation')   
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')  
        total = request.POST.get('total')  
        notes = request.POST.get('notes')   
        
        OrderInfo.objects.create(reference_no=reference_no,
                                     quotation=quotation, sub_total=sub_total,
                                     discount=discount,total_amount=total, 
                                     notes=notes,created_by=request.user.id,updated_by=request.user.id, 
                                     status='1')
        try:
            buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
            staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id) 
            email = BuyerEmails.objects.filter(buyer_id=staff_user.id) 
        except:
            print("not good")
        if staff_user.address == None: 
            staff_address = ''
        else:
            staff_address = staff_user.address
        context = {
            'title':title,
            'name':staff_user.buyer_vendor_name,
            'email':email,
            'address': staff_address,
            'location':staff_user.location,
            'phone_no':staff_user.phone_no,
            "ref_no":reference_no,
            "today": today,
            'sub_total':sub_total,
            'discount':discount,
            'total':total,
            'quotation': quotation,
            'notes':notes,
        }
        template = get_template('admin/order/pdf/invoice.html')
        html  = template.render(context)
        result = BytesIO() 
        destination = 'media/'
        filename = f'{today:%S%M%H%d%m%Y}' + '.pdf'
        file = open(destination + filename, "w+b")
        pdf = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
        # pdf = render_to_pdf('admin/order/pdf/invoice.html', context)
        html_content = render_to_string("admin/order/email/order_email.html", {'ref_no':reference_no, 
                'quotation':quotation,  'sub_total':sub_total, 'discount': discount, 'total':total,
                'notes':notes }) 
        msg = EmailMessage("Order Form",html_content,"operations@procurehero.com",to_email)
        msg.content_subtype = 'html'  
        msg.attach_file('media/'+filename)    
        msg.send()  
        print("send mail")
        message = "success"
        return HttpResponse(message)
     
        
    return render(request, 'admin/order/create_order.html',{
        
    })


@login_required(login_url='/users/login')
def order_list(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select ino.id,ino.reference_no,  TO_CHAR(ino.creation_datetime, 'DD-MM-YYYY') 
                        from order_orderinfo ino 
                        order by ino.creation_datetime DESC   """)
    order_list = cursor.fetchall() 

    return render(request, 'admin/order/order_list.html',{
        'order_list':order_list 
    })

# def GeneratePdf(request):
#         context = {
#             "c":"c",
#             'f':"f",

#         }
#         #getting the template
#         pdf = render_to_pdf('admin/order/pdf/invoice.html', context)
         
#          #rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')