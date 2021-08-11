from django import forms
from .models import Order,Customer, Product
from django.contrib.auth.models import User
from django.forms import ModelForm


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_by','shipping_address','mobile','email',"payment_method"]
        widgets = {
            "order_by": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the your full name........."
            }),
             "shipping_address": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your address........."

        }),
        "mobile": forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your mobile number....."

        }),
        "email": forms.EmailInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter you email address"

        }),
            "payment_method": forms.Select(attrs={
                "class" : "form-control"
                

        }),
      
      

        }

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the username........."
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your password........."
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
                "class" : "form-control",
                "placeholder" : "@example ram@gmail.com"
    }))

    class Meta:
        model = Customer 
        fields = ['username','password','email','full_name','address']
        widgets = {

            "full_name": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your full name."
            }),
             "address": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your actual address."
            }),

    }
    


    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Customer with this Username already exixts.")
        return uname


class CustomerLoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Enter your username "

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Enter your password "

    }))
    

class AdminLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Enter your username "

    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Enter your password "

    }))
    

class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class":"form-control",
        "multiple":True
    }))
    class Meta:
        model = Product
        fields = ["title","slug","category","image", "marked_price", "selling_price","description","warranty","warranty_policy"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product name........."
            }),
             "slug": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the unique slug here........."

        }),
            "category": forms.Select(attrs={
                "class" : "form-control"
                

        }),
          "image": forms.ClearableFileInput(attrs={
                "class" : "form-control"
                

        }),
          "marked_price": forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the marked price of the product......"

        }),
        "selling_price": forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the selling price of the product......"

        }),
        "description": forms.Textarea(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the description of products......",
                "rows": 5

        }),
        "warranty": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product warranty here....."

        }),

        "warranty_policy": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product warranty_policy here....."

        }),


        }
class ProductUpdateForm(forms.ModelForm):
   
    class Meta:
        model = Product
        fields = ["title","slug","category","image", "marked_price", "selling_price","description","warranty","warranty_policy"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product name........."
            }),
             "slug": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the unique slug here........."

        }),
            "category": forms.Select(attrs={
                "class" : "form-control"
                

        }),
          "image": forms.ClearableFileInput(attrs={
                "class" : "form-control"
                

        }),
          "marked_price": forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the marked price of the product......"

        }),
        "selling_price": forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the selling price of the product......"

        }),
        "description": forms.Textarea(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the description of products......",
                "rows": 5

        }),
        "warranty": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product warranty here....."

        }),

        "warranty_policy": forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter the product warranty_policy here....."

        }),


        }

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Enter the email used in customer account...... "

    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:

            raise forms.ValidationError("Customer with this account does not exists..")
        return e

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password
