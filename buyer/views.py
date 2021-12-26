import json
import datetime
from django.db.backends import utils

from django.shortcuts import render, redirect
from itertools import chain
from random import choice
from string import ascii_lowercase, digits
from django.db import connection 
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage  
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string 
from django.http import HttpResponse, JsonResponse  
from django.contrib.auth.models import User as DjangoUser 
from users.models import StaffUser as User, StaffUser 
from buyer.models import BuyerInquiry, BuyerAttachment, BuyerCategories, BuyerMenufactures, BuyerEmails, BuyerModels, \
                          BuyerInquiryToVendor, BuyerPO
from django.contrib.auth.decorators import login_required

def sendSimpleEmail(request,emailto):
   print(emailto)
   res = send_mail("hello paul", "zeshan ny email ki?", "operations@procurehero.com", [emailto])
   return HttpResponse('%s'%res)


def buyer_inquiry(request): 
    
    

    return render(request, 'web/buyer_inquiry.html',{})

def buyer_category(request):  
    keyword = request.POST.get('keyword')
    cursor = connection.cursor()
    cursor.execute(""" select DISTINCT category_name  from vendor_categories  where status = '1'
                        and  category_name LIKE '%""" + keyword + """%'   """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[0], 'id': obj[0]}) 
    return JsonResponse(list, safe=False)

def buyer_menufacture(request):  
    keyword = request.POST.get('keyword')
    cursor = connection.cursor()
    cursor.execute(""" select DISTINCT menufacture_name  from vendor_menufactures where status = '1'  
                       and  menufacture_name LIKE '%""" + keyword + """%' """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[0], 'id': obj[0]}) 
    return JsonResponse(list, safe=False)

def buyer_model(request):  
    keyword = request.POST.get('keyword')
    cursor = connection.cursor()
    cursor.execute(""" select DISTINCT model_name  from vendor_vendormodels  where status = '1' 
                        and  model_name LIKE '%""" + keyword + """%'  """)
    pro_types = cursor.fetchall()
    list = []
    for obj in pro_types:
        list.append({'name': obj[0], 'id': obj[0]}) 
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
    today = datetime.datetime.now()  
    if request.is_ajax():
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name')
        email = request.POST.getlist('emails')
        phone_no = request.POST.get('phone_no')
        alt_phone_no = request.POST.get('alt_phone_no')
        inquiry_type = request.POST.get('inquiry_type')
        inquiry_des = request.POST.get('inquires')
        category_list = request.POST.getlist('category')
        menufacture_list = request.POST.getlist('menufacture') 
        model_list = request.POST.getlist('model') 
        location = request.POST.get('location') 
        myfile = request.FILES.getlist('file')
        email_to = "operations@procurehero.com"
        ref_no = f'{today:%S%M%H%d%m%Y}'
        # print(category_list)

        user = DjangoUser.objects.create( email="precure@gmail.com", username="procureher" + str(generated_username))
        this_user = User.objects.create(user=user,buyer_vendor_name=buyer_vendor_name,role="buyer",status='1',
                                         company_name=company_name, phone_no=phone_no,
                                          alt_phone_no=alt_phone_no, location=location)
       
        buyerinfo = BuyerInquiry.objects.create(reference_no= ref_no,inquiry_type=inquiry_type,inquires=inquiry_des,
                                                user=user,status='1', created_by=user.id,updated_by=user.id)
        for f in myfile: 
            BuyerAttachment.objects.create(buyerinq=buyerinfo,status='1', attachment_file=f )
 
        
        for cat in  category_list: 
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
                
        for menufacture in  menufacture_list: 
            
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

        for model in  model_list:
            
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
        
        try:
            print(email)  
            html_content = render_to_string("web/email/buyer_inquiry_email.html", {'inquiry_des':inquiry_des, 
            'inquiry_type':inquiry_type, 'category_tag':category_list, 'manufacture_tag':menufacture_list,
            'model':model_list, 'location':location}) 
            # text_content = strip_tags(html_content) 
            msg = EmailMessage("Inquiry Form",html_content,"operations@procurehero.com",[email_to])
            msg.content_subtype = 'html'
            for f in myfile:   
                msg.attach_file('media/'+f.name) 
            msg.send() 
             
            send_mail("Thank You", "Thank You For Query. This is Your Reference #:"+ ref_no, "operations@procurehero.com", [email])
            BuyerInquiryToVendor.objects.create(inquiry_id=str(buyerinfo.id),quotes_received=0,no_of_vendor_send=0)
            
            print("send mail")         
        except:
            print("email not send")

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
            buyer_category = BuyerCategories.objects.filter(buyer_id=buyer_detail, status='1')
            buyer_menufacture = BuyerMenufactures.objects.filter(buyer_id=buyer_detail, status='1')
            buyer_model = BuyerModels.objects.filter(buyer_id=buyer_detail, status='1')
            buyer_email = BuyerEmails.objects.filter(buyer_id=buyer_detail, status='1') 
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

# Email delete for Buyer
@login_required(login_url='/users/login')
@csrf_exempt    
def delete_buyer_email(request, id): 
    try:
        BuyerEmails.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_buyer_email(request, id):
    try:
        BuyerEmails.objects.create(buyer_id=id,email_list=request.POST.get('email_list'), status='1')
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

# Delete category
@login_required(login_url='/users/login')
@csrf_exempt    
def delete_buyer_category(request, id): 
    try:
        BuyerCategories.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_buyer_category(request, id):
    try:
        BuyerCategories.objects.create(buyer_id=id,category_name=request.POST.get('category'), status='1')
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

@login_required(login_url='/users/login')
@csrf_exempt    
def delete_buyer_menufacture(request, id): 
    try:
        BuyerMenufactures.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_buyer_menufacture(request, id):
    try:
        BuyerMenufactures.objects.create(buyer_id=id,menufacture_name=request.POST.get('menufacture_name'), status='1')
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
@csrf_exempt    
def delete_buyer_model(request, id): 
    try:
        BuyerModels.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')
@csrf_exempt    
def delete_buyer_attachment(request, id): 
    try:
        BuyerAttachment.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

login_required(login_url='/users/login')    
def update_buyer_attachment(request, id):
    folder='media/' 
    attachment_file=request.FILES['file']
    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
    filename = fs.save(attachment_file.name, attachment_file)
    file_url = fs.url(filename)
    try:
          
        BuyerAttachment.objects.filter(id=id).update(attachment_file=attachment_file)
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_buyer_attachment(request, id):
    folder='media/' 
    attachment_file=request.FILES['file']
    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
    filename = fs.save(attachment_file.name, attachment_file)
    file_url = fs.url(filename)
    try: 
        BuyerAttachment.objects.create(buyerinq_id=id,attachment_file=attachment_file, status='1')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_buyer_model(request, id):
    try:
        BuyerModels.objects.create(buyer_id=id,model_name=request.POST.get('model_name'), status='1')
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
    delete_buyer.status =6
    delete_buyer.save()
      
    return redirect('buyer_list')

@login_required(login_url='/users/login')
def buyer_inquiry_list(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select bi.id, TO_CHAR(bi.creation_datetime, 'DD-MM-YYYY'),bi.reference_no,
                        us.buyer_vendor_name,us.location, bbi.no_of_vendor_send,
                        Case when bi.status = '1' then 'Received'
                        when bi.status = '2' then 'Sourcing'
                        when bi.status = '3' then 'Submitted'
                        when bi.status = '4' then 'Won'
                        when bi.status = '5' then 'Lost'
                        Else 'Close' End as status, bbi.quotes_received
                        from buyer_buyerinquiry bi
                        left join auth_user au on bi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        left join buyer_buyerinquirytovendor bbi on bbi.inquiry_id::integer = bi.id
                        order by bi.creation_datetime DESC   """)
    buyer_inquiry_lists = cursor.fetchall()
    cursor.execute(""" select * from buyer_buyerinquirytovendor   """)
    quote_vendor = cursor.fetchall() 

    return render(request, 'admin/buyer/inquiry/buyer_inquiry_list.html',{
        'buyer_inquiry_lists':buyer_inquiry_lists,
        'quote_vendor':quote_vendor
    })

@login_required(login_url='/users/login')
def view_buyer_inquiry(request, id):
    cursor = connection.cursor()
    cursor.execute(""" Select us.buyer_vendor_name, us.company_name,us.phone_no, us.alt_phone_no,
                        bi.inquiry_type, bi.inquires, us.location from auth_user au
                        left join buyer_buyerinquiry bi on bi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where bi.id = '""" + str(id) + """'   """)
    buyer_inquiry_view = cursor.fetchall()
    cursor.execute(""" select bbc.category_name from buyer_buyercategories bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'   """)
    buyer_category = cursor.fetchall() 
    cursor.execute(""" select bbc.menufacture_name from buyer_buyermenufactures bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'   """)
    buyer_menufacture = cursor.fetchall() 
    cursor.execute(""" select bbc.model_name from buyer_buyermodels bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'   """)
    buyer_model = cursor.fetchall()  
    cursor.execute(""" select bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'   """)
    buyer_email = cursor.fetchall() 
    cursor.execute(""" select bbc.attachment_file from buyer_buyerattachment bbc 
                       left join buyer_buyerinquiry bbi on bbc.buyerinq_id = bbi.id
                        where bbi.id = '""" + str(id) + """'   """)
    buyer_attachment = cursor.fetchall()
     
    return render(request, 'admin/buyer/inquiry/view_inquiry.html',{
        'buyer_inquiry_view': buyer_inquiry_view,
        'buyer_category':buyer_category,
        'buyer_menufacture':buyer_menufacture,
        'buyer_model':buyer_model,
        'buyer_email':buyer_email,
        'buyer_attachment':buyer_attachment
    })

@login_required(login_url='/users/login')
def edit_buyer_inquiry(request, id):
    cursor = connection.cursor()
    cursor.execute(""" Select bi.id, us.buyer_vendor_name, us.company_name,us.phone_no, us.alt_phone_no,
                        bi.inquiry_type, bi.inquires, us.location, us.id,bi.reference_no,
                        bi.status from auth_user au
                        left join buyer_buyerinquiry bi on bi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where bi.id = '""" + str(id) + """'   """)
    buyer_inquiry_view = cursor.fetchall()
    cursor.execute(""" select bbc.id,bbc.category_name from buyer_buyercategories bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'
                        and bbc.status = '1'   """)
    buyer_category = cursor.fetchall() 
    cursor.execute(""" select bbc.id,bbc.menufacture_name from buyer_buyermenufactures bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """'
                        and bbc.status = '1'   """)
    buyer_menufacture = cursor.fetchall() 
    cursor.execute(""" select bbc.id, bbc.model_name from buyer_buyermodels bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """' 
                        and bbc.status = '1'  """)
    buyer_model = cursor.fetchall()  
    cursor.execute(""" select bbc.id,bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(id) + """' 
                        and bbc.status = '1'  """)
    buyer_email = cursor.fetchall() 
    cursor.execute(""" select bbc.id,bbc.attachment_file from buyer_buyerattachment bbc 
                       left join buyer_buyerinquiry bbi on bbc.buyerinq_id = bbi.id
                        where bbi.id = '""" + str(id) + """'
                        and bbc.status = '1'   """)
    buyer_attachment = cursor.fetchall()
    bbc = [('1')]
    bmc = [('1')]
    bm = [('1')]
    for buyer_cat in buyer_category:
        bbc.append(buyer_cat[1])
    bbc = tuple(bbc) 
    for buyer_menuf  in buyer_menufacture:
        bmc.append(buyer_menuf[1])
    bmc = tuple(bmc) 
    for buyer_mod in buyer_model:
        bm.append(buyer_mod[1])
    bm = tuple(bm) 
    cursor.execute(""" select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_categories" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_categories 
                            where category_name in  """ + str(bbc) + """
                            group by vendor_id 
                            having count(distinct category_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name
                        union
                        select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_menufactures" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_menufactures 
                            where menufacture_name in """ + str(bmc) + """
                            group by vendor_id 
                            having count(distinct menufacture_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name
                        union
                        select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_vendormodels" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_vendormodels
                            where model_name in """ + str(bm) + """
                            group by vendor_id 
                            having count(distinct model_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name   """)
    sender_email_lists = cursor.fetchall() 
    return render(request, 'admin/buyer/inquiry/edit_buyer_inquiry.html',{
        'buyer_inquiry_view': buyer_inquiry_view,
        'buyer_category':buyer_category,
        'buyer_menufacture':buyer_menufacture,
        'buyer_model':buyer_model,
        'buyer_email':buyer_email,
        'buyer_attachment':buyer_attachment,
        'sender_email_lists':sender_email_lists 
    })

@login_required(login_url='/users/login')
def update_buyer_inquiry(request, inquiry_id):  
    
    today = datetime.datetime.now()    
    if request.is_ajax():
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name') 
        phone_no = request.POST.get('phone_no')
        alt_phone_no = request.POST.get('alt_phone_no')
        inquiry_type = request.POST.get('inquiry_type')
        inquiry_des = request.POST.get('inquires') 
        location = request.POST.get('location')    
        status = request.POST.get('status') 
        try:   
            buyer_info = BuyerInquiry.objects.get(id=inquiry_id)  
            update_buyer_info = StaffUser.objects.filter(user_id=buyer_info.user_id) 
            update_buyer_info.update(buyer_vendor_name=buyer_vendor_name, 
                                company_name=company_name, phone_no=phone_no, alt_phone_no=alt_phone_no, 
                                 location=location  )
            inquiry_update = BuyerInquiry.objects.filter(id=inquiry_id).update(inquiry_type=inquiry_type, 
                                inquires=inquiry_des,  updated_by=request.user.id, update_datetime=today, status=status)
            message = "success"
            return HttpResponse(message)
        except: 
            message = "error"
            return HttpResponse(message)

@login_required(login_url='/users/login')
def view_send_buyer_inquiry(request, inquiry_id):
    cursor = connection.cursor()
    cursor.execute(""" Select bi.id, us.buyer_vendor_name, us.company_name,us.phone_no, us.alt_phone_no,
                        bi.inquiry_type, bi.inquires, us.location, us.id,bi.reference_no from auth_user au
                        left join buyer_buyerinquiry bi on bi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where bi.id = '""" + str(inquiry_id) + """'    """)
    buyer_inquiry_view = cursor.fetchall()
    cursor.execute(""" select bbc.id,bbc.category_name from buyer_buyercategories bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(inquiry_id) + """'
                        and bbc.status = '1'   """)
    buyer_category = cursor.fetchall() 
    cursor.execute(""" select bbc.id,bbc.menufacture_name from buyer_buyermenufactures bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(inquiry_id) + """'
                        and bbc.status = '1'   """)
    buyer_menufacture = cursor.fetchall() 
    cursor.execute(""" select bbc.id, bbc.model_name from buyer_buyermodels bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(inquiry_id) + """'
                        and bbc.status = '1'   """)
    buyer_model = cursor.fetchall()  
    cursor.execute(""" select bbc.id,bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.id = '""" + str(inquiry_id) + """'
                        and bbc.status = '1'   """)
    buyer_email = cursor.fetchall() 
    cursor.execute(""" select bbc.attachment_file from buyer_buyerattachment bbc 
                       left join buyer_buyerinquiry bbi on bbc.buyerinq_id = bbi.id
                        where bbi.id = '""" + str(inquiry_id) + """'
                        and bbc.status = '1'   """)
    buyer_attachment = cursor.fetchall()
    bbc = [('1')]
    bmc = [('1')]
    bm = [('1')]
    for buyer_cat in buyer_category:
        bbc.append(buyer_cat[1])
    bbc = tuple(bbc) 
    for buyer_menuf  in buyer_menufacture:
        bmc.append(buyer_menuf[1])
    bmc = tuple(bmc) 
    for buyer_mod in buyer_model:
        bm.append(buyer_mod[1])
    bm = tuple(bm) 
    # print(bm,bmc,bbc)
    cursor.execute(""" select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_categories" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_categories 
                            where category_name in  """ + str(bbc) + """
                            group by vendor_id 
                            having count(distinct category_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name
                        union
                        select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_menufactures" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_menufactures 
                            where menufacture_name in """ + str(bmc) + """
                            group by vendor_id 
                            having count(distinct menufacture_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name
                        union
                        select s.email_list, us.company_name
                        from "vendor_emails" s
                        join "vendor_vendormodels" a on s.vendor_id = a.vendor_id
                        join "users_staffuser" us on s.vendor_id = us.id
                        join (
                            select vendor_id 
                            from vendor_vendormodels
                            where model_name in """ + str(bm) + """
                            group by vendor_id 
                            having count(distinct model_name) = 1
                        ) t on s.vendor_id = t.vendor_id
                        group by s.email_list, us.company_name   """)
    sender_email_lists = cursor.fetchall() 
    return render(request, 'admin/buyer/inquiry/view_send_inquiry.html',{
        'buyer_inquiry_view': buyer_inquiry_view,
        'buyer_category':buyer_category,
        'buyer_menufacture':buyer_menufacture,
        'buyer_model':buyer_model,
        'buyer_email':buyer_email,
        'buyer_attachment':buyer_attachment,
        'sender_email_lists':sender_email_lists 
    })
  
@login_required(login_url='/users/login')
def send_buyer_inquiry_to_vendor(request):  
    
    today = datetime.datetime.now() 
    a = 0   
    if request.is_ajax():
        inquiry_id = request.POST.get('inquiry_id')
        category_list = request.POST.getlist('category_list')
        menufacture_list = request.POST.getlist('menufacture_list') 
        model_list = request.POST.getlist('model_list')
        vendor_email_list = request.POST.getlist('vendor_emails',"false")  
        inquiry_type = request.POST.get('inquiry_type')
        inquiry_des = request.POST.get('inquires')  
        myfile = request.POST.getlist('file',"false")
        email_to = "operations@procurehero.com"
        try:   
              
                
                html_content = render_to_string("admin/buyer/email/inquiry_to_vendor_mail.html", {'inquiry_des':inquiry_des, 
                'inquiry_type':inquiry_type, 'category_tag':category_list, 'manufacture_tag':menufacture_list,
                'model':model_list,  }) 
                # text_content = strip_tags(html_content)
                msg = EmailMessage("Quotation Form",html_content,"operations@procurehero.com",vendor_email_list)
                
                msg.content_subtype = 'html' 
                for f in myfile:  
                    print(f) 
                    msg.attach_file('media/'+f) 
                msg.send()   
                 
                print("send mail")
                for v in vendor_email_list:
                    a +=1 

                inquiry_update = BuyerInquiry.objects.filter(id=inquiry_id).update(status=2)
                BuyerInquiryToVendor.objects.filter(inquiry_id=inquiry_id).update(no_of_vendor_send=a)
                message = "success"
                return HttpResponse(message)
        except: 
            message = "error"
            return HttpResponse(message)

@login_required(login_url='/users/login')
def delete_buyer_inquiry(request, id):
    delete_buyer = BuyerInquiry.objects.get(id=id)
    delete_buyer.status =6
    delete_buyer.save()
      
    return redirect('buyer_inquiry_list')

@login_required(login_url='/users/login')
def add_buyer_inquiry(request): 
    generated_username = generate_random_username()
    today = datetime.datetime.now()  
    if request.is_ajax():
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('emails')
        phone_no = request.POST.get('phone_no')
        alt_phone_no = request.POST.get('alt_phone_no')
        inquiry_type = request.POST.get('inquiry_type')
        inquiry_des = request.POST.get('inquires')
        category_list = request.POST.get('category')
        menufacture_list = request.POST.get('menufacture') 
        model_list = request.POST.get('model') 
        location = request.POST.get('location') 
        myfile = request.FILES.getlist('file')
        email_to = "operations@procurehero.com"
        ref_no = f'{today:%S%M%H%d%m%Y}'
        # print(category_list)

        user = DjangoUser.objects.create( email="precure@gmail.com", username="procureher" + str(generated_username))
        this_user = User.objects.create(user=user,buyer_vendor_name=buyer_vendor_name,role="buyer",status='1',
                                         company_name=company_name, phone_no=phone_no,
                                          alt_phone_no=alt_phone_no, location=location)
       
        buyerinfo = BuyerInquiry.objects.create(reference_no= ref_no,inquiry_type=inquiry_type,inquires=inquiry_des,
                                                user=user,status='1', created_by=user.id,updated_by=user.id)
        for f in myfile: 
            BuyerAttachment.objects.create(buyerinq=buyerinfo,status='1', attachment_file=f )
 
        cat_list = category_list.split (",")  
        menufacture_list = menufacture_list.split (",")  
        model_list = model_list.split (",")  
        emails_list = email.split (",")
        for cat in  cat_list: 
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
                
        for menufacture in  menufacture_list: 
            
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

        for model in  model_list:
            
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


        for email in  emails_list: 
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
        
        try:
            BuyerInquiryToVendor.objects.create(inquiry_id=str(buyerinfo.id),quotes_received=0,no_of_vendor_send=0)
        except:
            print("BuyerInquiryToVendor not added")
        # try:
        #     print(email)  
        #     html_content = render_to_string("web/email/buyer_inquiry_email.html", {'inquiry_des':inquiry_des, 
        #     'inquiry_type':inquiry_type, 'category_tag':category_list, 'manufacture_tag':menufacture_list,
        #     'model':model_list, 'location':location}) 
        #     # text_content = strip_tags(html_content) 
        #     msg = EmailMessage("Inquiry Form",html_content,"operations@procurehero.com",[email_to])
        #     msg.content_subtype = 'html'
        #     for f in myfile:   
        #         msg.attach_file('media/'+f.name) 
        #     msg.send() 
             
        #     send_mail("Thank You", "Thank You For Query. This is Your Reference #:"+ ref_no, "operations@procurehero.com", [email])
        #     BuyerInquiryToVendor.objects.create(inquiry_id=str(buyerinfo.id),quotes_received=0,no_of_vendor_send=0)
            
        #     print("send mail")         
        # except:
        #     print("email not send")

        message = "success"
        return HttpResponse(message)
    # else:
    #     message = "error"
    #     return HttpResponse(message)

    return render(request, 'admin/buyer/inquiry/add_buyer_inquiry.html',{
        
    })

@login_required(login_url='/users/login')
def create_buyer_po(request):
    
    today = datetime.datetime.now() 
    
    if request.is_ajax(): 
        reference_no = request.POST.get('reference_no') 
        buyer_email_list = request.POST.getlist('buyer_emails',"false")  
        to_email = request.POST.get('to_email') 
        quotation = request.POST.get('quotation')   
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')  
        total = request.POST.get('total')  
        notes = request.POST.get('notes')  
        myfile = request.FILES['file'] 
        
        buyer_po = BuyerPO.objects.create(reference_no=reference_no,
                                     quotation=quotation, sub_total=sub_total,
                                     discount=discount,total_amount=total, 
                                     notes=notes,created_by=request.user.id,updated_by=request.user.id,
                                     attachment_file=myfile,
                                     status='1')
        
        html_content = render_to_string("admin/buyer/email/buyer_po_email.html", {'ref_no':reference_no, 
                'quotation':quotation,  'sub_total':sub_total, 'discount': discount, 'total':total,
                'notes':notes }) 
        msg = EmailMessage("Quotation Form",html_content,"operations@procurehero.com",buyer_email_list)
        msg.content_subtype = 'html'    
        msg.attach_file('media/'+myfile.name) 
        msg.send()  

        message = "success"
        return HttpResponse(message)
     
        
    return render(request, 'admin/buyer/purchase_order/create_po.html',{
        
    })

def buyer_po_list(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select bpo.id,bpo.reference_no,  TO_CHAR(bpo.creation_datetime, 'DD-MM-YYYY') 
                        from buyer_buyerpo bpo 
                        order by bpo.creation_datetime DESC   """)
    po_list = cursor.fetchall() 

    return render(request, 'admin/buyer/purchase_order/po_list.html',{
        'po_list':po_list 
    })

csrf_exempt
def get_buyer_email(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('searchref') 
        
        vendor_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no, status='3') 
        staff_user = StaffUser.objects.get(user_id=vendor_inquiry_record.user_id) 
        email = BuyerEmails.objects.filter(buyer_id=staff_user.id) 
         
        return JsonResponse(serializers.serialize('json', email, fields=('email_list')), safe=False)