from django.db import models

# Create your models here.

class maindata(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=1024)
    status = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    def __str__(self):
        return self.name
    

class service(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class user(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class group(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class project(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
