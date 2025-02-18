from django import forms
from phonenumber_field.formfields import PhoneNumberField
from onlineshop.models import Comment, Product



class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    phone_number = PhoneNumberField(region="UZ")
    quantity = forms.IntegerField(min_value=1)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'description',
                  'price',
                  'image',
                  'category',
                  'quantity',
                  'rating',
                  'discount']
