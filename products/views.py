
from django.shortcuts import render,redirect,HttpResponse
from .models import Product
from .forms import ProductForm
from .models import User


from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


def list_products(request):
    products=Product.objects.all()
    count=Product.objects.all().count()
    return render(request,'products.html',{'products':products, 'count':count})

def create_product(request):
    form= ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, ('Product Has Been Added Successfully!!!! '))
        return redirect('list_products')

    return render(request,'products-form.html',{'form':form})

def update_product(request,id):
    product=Product.objects.get(id=id)
    form=ProductForm(request.POST or None,instance=product)

    if form.is_valid():
        form.save()
        messages.success(request, ('Product Has Been Updated Successfully!!!! '))
        return redirect('list_products')

    return render(request,'products-form.html',{'form':form,'product':product})

def delete_product(request,id):
    product=Product.objects.get(id=id)

    if request.method=='POST':
        product.delete()
        messages.success(request, ('Product Has Been Deleted Successfully!!!! '))
        return redirect('list_products')

    return render(request,'prod-delete-confirm.html',{'product':product})

def  view_product(request):
    if request.method == 'POST':
        search_query = request.POST['sb']
        print("Search Query : ",search_query)
        product=Product.objects.filter(title__icontains=search_query)

    return render(request, 'only-prod.html',{'product':product})


def index(request):
    return render(request, 'index.html')


def index2(request):
    return render(request, 'index2.html')


def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    hashed_password = request.POST['password'].encode('utf-8')
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    if (User.objects.filter(email=request.POST['login_email']).exists()):
        user = User.objects.filter(email=request.POST['login_email'])[0]
        if (request.POST['login_password'].encode('utf-8'), user.password.encode('utf-8')):
            request.session['id'] = user.id
            return redirect('/products')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'success.html', context)

