from django.urls import path
from . import views

urlpatterns = [
    path('CreateUser',views.create_user,name='create_user'),
    path('GetUser',views.login_user,name='login_user'),
    path('UpdateUser',views.update_user,name='update_user'),
    path('DeleteUser',views.delete_user,name='delete_user'),
    path('UploadFile',views.file_upload,name='file_upload'),
    path('DeleteFile',views.file_delete,name='file_delete'),
    path('GetFiles',views.get_all_files,name='get_all_files'),
    path('VerifyOtp',views.verify_otp,name='verify_otp'),
]
