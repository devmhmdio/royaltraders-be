from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.staticfiles.storage import staticfiles_storage
import json
import magic

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

import qrcode
from PIL import Image

from DB.models import *
from DB.serializers import ProductsSerializer

def index(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))

@csrf_protect
def login(request):
    # print(request.user_agent.device)
    # x =  request.META
    # print(x["REMOTE_ADDR"])
    vars = request.POST
    username = vars['username']
    pwd = vars['password']

    try:
        user = User.objects.get(username=username, password=pwd)
        template = loader.get_template('home.html')
        return HttpResponse(template.render({}, request))

    except Exception as e:
        return HttpResponse(e)

@csrf_protect
def addProductForm(request):
    template = loader.get_template('addProduct.html')
    return HttpResponse(template.render({'file':''}, request))

def addWholeseller(request):
    print(request.user_agent.device)
    x =  request.META
    print(x["REMOTE_ADDR"])

    try:
        wh_obj = WholeSellers(ip=x['REMOTE_ADDR'])
        wh_obj.save()
        return HttpResponse("Wholeseller added")

    except Exception as e:
        return HttpResponse(e)
    
@csrf_protect
def insertProduct(request):
    vars = request.POST
    p_id = vars['pname'][:2] + '-' + vars['cat'][:2] + '-' + str(hash(vars['pname'] + vars['cat'] + vars['subcat']))[:4]
    p_obj = Products(
        product_id = p_id,
        product_name = vars['pname'],
        cat = vars['cat'],
        subcat = vars['subcat'],
        ret_price = vars['retp'],
        ws_price = vars['whp']
    )
    try:
        p_obj.save()
        logo = Image.open('static/logo/royal_traders_final_logo.jpg')
        
        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        
        QRcode.add_data(p_id)
        
        QRcode.make()
        
        # taking color name from user
        QRcolor = 'Grey'
        
        # adding color to QR code
        QRimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')
        
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
        
        # save the QR code generated
        QRimg.save('static/qrcodes/{}.png'.format(p_id))

        # content_type = magic.from_buffer(QRimg, mime=True)
        # response = HttpResponse(QRimg, content_type=content_type)
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format(p_id)
        # return redirect('addProduct/', file_obj = 'qrcodes/ab-qw--147.png')

        response = HttpResponseRedirect('addProduct/')
        response.set_cookie(
            key = 'file',
            value = staticfiles_storage.url('qrcodes/{}.png'.format(p_id))
        )
        return response

    except Exception as e:
        print(e)
        return HttpResponse(e)

    # template = loader.get_template('addProduct.html')
    # return HttpResponse(template.render({}, request))

class ProductDetailView(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'product_id'

class ProductsView(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer