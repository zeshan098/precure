import json
from django.shortcuts import render, redirect
from itertools import chain
from random import choice
from string import ascii_lowercase, digits
from django.db import connection
from django.core import serializers
from django.http import HttpResponse, JsonResponse  
from django.contrib.auth.models import User as DjangoUser 
from users.models import StaffUser as User, StaffUser 
from buyer.models import BuyerInquiry, BuyerAttachment, BuyerCategories, BuyerMenufactures, BuyerEmails, BuyerModels 
from django.contrib.auth.decorators import login_required

def buyer_inquiry(request): 

    return render(request, 'web/buyer_inquiry.html',{})

def buyer_category(request):  
    cursor = connection.cursor()
    cursor.execute(""" select id, category_name  from vendor_categories  where status = '1'   """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[1], 'id': obj[1]}) 
    return JsonResponse(list, safe=False)

def buyer_menufacture(request):  
    cursor = connection.cursor()
    cursor.execute(""" select id, menufacture_name  from vendor_menufactures where status = '1'   """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[1], 'id': obj[1]}) 
    return JsonResponse(list, safe=False)

def buyer_model(request):  
    cursor = connection.cursor()
    cursor.execute(""" select id, model_name  from vendor_vendormodels  where status = '1'   """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[1], 'id': obj[1]}) 
    return JsonResponse(list, safe=False)


def generate_random_username(length=11, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        DjangoUser.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except DjangoUser.DoesNotExist:
        return username

def buyer_inquiry_form(request): 
    generated_username = generate_random_username()
    if request.is_ajax():
        buyer_name = request.POST.get('buyer_name')
        company_name = request.POST.get('company_name')
        email = request.POST.getlist('emails')
        phone_no = request.POST.get('phone_no')
        alt_phone_no = request.POST.get('alt_phone_no')
        inquiry_type = request.POST.get('inquiry_type')
        inquiry_des = request.POST.get('inquires')
        category = request.POST.getlist('category')
        menufacture = request.POST.getlist('menufacture') 
        model = request.POST.getlist('model') 
        location = request.POST.get('location') 
        myfile = request.FILES.getlist('file')
        print(category)

        user = DjangoUser.objects.create( email=email, username="procureher" + str(generated_username))
        this_user = User.objects.create(user=user,buyer_vendor_name=buyer_name,role="buyer",status='1',
                                         company_name=company_name, phone_no=phone_no,
                                          alt_phone_no=alt_phone_no, location=location)
       
        buyerinfo = BuyerInquiry.objects.create(inquiry_type=inquiry_type,inquires=inquiry_des,
                                                user=user,status='1')
        for f in myfile: 
            BuyerAttachment.objects.create(buyerinq=buyerinfo,status='1', attachment_file=f )

        # cat_list = category.split (",")  
        # menufacture_list = menufacture.split (",")  
        # model_list = model.split (",")  
        # emails_list = email.split (",")

        for cat in  category: 
            # cat_list = cat.split (",") 
            try:  
                cats = BuyerCategories()
                cats.buyer=this_user
                cats.category_name=cat
                cats.status='1'
                cats.save() 
                print("category Saved")
            except:
                print("not save")
                
        for menufacture in  menufacture: 
            
            # menufacture_list = menufacture.split (",") 
            try:  
                menufacture_lists = BuyerMenufactures()
                menufacture_lists.buyer=this_user
                menufacture_lists.menufacture_name=menufacture
                menufacture_lists.status='1'
                menufacture_lists.save() 
                print("menufacture Saved")
            except:
                print("not save")

        for model in  model:
            
            # model_list = model.split (",")   
            try:  
                b_model = BuyerModels()
                b_model.buyer=this_user
                b_model.model_name=model
                b_model.status='1'
                b_model.save() 
                print("model_name Saved")
            except:
                print("not save")


        for email in  email: 
            # emails_list = email.split (",")
            try:  
                emails = BuyerEmails()
                emails.buyer=this_user
                emails.email_list=email
                emails.status='1'
                emails.save() 
                print("email_list Saved")
            except:
                print("not save")
        message = "success"
        return HttpResponse(message)
    else:
        message = "error"
        return HttpResponse(message)


@login_required(login_url='/users/login')
def buyer_list(request):
    cursor = connection.cursor()
    cursor.execute("""select au.id, us.buyer_vendor_name, us.company_name,au.email,
                      us.phone_no,us.address  from auth_user au
                       inner join users_staffuser us on au.id = us.user_id
                        where us.role = 'buyer'
                       and us.status = '1' """); 
    buyer_list = cursor.fetchall()

    return render(request, 'admin/buyer/buyer_list.html',{
        'buyer_list': buyer_list,
    })

@login_required(login_url='/users/login')    
def add_edit_buyer(request, buyer_id=None):
    generated_username = generate_random_username()
    if buyer_id:
        try:
            buyer_detail = StaffUser.objects.get(user_id=buyer_id)
            buyer_category = BuyerCategories.objects.filter(buyer_id=buyer_detail)
            buyer_menufacture = BuyerMenufactures.objects.filter(buyer_id=buyer_detail)
            buyer_model = BuyerModels.objects.filter(buyer_id=buyer_detail)
            buyer_email = BuyerEmails.objects.filter(buyer_id=buyer_detail) 
        except StaffUser.DoesNotExist:
            buyer_detail = ''

    if request.is_ajax():
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name')
        emails = request.POST.get('emails')
        phone_no = request.POST.get('phone_no')
        alt_phone_no = request.POST.get('alt_phone_no')
        address = request.POST.get('address') 
        website = request.POST.get('website') 
        location = request.POST.get('location') 
        category_list = request.POST.get('category')
        menufacture = request.POST.get('menufacture') 
        model = request.POST.get('model')
        admin_notes = request.POST.get('admin_notes')  

        if buyer_id:
            try:   
                required_vendor = StaffUser.objects.filter(id=buyer_id)
                required_vendor.update(buyer_vendor_name=buyer_vendor_name, 
                                company_name=company_name, phone_no=phone_no, alt_phone_no=alt_phone_no,
                                address=address,website=website,location=location, admin_notes=admin_notes  )
                message = "success"
                return HttpResponse(message)
            except: 
                message = "error"
                return HttpResponse(message)
        else:
            cat_list = category_list.split (",")  
            menufacture_list = menufacture.split (",")  
            model_list = model.split (",")  
            emails_list = emails.split (",")

            try: 
                
                user = DjangoUser.objects.create( email="precure@gmail.com", username="procureher" + str(generated_username))
                this_user =User.objects.create(user=user,buyer_vendor_name=buyer_vendor_name, 
                                    company_name=company_name, phone_no=phone_no, alt_phone_no=alt_phone_no,
                                    address=address,website=website,location=location, 
                                    admin_notes=admin_notes ,role="buyer",status='1',)
     
                for cat in  cat_list: 
                    try:  
                         cats = BuyerCategories()
                         cats.buyer=this_user
                         cats.category_name=cat
                         cats.status='1'
                         cats.save() 
                         print("category Saved")
                    except:
                         print("not save")
                
                for menufacture in  menufacture_list: 
                    try:  
                         menufacture_lists = BuyerMenufactures()
                         menufacture_lists.buyer=this_user
                         menufacture_lists.menufacture_name=menufacture
                         menufacture_lists.status='1'
                         menufacture_lists.save() 
                         print("menufacture Saved")
                    except:
                         print("not save")

                for model in  model_list: 
                    try:  
                         b_model = BuyerModels()
                         b_model.buyer=this_user
                         b_model.model_name=model
                         b_model.status='1'
                         b_model.save() 
                         print("model_name Saved")
                    except:
                         print("not save")


                for email in  emails_list: 
                    try:  
                         emails = BuyerEmails()
                         emails.buyer=this_user
                         emails.email_list=email
                         emails.status='1'
                         emails.save() 
                         print("email_list Saved")
                    except:
                         print("not save")
     
                message = "success"
                return HttpResponse(message)
            except: 
                message = "error"
                return HttpResponse(message)
    
    if buyer_id:
        return render(request, 'admin/buyer/edit_buyer.html',{
            'buyer_detail': buyer_detail,
            'buyer_category':buyer_category,
            'buyer_menufacture':buyer_menufacture,
            'buyer_model':buyer_model,
            'buyer_email':buyer_email

        })
    else:
       return render(request, 'admin/buyer/add_buyer.html',{

        })

# Email Updata admin Side for Buyer
@login_required(login_url='/users/login')    
def update_buyer_email(request, id):
    try:
        BuyerEmails.objects.filter(id=id).update(email_list=request.POST.get('email_list'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

# Category Updata admin Side for Buyer
@login_required(login_url='/users/login')    
def update_buyer_category(request, id):
    try:
        BuyerCategories.objects.filter(id=id).update(category_name=request.POST.get('category'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)


# Menufacture Updata admin Side for buyer
@login_required(login_url='/users/login')    
def update_buyer_menufacture(request, id):
    try:
        BuyerMenufactures.objects.filter(id=id).update(menufacture_name=request.POST.get('menufacture_name'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)


# Model Updata admin Side for Buyer
@login_required(login_url='/users/login')    
def update_buyer_model(request, id):
    try:
        BuyerModels.objects.filter(id=id).update(model_name=request.POST.get('model_name'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')
def view_buyer(request, id):
    buyer_record = StaffUser.objects.get(user_id=id)
    buyer_category = BuyerCategories.objects.filter(buyer_id=buyer_record)
    buyer_menufacture = BuyerMenufactures.objects.filter(buyer_id=buyer_record)
    buyer_model = BuyerModels.objects.filter(buyer_id=buyer_record)
    buyer_email = BuyerEmails.objects.filter(buyer_id=buyer_record)
     
    return render(request, 'admin/buyer/buyer_profile.html',{
        'buyer_record': buyer_record,
        'buyer_category':buyer_category,
        'buyer_menufacture':buyer_menufacture,
        'buyer_model':buyer_model,
        'buyer_email':buyer_email
    })

@login_required(login_url='/users/login')
def delete_buyer(request, id):
    delete_buyer = StaffUser.objects.get(user_id=id)
    delete_buyer.status =2
    delete_buyer.save()
      
    return redirect('buyer_list')