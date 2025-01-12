# from django.shortcuts import render, redirect
# from django.views import View
# import json
# from validate_email import validate_email 
# from django.http import JsonResponse
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.core.mail import EmailMessage
# from django.urls import reverse
# from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from .utils import account_activation_token
# from django.contrib import auth









# class EmailValidationView(View):
#     def get(self, request):
#         data = json.loads(request.body)
#         email = data['email']

#         if not validate_email(email):
#             return JsonResponse({"email_error": "Emailis valid"}, status='400')
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({"email_error": "soryy email in use, Choose another one"}, status='409')
#         return JsonResponse({"email_valid": True})


# class UserNameValidationView(View):
#     def get(self, request):
#         data = json.loads(request.body)
#         username = data['username']

#         if not str(username).isalnum():
#             return JsonResponse({"username_error": "username should only contain alphanumeric characters"}, status='400')
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({"username_error": "soryy username in use, Choose another one"}, status='409')
#         return JsonResponse({"username_valid": True})
    
# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'authentication/register.html')
    
#     def post(self, request):
#         # GET USER DATA
#         # VALIDATE
#         # create a user account

#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         context = {
#             'fieldValues': request.POST 
#         }


#         if not User.objects.filter(username=username).exists():
#             if not User.objects.filter(email=email).exists():

#                 if len(password) <6:
#                     messages.error(request, 'Parol juda qisqa')
#                     return render(request, 'authentication/register.html', context)
#                 user = User.objects.create_user(username=username, email=email)
#                 user.set_password(password)
#                 user.is_active=True  
#                 user.save()

#                 # path_to_view
#                 # - getting domain we are on
#                 # - relative url to verification
#                 # - encode uid
#                 # - token
#                 uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#                 domain = get_current_site(request).domain
#                 link = reverse('activate', kwargs={
#                     'uidb64': uidb64, 'token': account_activation_token.make_token(user)
#                 })

#                 activate_url = 'http://' + domain+link

#                 email_subject = 'Activate your account'
#                 email_body = 'Salom'+user.username + 'Hisobingizni tasdiqlash uchun ushbu havoladan foydalaning' + activate_url 
#                 email = EmailMessage(
#                         email_subject,
#                         email_body,
#                         "azamovhusanboy08@gmail.com",
#                         [email],
#                     )
#                 email.send(fail_silently=False)
#                 messages.success(request, 'Hisob muvaffaqiyatli yaratildi')
#                 return render(request, 'authentication/register.html')


#         return render(request, 'authentication/register.html')
    

# class VerificationView(View):
#     def get(self, request, uidb64, token):
#         try:
#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=id)

#             if not account_activation_token.check_token(user, token):
#                 return redirect("login"+"?message="+'User already activated')
            
#             if user.is_active:
#                 return redirect("login")
#             user.is_active = True
#             user.save()

#             messages.success(request, "Hisob muvaffaqiyatli yaratildi")
#             return redirect("login")





#         except Exception as ex:
#             pass

#         return redirect("login")
    

# class LoginView(View):
#     def get(self, request):
#         return render(request, "authentication/login.html")
    

#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']


#         if username and password:
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     auth.login(request, user)
#                     messages.success(
#                         request, 'Xush kelibsiz, ' + username + ' endi tizimga kirgansiz'
#                         )
#                     return redirect('expenses')

#                 messages.error(
#                     request, "Hisob faollashtirilmagan, o'z hisobingizni tekshiring"
#                     )
#                 return render(request, 'authentication/login.html')
        
#             messages.error(
#                 request, 'Yaroqsiz hisob maʼlumotlari qayta urinib koʻring'
#             )
#             return render(request, 'authentication/login.html')
        
#         messages.error(
#                 request, 'Iltimos, barcha maydonlarni toʻldiring')
#         return render(request, 'authentication/login.html')
        

# class LogoutView(View):
#     def post(self, request):
#         auth.logout(request)
#         messages.success(request, "Siz tizimdan chiqdingiz")
#         return redirect("login")


# class RequestPasswordResetEmail(View):
#     def get(self, request):
#         return render(request, 'authentication/reset-password.html')
    
#     def post(self, request):
#         return render(request, 'authentication/reset-password.html')