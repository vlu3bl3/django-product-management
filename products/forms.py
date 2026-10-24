from django import forms
from .models import Product
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","stock","category"]

    def clean_price(self):
        price=self.cleaned_data["price"]

        if price < 0 :
            raise forms.ValidationError(
                "price must be greater than 0"
            )
        return price 

    def clean_name(self):
        name=self.cleaned_data["name"]

        if len(name) < 3:
            raise forms.ValidationError(
                "name must  have atleast 3 characters"
            )
        return name 
    
    def clean(self):
        cleaned_data=super().clean()

        price = cleaned_data.get("price")
        stock = cleaned_data.get("stock")

        if price is not None and stock == 0 and price >= 1000:
            raise forms.ValidationError(
                "an out of stock product can not cost more than 1000"
            )
        return cleaned_data


class Registerform(forms.ModelForm):
    password=forms.CharField(
        label="password",
        widget=forms.PasswordInput
    )

    password2=forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput
    )

    class Meta:
        model=User
        fields=["username","email","password"]

    def clean(self):
        cleaned_data=super().clean()

        password=cleaned_data.get("password")
        password2=cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                "passwords do not match"
            )

        return cleaned_data