
from django import forms
from .models import CustomUser
from django.contrib.auth.models import User
class EmailForm(forms.Form):
    username = forms.CharField(max_length=50,label="Kullanici Adi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Doğrula",widget=forms.PasswordInput)
    email = forms.EmailField(label="email")
    def clean(self):
        #formdaki bilgiler alındı 
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        email = self.cleaned_data.get("email")

        #parola kontrolü yapıldı 
        if password and confirm and password != confirm:
            raise forms.ValidationError("parolalar uyuşmuyor")
        
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı zaten kullanılıyor, lütfen farklı bir kullanıcı adı seçin.')

        
        values = {
            "username":username,
            "password":password,
            "email":email
        }

        return values  

