from django.db import models

# Create your models here.
class Instructor(models.Model):
    insId = models.CharField(max_length=20, primary_key=True)
    insName = models.CharField(max_length=100)
    insIc = models.CharField(max_length=100)
    insEmail = models.EmailField()
    insNumber = models.CharField(max_length=20, default=0)

class Program(models.Model):
    progTitle = models.CharField(max_length=100)
    progDescription = models.TextField()
    progDate = models.DateField()
    progTime = models.TimeField()
    progInstructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    progVenue = models.CharField(max_length=50)
    progCapacity = models.IntegerField()
    progRegistration = models.BooleanField(default=False)

class Registration(models.Model):
    regName = models.CharField(max_length=100)
    regIc = models.CharField(max_length=100)
    regEmail = models.EmailField()
    regProgram = models.ForeignKey(Program, on_delete=models.CASCADE)

class Feedback(models.Model):
    feedName = models.CharField(max_length=100)
    feedMessage = models.TextField()
    feedProgram = models.ForeignKey(Program, on_delete=models.CASCADE)

