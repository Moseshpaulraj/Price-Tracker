from django.db import models
import datetime
import os

def getFileName(requset,filename):
  now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename="%s%s"%(now_time,filename)
  return os.path.join('uploads/',new_filename)


class Category(models.Model):
  name=models.CharField(max_length=150,null=False,blank=False)
  image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  description=models.TextField(max_length=500,null=False,blank=False)

 
  def __str__(self) :
    return self.name
 

class FProducts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(max_length=2000)
    fid = models.CharField(max_length=100)
    image_link = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    offer = models.CharField(max_length=100)
    price = models.JSONField(default=list)
    date = models.JSONField(default=list)
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")

    def __str__(self):
        return self.name
    
class AProducts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(max_length=1000)
    aid = models.CharField(max_length=100)
    image_link = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    offer = models.CharField(max_length=100)
    price = models.JSONField(default=list)
    date = models.JSONField(default=list)
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")

    def __str__(self):
        return self.name
    

class Notify(models.Model):
    name=models.CharField(max_length=500)
    image_link=models.CharField(max_length=500)
    url=models.CharField(max_length=1000)
    offer=models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
   