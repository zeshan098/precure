from django.shortcuts import render, redirect
from random import choice
from string import ascii_lowercase, digits
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User as DjangoUser
from users.models import StaffUser as User, StaffUser
from vendor.models import VendorInquiry, VendorAttachment, Categories, Menufactures, VendorModels, Emails
from django.contrib.auth.decorators import login_required

# Create your views here.
def vendor_inquiry(request): 
    return render(request, 'web/vendor_inquiry.html',{})


def generate_random_username(length=11, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        DjangoUser.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except DjangoUser.DoesNotExist:
        return username

def vendor_inquiry_form(request): 
    generated_username = generate_random_username()
    if request.is_ajax():
        inquiry_reference_no = request.POST.get('inquiry_reference_no')
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name')
        emails = request.POST.get('emails')
        phone_no = request.POST.get('phone_no')
        website = request.POST.get('website')
        address = request.POST.get('address')  
        quotation_des = request.POST.get('quotation')
        category = request.POST.get('category')
        menufacture = request.POST.get('menufactures') 
        model = request.POST.get('models')
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')
        total_amount = request.POST.get('total_amount') 
        notes = request.POST.get('notes')   
        myfile = request.FILES.getlist('file')
        print(category)

        user = DjangoUser.objects.create( email="precure@gmail.com", username="procureher" + str(generated_username))
        this_user = User.objects.create(user=user,buyer_vendor_name=buyer_vendor_name,
                                         company_name=company_name, phone_no=phone_no, 
                                         website=website, address=address, role="vendor",status='1'
                                         )
  
        vendorinfo = VendorInquiry.objects.create(inquiry_reference_no=inquiry_reference_no,
                                     quotation=quotation_des, sub_total=sub_total,
                                     discount=discount,total_amount=total_amount, 
                                     notes=notes,user=user,status='1')

        
        for f in myfile: 
            VendorAttachment.objects.create(vendorinq=vendorinfo, status='1', attachment_file=f )
        
        try: 
            if category != '': 
                cat_list = category.split (",")
                for cat in  cat_list: 
                    try:  
                        cats = Categories()
                        cats.vendor=this_user
                        cats.category_name=cat
                        cats.status='1'
                        cats.save() 
                        print("category Saved")
                    except:
                        print("not save")


            if menufacture != '': 
                menufacture_list = menufacture.split (",")     
                for menufacture in  menufacture_list: 
                    try:  
                        menufacture_lists = Menufactures()
                        menufacture_lists.vendor=this_user
                        menufacture_lists.menufacture_name=menufacture
                        menufacture_lists.status='1'
                        menufacture_lists.save() 
                        print("menufacture Saved")
                    except:
                        print("not save")
            
            if model != '':
                model_list = model.split (",")
                for model in  model_list: 
                    try:  
                        b_model = VendorModels()
                        b_model.vendor=this_user
                        b_model.model_name=model
                        b_model.status='1'
                        b_model.save() 
                        print("model_name Saved")
                    except:
                        print("not save")

            if emails != '':
                emails_list = emails.split (",") 
                for email in  emails_list: 
                    try:  
                        emails = Emails()
                        emails.vendor=this_user
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
        message = "success"
        return HttpResponse(message)
    else:
        message = "error"
        return HttpResponse(message)

# Admin side Vendor
@login_required(login_url='/users/login')
def vendor_list(request):
    cursor = connection.cursor()
    cursor.execute(""" select au.id, us.buyer_vendor_name, us.company_name, 
                        us.phone_no,us.address  from auth_user au
                        inner join users_staffuser us on au.id = us.user_id 
                        where us.role = 'vendor'
                        and us.status = '1' """); 
    vendor_list = cursor.fetchall()

    return render(request, 'admin/vendor/vendor_list.html',{
        'vendor_list': vendor_list,
    })

# Email Updata admin Side for vendor
@login_required(login_url='/users/login')    
def update_vendor_email(request, id):
    try:
        Emails.objects.filter(id=id).update(email_list=request.POST.get('email_list'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

# Category Updata admin Side for vendor
@login_required(login_url='/users/login')    
def update_vendor_category(request, id):
    try:
        Categories.objects.filter(id=id).update(category_name=request.POST.get('category'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

# Menufacture Updata admin Side for vendor
@login_required(login_url='/users/login')    
def update_vendor_menufacture(request, id):
    try:
        Menufactures.objects.filter(id=id).update(menufacture_name=request.POST.get('menufacture_name'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)


# Model Updata admin Side for vendor
@login_required(login_url='/users/login')    
def update_vendor_model(request, id):
    try:
        VendorModels.objects.filter(id=id).update(model_name=request.POST.get('model_name'))
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_edit_vendor(request, vendor_id=None):
    generated_username = generate_random_username()
    if vendor_id:
        try:
            vendor_detail = StaffUser.objects.get(user_id=vendor_id)
            vendor_category = Categories.objects.filter(vendor_id=vendor_detail)
            vendor_menufacture = Menufactures.objects.filter(vendor_id=vendor_detail)
            vendor_model = VendorModels.objects.filter(vendor_id=vendor_detail)
            vendor_email = Emails.objects.filter(vendor_id=vendor_detail) 
        except StaffUser.DoesNotExist:
            vendor_detail = ''

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
          
        if vendor_id:
            try:   
                required_vendor = StaffUser.objects.filter(id=vendor_id)
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
                this_user = User.objects.create(user=user,buyer_vendor_name=buyer_vendor_name,
                                    company_name=company_name, phone_no=phone_no, alt_phone_no=alt_phone_no,
                                    address=address,website=website,location=location, admin_notes=admin_notes,
                                    role="vendor",status='1',)
                for cat in  cat_list: 
                    try:  
                         cats = Categories()
                         cats.vendor=this_user
                         cats.category_name=cat
                         cats.status='1'
                         cats.save() 
                         print("category Saved")
                    except:
                         print("not save")
                
                for menufacture in  menufacture_list: 
                    try:  
                         menufacture_lists = Menufactures()
                         menufacture_lists.vendor=this_user
                         menufacture_lists.menufacture_name=menufacture
                         menufacture_lists.status='1'
                         menufacture_lists.save() 
                         print("menufacture Saved")
                    except:
                         print("not save")

                for model in  model_list: 
                    try:  
                         b_model = VendorModels()
                         b_model.vendor=this_user
                         b_model.model_name=model
                         b_model.status='1'
                         b_model.save() 
                         print("model_name Saved")
                    except:
                         print("not save")


                for email in  emails_list: 
                    try:  
                         emails = Emails()
                         emails.vendor=this_user
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
    
    if vendor_id:
        return render(request, 'admin/vendor/edit_vendor.html',{
            'vendor_detail': vendor_detail,
            'vendor_category':vendor_category,
            'vendor_menufacture':vendor_menufacture,
            'vendor_model':vendor_model,
            'vendor_email':vendor_email

        })
    else:
       return render(request, 'admin/vendor/add_vendor.html',{

        })

@login_required(login_url='/users/login')
def view_vendor(request, id):
    vendor_record = StaffUser.objects.get(user_id=id) 
    vendor_category = Categories.objects.filter(vendor_id=vendor_record)
    vendor_menufacture = Menufactures.objects.filter(vendor_id=vendor_record)
    vendor_model = VendorModels.objects.filter(vendor_id=vendor_record)
    vendor_email = Emails.objects.filter(vendor_id=vendor_record)
     
    return render(request, 'admin/vendor/vendor_profile.html',{
        'vendor_record': vendor_record, 
        'vendor_category':vendor_category,
        'vendor_menufacture':vendor_menufacture,
        'vendor_model':vendor_model,
        'vendor_email':vendor_email
    })

@login_required(login_url='/users/login')
def delete_vendor(request, id):
    delete_vendor = StaffUser.objects.get(user_id=id)
    delete_vendor.status =2
    delete_vendor.save()
      
    return redirect('vendor_list')