from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from onlineshop.models import Comment, Product


class OrderForm(forms.Form):
    full_name = forms.CharField()
    phone_number = PhoneNumberField(region='UZ')
    quantity = forms.IntegerField()


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
