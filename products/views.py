from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import Product, Category, Order
from django.http import Http404
from .forms import ProductForm, Registerform

def test_404(request):
    raise Http404("Product not found")

@login_required
@user_passes_test(lambda user: user.is_staff)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request,"product created succesfully")
            return redirect("products")

    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Create Product"
    })

@login_required
@user_passes_test(lambda user: user.is_staff)
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
@user_passes_test(lambda user: user.is_staff)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id,)

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
    product = get_object_or_404(Product,id=product_id,)

    context = {
        "product": product
    }

    return render(request, "products/products_details.html", context)

@login_required
def product_buy(request,product_id):
    if  request.method !="POST":
        product=get_object_or_404(Product,id=product_id)
        return render(request,
        "products/product_buy.html",
        {"product" : product}
        )
    
    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(),
            id=product_id,
        )   
    
    if product.stock < 1:
        messages.error(request,"out of stock")
        return redirect("product_buy",product_id=product.id)

    Order.objects.create(
        customer=request.user,
        product=product,
        quantity=1,
        price_at_purchase=product.price,
    )
    product.stock -= 1
    product.save(update_fields=["stock"])

    messages.success(request,"bought sucessfully")
    return redirect("product_detail",product_id=product.id)


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


@login_required
def my_orders(request):
    orders=(
        Order.objects
        .filter(customer=request.user)
        .select_related("product")
        .order_by("-created_at")
    )
    return render(
        request,
        "products/my_orders.html",
        {"orders":orders},
    )

@login_required
@user_passes_test(lambda user:user.is_staff)
def manage_orders(request):
    orders=(
        Order.objects.
        select_related("customer","product").
        order_by("-created_at")
    )
    return render(
        request,
        "products/manage_orders.html",
        {"orders":orders}
    )

@login_required
@user_passes_test(lambda user:user.is_staff)
def update_order_status(request,order_id):
    if request.method!="POST":
        return redirect("manage_orders")

    order=get_object_or_404(Order,id=order_id)
    new_status=request.POST.get("status")

    valid_statuses=dict(Order.STATUS_CHOICES)

    if new_status not in valid_statuses:
        messages.error(request,"status is not valid")
        return redirect("manage_orders")
    
    order.status=new_status
    order.save(update_fields=["status"])

    messages.success(
        request,
        f"order #{order.id} status successfully updated"
    )
    return redirect("manage_orders")