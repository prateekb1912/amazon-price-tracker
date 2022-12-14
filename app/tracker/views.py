import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from scrapers.amazon_in import get_product_details

from .models import Product
from .forms import UserCreationForm

logger = logging.getLogger(__name__)

@login_required(login_url='/register/', redirect_field_name='')
def index(request):
    if request.method == 'POST':
        post_data = request.POST
        url = post_data['inputURL']

        product_data = get_product_details(url)

        if 'error' in product_data:
            return HttpResponseBadRequest('Error parsing product site')
        
        new_product = Product(**product_data)
        new_product.save()

        return redirect('/products')

    return render(request, 'index.html')

def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        data = request.POST
        logger.warning(data)

        data = request.POST.copy()
        data._mutable = True
        data['password'] = make_password(request.POST['password'])

        form = UserCreationForm(data)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Register success')
            
            return redirect('index')

    context = {'form': form}

    return render(request, 'register.html', context)

@login_required(login_url='/register/', redirect_field_name='')
def view_product(request, asin):
    try:
        product = Product.objects.filter(asin__contains=asin)
        return HttpResponse(product)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest({'error': 'Wrong ASIN'})

@login_required(login_url='/register/', redirect_field_name='')
def list_all_products(request):
    products_list = Product.objects.order_by('-added_at')

    return render(request, template_name='products_list.html', context={'list': products_list})

@login_required(login_url='/register/', redirect_field_name='')
def delete_product(request, asin):
    product = Product.objects.get(asin=asin)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html')
