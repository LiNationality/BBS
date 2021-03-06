from django.forms import ModelForm,widgets
from web_app import models
from django import forms



class User(ModelForm):
    def __new__(cls, *args, **kwargs):

        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model=models.User
        fields="__all__"