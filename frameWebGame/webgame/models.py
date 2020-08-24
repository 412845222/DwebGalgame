from django.db import models

# Create your models here.
class Changjing(models.Model):
    name = models.CharField(null=True,blank=True,max_length=200)
    bgimg = models.ImageField(null=True,blank=True,max_length=200)
    belong = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='changjing_children')
    def __str__(self):
        return self.name

class People(models.Model):
    nickName = models.CharField(null=True,blank=True,max_length=200)
    def __str__(self):
        return self.nickName

class People_action(models.Model):
    name = models.CharField(null=True,blank=True,max_length=200)
    bodyimg = models.CharField(null=True,blank=True,max_length=200)
    belong = models.ForeignKey(People,on_delete=models.CASCADE,null=True,blank=True,related_name='action_people')
    def __str__(self):
        return self.name

class Step(models.Model):
    index = models.CharField(null=True,blank=True,max_length=200)
    name = models.CharField(null=True,blank=True,max_length=200)
    people1 = models.ForeignKey(People_action,on_delete=models.CASCADE,null=True,blank=True,related_name='step_people1')
    people2 = models.ForeignKey(People_action,on_delete=models.CASCADE,null=True,blank=True,related_name='step_people2')
    text = models.CharField(null=True,blank=True,max_length=200)
    belong = models.ForeignKey(Changjing,on_delete=models.CASCADE,null=True,blank=True,related_name='step_changjing')
    def __int__(self):
        return self.id