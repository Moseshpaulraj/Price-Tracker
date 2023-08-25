from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator


context={}
search_list=[]

def home(request):
    combined = FProducts.objects.filter(trending=1).union(AProducts.objects.filter(trending=1))
    return render(request,"app/index.html",{'products':combined})

def register(request):
    return render(request,"app/register.html")

def collections(request):
    category = Category.objects.filter()
    return render(request,"app/collections.html", {'category': category})

def collectionsview(request,name):
    combined = FProducts.objects.filter(category__name=name).union(AProducts.objects.filter(category__name=name))
    paginator = Paginator(combined, 40)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'app/products/index.html', {'products': products,'category_name':name})

    
def product_details(request,cname,pname):
    Fproducts=FProducts.objects.filter(category__name=cname,name=pname).first()
    Aproducts=AProducts.objects.filter(category__name=cname,name=pname).first()
    if Fproducts:
        products=Fproducts
    elif Aproducts:
        products=Aproducts
    return render(request,"app/products/product_details.html",{"products":products})

def search_product(request):
    if request.method == 'POST':
        search_value = request.POST.get('search')
        result = str(search_value).strip()
        categories=Category.objects.all()
        values = [category.name for category in categories]
        for value in values:
            if(result==value or result==value.lower() or result==value[:len(value)-1] or result==value[:len(value)-1].lower() or result==value.replace(" ","")):
                combined = FProducts.objects.filter(category__name=value).union(AProducts.objects.filter(category__name=value))
                return render(request,"app/search_product.html",{"products":combined})
            
        combined = FProducts.objects.filter(name__icontains=result).union(AProducts.objects.filter(name__icontains=result))
        return render(request,"app/search_product.html",{"products":combined})
    return redirect("home")
        



def notification(request):
    return render(request,"app/notification.html",context)
