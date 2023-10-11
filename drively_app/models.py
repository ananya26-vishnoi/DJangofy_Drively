from django.db import models 

class User(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    role=models.CharField(max_length=1000)

class Token(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    token_value = models.CharField(max_length=1000)

class File(models.Model):
    file_name = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

