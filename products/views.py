from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Product,Category
from django.http import Http404
from .forms import ProductForm,Registerform
from django.contrib.auth.decorators import login_required


def test_404(request):
    raise Http404("Product not found")

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"product created succesfully")
            return redirect("products")

    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Create Product"
    })

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Product updated successfully!"
            )
            return redirect("products")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Edit Product"
    })

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("products")

    return render(request, "products/product_confirm_delete.html", {
        "product": product
    })


def products(request):

    products = Product.objects.all() 
    context ={
        "products" : products
    }
    return render(request,"products/products.html",context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product,id=product_id)

    context = {
        "product": product
    }

    return render(request, "products/products_details.html", context)

def category_products(request,category_id):
    category = get_object_or_404(Category,id=category_id)

    products = category.products.all()

    return render(request,"products/category_products.html",{
        "products" : products,
        "category" : category
    })

def register_view(request):
    if request.method=="POST":
        form=Registerform(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.success(
                request,
                "account created sucessfully"
            )
            return redirect("login")
        
    else:
        form=Registerform()

    return render(
        request,
        "products/register.html",
        {"form":form}
    )