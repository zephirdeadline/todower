from django.db import models

# Create your models here.


class Day(models.Model):
    date = models.DateField(auto_created=True)
    member = models.ForeignKey('login.Member', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)


class List(models.Model):
    progress = models.IntegerField(default=1)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.day) + str(self.progress)


class Task(models.Model):
    text = models.CharField(max_length=64)
    priority = models.IntegerField(default=5)
    list = models.ForeignKey(List, models.CASCADE)
    date_end = models.DateField(null=True, blank=True)
    coment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text
