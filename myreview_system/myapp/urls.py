# from django.urls import path
# from .views.user import user_registration, user_login, user_list,home,otp,login,reset_pass,forgot_pass

# urlpatterns = [
#     path('', home),
#     path('getotp/', otp),
#     path('login/',login),
#     path('reset_pass/', reset_pass),
#     path('login/forgot_pass/', forgot_pass),
#     path('register/', user_registration, name='register'),
#     path('login/', user_login, name='login'),
#     path('users/', user_list, name='user-list'),
# ]


from django.urls import path

from .views.user import user_signup, user_login, user_logout,home
from .views.otp import otp_verification,reset_password,otp_verification,forgot_password
# from .views.otp import

urlpatterns = [
    path('', home, name='home'),
    path('login/forgot_pass/', forgot_password, name='forgot_password'),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    
    path('otp_verification/', otp_verification, name='otp_verification'),  # Only define this once
    path('reset-password/', reset_password, name='reset_password'),
    # path('otp/', otp, name='otp'),

]