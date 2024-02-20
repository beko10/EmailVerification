
from django.shortcuts import render,redirect,HttpResponse
from .forms import EmailForm
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import CustomUser

# Create your views here.

# nfmy cspl xugp qmpf

def index(request):
    return render(request,"index.html")


def register(request):
    
    form = EmailForm(request.POST or None)

    if form.is_valid():
        #formdan gelen bilgiler alındı 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        #kullanıcıc kayıt işlemi
        newUser = CustomUser(username=username)
        newUser.set_password(password)
        newUser.is_active = False
        newUser.save()
        #site domaini alındı 
        current_site = get_current_site(request)
        #mesaj başlığı
        subject = "merhaba"
        #mesaj içeriği 
        messages = message = render_to_string('emaildogrulama.html', {
                'user': newUser,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),#kulanıcının id bilgisi force_bytes fon. ile byte dizisine çevirilde urlsafe_base64_encode ile çevrilen bayt dizisi url uyumlu base64 kodlar
                'token': account_activation_token.make_token(newUser),#kullanıcıya özgü token oluşturur 
            })
        #gonderen
        email_from = settings.EMAIL_HOST_USER
        #alıcı
        recipient_list = [email] 
        #email gönmderildi 
        send_mail(subject,messages,email_from,recipient_list)
        return HttpResponse("e mail doğrula ")

    context ={
        "form":form
    }
    return render(request,"register.html",context)

def activate(request, uidb64, token):
    try:
        #kodlanan uid çözülür
        uid = urlsafe_base64_decode(uidb64).decode()
        #veri tabanından çözülen uid bilgisine sahip kullanıcı alınır
        user = CustomUser.objects.get(pk=uid)
        #tokenin geçerliliği kontroledilir
        if default_token_generator.check_token(user, token):
            #kullanıcı aktif edilir
            user.is_active = True
            user.save()
            return render(request, "activation_success.html")  # Create this success template
        else:
            return HttpResponse("Activation link is invalid.")
    except Exception as e:
        return HttpResponse("Activation link is invalid.")



"""
NOTLAR
---------
urlsafe_base64_encode ve force_bytes gibi terimler Django web çerçevesiyle ilgilidir ve kullanıcı kimliklerinin veya anahtarlarının işlenmesinde sıkça kullanılırlar.

force_bytes:

force_bytes fonksiyonu, verilen bir değeri (genellikle bir string veya başka bir veri) bytes türüne dönüştürür. Django'da sıklıkla veritabanına veya başka bir yerde 
kullanılmadan önce veriyi uygun bir biçime getirmek için kullanılır. Özellikle karakter dizileri (strings) ve Unicode verileri ile çalışırken kullanışlıdır çünkü Django, bu tür verilerin güvenli bir şekilde işlenmesini sağlar.

urlsafe_base64_encode:

urlsafe_base64_encode, verilen bir byte dizisini URL'lerde güvenle kullanılabilen base64 kodlamasına dönüştüren bir işlevidir. Normal base64 kodlamasının 
URL'lerle uyumsuz karakterleri içerdiği için Django'da kimlik doğrulama belirteçleri veya diğer hassas verileri URL'lerle birlikte kullanırken kullanılır. 
Bu işlem, base64 kodlamasında kullanılan bazı karakterleri değiştirir, böylece URL'lerde kullanılabilecek bir biçime getirir.
Sorunuzdaki kod, yeni bir kullanıcı (muhtemelen Django'da bir kullanıcı modeli ile ilişkilendirilen) için bir kimlik belirteci oluşturuyor gibi görünüyor. 
Bu kimlik belirteci URL'lerde kullanılmak üzere güvenli bir şekilde base64 kodlanmış bir değeri temsil ediyor olabilir. Bu tür kimlik belirteçleri, kullanıcı oturumlarını yönetmek veya kimlik doğrulama işlemlerini kolaylaştırmak için kullanılabilir.




"""