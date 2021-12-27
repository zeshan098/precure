import json
import datetime
from io import BytesIO
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
from vendor.models import VendorInquiry, VendorAttachment, Categories, Menufactures, VendorModels, Emails, VendorPO
from buyer.models import BuyerInquiry, BuyerInquiryToVendor, BuyerCategories, BuyerMenufactures, BuyerModels, BuyerEmails 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xhtml2pdf import pisa 

# Create your views here.
def vendor_inquiry(request): 
    return render(request, 'web/vendor_inquiry.html',{})

@csrf_exempt
def get_category_tag(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('reference_no') 
        
        buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
        staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id) 
        category = BuyerCategories.objects.filter(buyer_id=staff_user.id) 
        # list = []
        # for obj in category:
        #     list.append(obj) 

        return JsonResponse(serializers.serialize('json', category, fields=('category_name')), safe=False)

@csrf_exempt
def get_menufacture_tag(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('reference_no') 
        
        buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
        staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id)  
        menufacture = BuyerMenufactures.objects.filter(buyer_id=staff_user.id) 
        # list = []
        # for obj in category:
        #     list.append(obj)

        return JsonResponse(serializers.serialize('json', menufacture, fields=('menufacture_name')), safe=False)

@csrf_exempt
def get_model_tag(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('reference_no') 
        
        buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
        staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id)  
        model = BuyerModels.objects.filter(buyer_id=staff_user.id) 
        # list = []
        # for obj in category:
        #     list.append(obj)

        return JsonResponse(serializers.serialize('json', model, fields=('model_name')), safe=False)

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
    no_of_qoute = 1
    if request.is_ajax():
        inquiry_reference_no = request.POST.get('inquiry_reference_no')
        buyer_vendor_name = request.POST.get('buyer_vendor_name')
        company_name = request.POST.get('company_name')
        emails_list = request.POST.getlist('email')
        phone_no = request.POST.get('phone_no')
        website = request.POST.get('website')
        address = request.POST.get('address')  
        quotation_des = request.POST.get('quotation')
        category_list = request.POST.get('category')
        menufacture_list = request.POST.get('menufactures') 
        model_list = request.POST.get('models')
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')
        total_amount = request.POST.get('total_amount') 
        notes = request.POST.get('notes')   
        myfile = request.FILES.getlist('file')
        email_to="operations@procurehero.com"
        print(emails_list)

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
            if category_list != '': 
                cat_list = category_list.split (",")
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


            if menufacture_list != '': 
                menufacture_lists = menufacture_list.split (",")     
                for menufacture in  menufacture_lists: 
                    try:  
                        menufacture_lists = Menufactures()
                        menufacture_lists.vendor=this_user
                        menufacture_lists.menufacture_name=menufacture
                        menufacture_lists.status='1'
                        menufacture_lists.save() 
                        print("menufacture Saved")
                    except:
                        print("not save")
            
            if model_list != '':
                model_lists = model_list.split (",")
                for model in  model_lists: 
                    try:  
                        b_model = VendorModels()
                        b_model.vendor=this_user
                        b_model.model_name=model
                        b_model.status='1'
                        b_model.save() 
                        print("model_name Saved")
                    except:
                        print("not save")

            if emails_list != '':
                # emails_lists = emails_list.split (",") 
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
            try:
                print(email)  
                html_content = render_to_string("web/email/vendor_inquiry_email.html", {'ref_no':inquiry_reference_no, 
                'quotation':quotation_des, 'category_tag':category_list, 'manufacture_tag':menufacture_list,
                'model':model_list, 'sub_total':sub_total, 'discount': discount, 'total':total_amount,
                'vendor_notes':notes }) 
                msg = EmailMessage("Quotation Form",html_content,"operations@procurehero.com",[email_to])
                msg.content_subtype = 'html'
                for f in myfile:   
                    msg.attach_file('media/'+f.name) 
                msg.send()  
                # emails_lists = emails_list.split (",") 
                for email in  emails_list:  
                    send_mail("Inquiry Form", "Thank you For Quotation", "operations@procurehero.com", [email])
                    print("send mail")
                    inquiry_update = BuyerInquiry.objects.get(reference_no=inquiry_reference_no)
                    quote_received = BuyerInquiryToVendor.objects.get(inquiry_id=inquiry_update.id)
                    no_of_qoute  =int(quote_received.quotes_received) + 1
                    BuyerInquiryToVendor.objects.filter(inquiry_id=inquiry_update.id).update(quotes_received=no_of_qoute)
            except:
                print("email not send")            
            message = "success"
            return HttpResponse(message)
        except: 
            message = "error"
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

# Email delete for vendor
@login_required(login_url='/users/login')
@csrf_exempt    
def delete_vendor_email(request, id): 
    try:
        Emails.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_vendor_email(request, id):
    try:
        Emails.objects.create(vendor_id=id,email_list=request.POST.get('email_list'), status='1') 
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

@login_required(login_url='/users/login')
@csrf_exempt    
def delete_vendor_category(request, id): 
    try:
        Categories.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_vendor_category(request, id):
    try:
        Categories.objects.create(vendor_id=id,category_name=request.POST.get('category'), status='1') 
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

@login_required(login_url='/users/login')
@csrf_exempt    
def delete_vendor_menufacture(request, id): 
    try:
        Menufactures.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_vendor_menufacture(request, id):
    try:
        Menufactures.objects.create(vendor_id=id,menufacture_name=request.POST.get('menufacture_name'), status='1') 
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
@csrf_exempt    
def delete_vendor_model(request, id): 
    try:
        VendorModels.objects.filter(pk=id).update(status='2')
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

@login_required(login_url='/users/login')    
def add_vendor_model(request, id):
    try:
        VendorModels.objects.create(vendor_id=id,model_name=request.POST.get('model_name'), status='1') 
        message = "success"
        return HttpResponse(message)
    except:
        message = "error"
        return HttpResponse(message)

# //admin vendor 
@login_required(login_url='/users/login')    
def add_edit_vendor(request, vendor_id=None):
    generated_username = generate_random_username()
    if vendor_id:
        try:
            vendor_detail = StaffUser.objects.get(user_id=vendor_id)
            vendor_category = Categories.objects.filter(vendor_id=vendor_detail, status='1')
            vendor_menufacture = Menufactures.objects.filter(vendor_id=vendor_detail, status='1')
            vendor_model = VendorModels.objects.filter(vendor_id=vendor_detail, status='1')
            vendor_email = Emails.objects.filter(vendor_id=vendor_detail, status='1') 
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


@login_required(login_url='/users/login')
def quotation_list(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select vi.id, TO_CHAR(vi.creation_datetime, 'DD-MM-YYYY'),vi.inquiry_reference_no,
                        us.buyer_vendor_name,  
                        Case when vi.status = '1' then 'Open'
                        when vi.status = '2' then 'Sent'
                        when vi.status = '3' then 'Close'
                        Else 'Confirm' End as status   
                        from vendor_vendorinquiry vi
                        left join auth_user au on vi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id 
                        order by vi.creation_datetime DESC   """)
    quotation_list = cursor.fetchall() 

    return render(request, 'admin/vendor/quotation/quotation_list.html',{
        'quotation_list':quotation_list 
    })

@login_required(login_url='/users/login')
def add_vendor_quotation(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select vi.id, TO_CHAR(vi.creation_datetime, 'DD-MM-YYYY'),vi.inquiry_reference_no,
                        us.buyer_vendor_name,  
                        Case when vi.status = '1' then 'Open'
                        when vi.status = '2' then 'Close'
                        Else 'Confirm' End as status   
                        from vendor_vendorinquiry vi
                        left join auth_user au on vi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id 
                        order by vi.creation_datetime DESC   """)
    quotation_list = cursor.fetchall() 

    return render(request, 'admin/vendor/quotation/add_quotation.html',{
        'quotation_list':quotation_list 
    })
 
csrf_exempt
def get_buyer_email(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('searchref') 
        
        buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
        staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id) 
        email = BuyerEmails.objects.filter(buyer_id=staff_user.id) 
        
        return JsonResponse(serializers.serialize('json', email, fields=('email_list')), safe=False)

@login_required(login_url='/users/login')
def send_quotation(request):  
    
    today = datetime.datetime.now() 
    no_of_qoute = 1
    if request.is_ajax(): 
        title = request.POST.get('title')
        reference_no = request.POST.get('reference_no') 
        quotation = request.POST.get('quotation')  
        buyer_email_list = request.POST.getlist('buyer_emails',"false")  
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')  
        total = request.POST.get('total')  
        notes = request.POST.get('notes')  
        email_to = request.POST.get('from_email') 

        
        VendorInquiry.objects.create(inquiry_reference_no=reference_no,
                                     quotation=quotation, sub_total=sub_total,
                                     discount=discount,total_amount=total, 
                                     notes=notes,user=request.user,status='2')
        try:   
            for buyer_email_list in buyer_email_list: 
                buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
                staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id) 
                email = BuyerEmails.objects.filter(buyer_id=staff_user.id)  
                context = {
                    'title':title,
                    'name':staff_user.buyer_vendor_name,
                    'email':email,
                    'address': staff_user.address,
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
                template = get_template('admin/vendor/pdf/invoice.html')
                html  = template.render(context)
                result = BytesIO() 
                destination = 'media/'
                filename = f'{today:%S%M%H%d%m%Y}' + '.pdf'
                file = open(destination + filename, "w+b")
                pdf = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
                html_content = render_to_string("admin/vendor/email/quotation_template.html", {'reference_no':reference_no, 
                'date':today, 'quotation':quotation, 'sub_total':sub_total, 'discount':discount,
                'total':total, 'notes':notes }) 
                # text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject="Quotation", from_email="operations@procurehero.com",
                                to=[buyer_email_list], body=html_content)
                msg.content_subtype = 'html'  
                msg.attach_file('media/'+filename) 
                msg.send() 
                print("send mail") 
                inquiry_update = BuyerInquiry.objects.get(reference_no=reference_no)
                quote_received = BuyerInquiryToVendor.objects.get(inquiry_id=inquiry_update.id) 
                no_of_qoute  =int(quote_received.quotes_received) + 1
                BuyerInquiryToVendor.objects.filter(inquiry_id=inquiry_update.id).update(quotes_received=no_of_qoute)
            message = "success"
            return HttpResponse(message)
        except: 
            message = "error"
            return HttpResponse(message)

@login_required(login_url='/users/login')
def view_vendor_inquiry(request, id):
    cursor = connection.cursor()
    cursor.execute(""" Select us.buyer_vendor_name,vi.inquiry_reference_no,TO_CHAR(vi.creation_datetime, 'DD-MM-YYYY'), 
                        vi.quotation,vi.sub_total,vi.discount, vi.total_amount,vi.notes,vi.id from auth_user au
                        left join vendor_vendorinquiry vi on vi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where vi.id = '""" + str(id) + """'   """)
    vendor_quoatation_view = cursor.fetchall()
    vendor_reference_no = VendorInquiry.objects.get(id=id) 
    cursor.execute(""" select bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.reference_no = '""" + str(vendor_reference_no.inquiry_reference_no) + """'   """)
    buyer_email = cursor.fetchall() 
     
    print(buyer_email)
    return render(request, 'admin/vendor/quotation/view_quotation.html',{
        'vendor_quoatation_view': vendor_quoatation_view, 
        'buyer_email':buyer_email 
    })

@login_required(login_url='/users/login')
def view_edit_inquiry(request, id):
    cursor = connection.cursor()
    cursor.execute(""" Select us.buyer_vendor_name,vi.inquiry_reference_no,TO_CHAR(vi.creation_datetime, 'DD-MM-YYYY'), 
                        vi.quotation,vi.sub_total,vi.discount, vi.total_amount,vi.notes,vi.id,
                        vi.status from auth_user au
                        left join vendor_vendorinquiry vi on vi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where vi.id = '""" + str(id) + """'   """)
    vendor_quoatation_view = cursor.fetchall()
    vendor_reference_no = VendorInquiry.objects.get(id=id) 
    cursor.execute(""" select bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.reference_no = '""" + str(vendor_reference_no.inquiry_reference_no) + """'   """)
    buyer_email = cursor.fetchall() 
     
     
    return render(request, 'admin/vendor/quotation/edit_quotation.html',{
        'vendor_quoatation_view': vendor_quoatation_view, 
        'buyer_email':buyer_email 
    })

@login_required(login_url='/users/login')
def view_send_inquiry(request, id):
    cursor = connection.cursor()
    cursor.execute(""" Select us.buyer_vendor_name,vi.inquiry_reference_no,TO_CHAR(vi.creation_datetime, 'DD-MM-YYYY'), 
                        vi.quotation,vi.sub_total,vi.discount, vi.total_amount,vi.notes,vi.id,
                        vi.status from auth_user au
                        left join vendor_vendorinquiry vi on vi.user_id = au.id
                        left join users_staffuser us on us.user_id = au.id
                        where vi.id = '""" + str(id) + """'   """)
    vendor_quoatation_view = cursor.fetchall()
    vendor_reference_no = VendorInquiry.objects.get(id=id) 
    cursor.execute(""" select bbc.email_list from buyer_buyeremails bbc
                        left join users_staffuser us on bbc.buyer_id = us.id
                        left join auth_user au on au.id = us.user_id
                        left join buyer_buyerinquiry bbi on bbi.user_id = au.id
                        where bbi.reference_no = '""" + str(vendor_reference_no.inquiry_reference_no) + """'   """)
    buyer_email = cursor.fetchall() 
     
     
    return render(request, 'admin/vendor/quotation/send_quotation.html',{
        'vendor_quoatation_view': vendor_quoatation_view, 
        'buyer_email':buyer_email 
    })

@login_required(login_url='/users/login')
def update_send_inquiry(request):  
    
    today = datetime.datetime.now()    
    if request.is_ajax():
        id = request.POST.get('id')
        reference_no = request.POST.get('reference_no') 
        quotation = request.POST.get('quotation')
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')
        total = request.POST.get('total') 
        notes = request.POST.get('notes')    
        status = request.POST.get('status') 
        
        try:
            inquiry_update = VendorInquiry.objects.filter(id=id).update(quotation=quotation,sub_total=sub_total,
                              discount=discount,notes=notes,
                              total_amount=total, status=status)

            message = "success"
            return HttpResponse(message)
        except: 
            message = "error"
            return HttpResponse(message)


@login_required(login_url='/users/login')
def send_quotation_to_buyer_email(request):  
    
    today = datetime.datetime.now() 
    no_of_qoute = 1
    if request.is_ajax():
        id = request.POST.get('id')
        title = request.POST.get('title')
        reference_no = request.POST.get('reference_no')
        date = request.POST.get('date')
        quotation = request.POST.get('quotation')  
        buyer_email_list = request.POST.getlist('buyer_emails',"false")  
        sub_total = request.POST.get('sub_total')
        discount = request.POST.get('discount')  
        total = request.POST.get('total')  
        notes = request.POST.get('notes')  
        email_to = "operations@procurehero.com" 
        try:   
            for buyer_email_list in buyer_email_list: 
                buyer_inquiry_record = BuyerInquiry.objects.get(reference_no=reference_no) 
                staff_user = StaffUser.objects.get(user_id=buyer_inquiry_record.user_id) 
                email = BuyerEmails.objects.filter(buyer_id=staff_user.id)  
                context = {
                    'title':title,
                    'name':staff_user.buyer_vendor_name,
                    'email':email,
                    'address': staff_user.address,
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
                template = get_template('admin/vendor/pdf/invoice.html')
                html  = template.render(context)
                result = BytesIO() 
                destination = 'media/'
                filename = f'{today:%S%M%H%d%m%Y}' + '.pdf'
                file = open(destination + filename, "w+b")
                pdf = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
                html_content = render_to_string("admin/vendor/email/quotation_template.html", {'reference_no':reference_no, 
                'date':date, 'quotation':quotation, 'sub_total':sub_total, 'discount':discount,
                'total':total, 'notes':notes }) 
                # text_content = strip_tags(html_content) 
                msg = EmailMultiAlternatives(subject="Quotation", from_email="operations@procurehero.com",
                                to=[buyer_email_list], body=html_content)
                msg.content_subtype = 'html'  
                msg.attach_file('media/'+filename)
                msg.send() 
                print("send mail") 
                inquiry_update = BuyerInquiry.objects.get(reference_no=reference_no)
                quote_received = BuyerInquiryToVendor.objects.get(inquiry_id=inquiry_update.id)
                no_of_qoute  =int(quote_received.quotes_received) + 1
                BuyerInquiryToVendor.objects.filter(inquiry_id=inquiry_update.id).update(quotes_received=no_of_qoute)
            VendorInquiry.objects.filter(id=id).update(status=2)    
            message = "success"
            return HttpResponse(message)
        except: 
            message = "error"
            return HttpResponse(message)


@login_required(login_url='/users/login')
def delete_vendor_quotation(request, id):
    delete_quotation = VendorInquiry.objects.get(id=id)
    delete_quotation.status =3
    delete_quotation.save()
      
    return redirect('quotation_list')

@login_required(login_url='/users/login')
def create_vendor_po(request):
    
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
        
        vendor_po = VendorPO.objects.create(reference_no=reference_no,
                                     quotation=quotation, sub_total=sub_total,
                                     discount=discount,total_amount=total, 
                                     notes=notes,created_by=request.user.id,updated_by=request.user.id,
                                     attachment_file=myfile,
                                     status='1')
        
        html_content = render_to_string("admin/vendor/email/vendor_po_email.html", {'ref_no':reference_no, 
                'quotation':quotation,  'sub_total':sub_total, 'discount': discount, 'total':total,
                'notes':notes }) 
        msg = EmailMessage("Quotation Form",html_content,"operations@procurehero.com",buyer_email_list)
        msg.content_subtype = 'html'    
        msg.attach_file('media/'+myfile.name) 
        msg.send()  

        message = "success"
        return HttpResponse(message)
     
        
    return render(request, 'admin/vendor/purchase_order/create_po.html',{
        
    })

csrf_exempt
def get_vendor_email(request): 
    if request.method == 'POST':
        reference_no = request.POST.get('searchref') 
        
        vendor_inquiry_record = VendorInquiry.objects.get(inquiry_reference_no=reference_no, status='4') 
        if vendor_inquiry_record.status =='4':
            staff_user = StaffUser.objects.get(user_id=vendor_inquiry_record.user_id) 
            email = Emails.objects.filter(vendor_id=staff_user.id) 
            
            return JsonResponse(serializers.serialize('json', email, fields=('email_list')), safe=False)
        else:
            message = "error"
            return HttpResponse(message)

@login_required(login_url='/users/login')
def vendor_po_list(request): 
    
    cursor = connection.cursor()
    cursor.execute(""" select vpo.id,vpo.reference_no,  TO_CHAR(vpo.creation_datetime, 'DD-MM-YYYY') 
                        from vendor_vendorpo vpo 
                        order by vpo.creation_datetime DESC   """)
    po_list = cursor.fetchall() 

    return render(request, 'admin/vendor/purchase_order/po_list.html',{
        'po_list':po_list 
    })