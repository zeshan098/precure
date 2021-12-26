from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
 
from django.http import HttpResponse
from django.template.loader import get_template
 
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf. 
from xhtml2pdf import pisa  
#difine render_to_pdf() function
 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO() 
     print(template_src)
     #This part will create the pdf.  
     destination = 'media/'
     filename = "zeshan1" + '.pdf'
     file = open(destination + filename, "w+b")
     pdf = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

    