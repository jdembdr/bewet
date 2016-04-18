from django.db import models
from django.db.models import EmailField, DateField

# Create your models here.
class ExternalMailingListSubscriber(models.Model):
    email = EmailField(blank=False)
    subscription_date = DateField()


    def __str__(self):
        return self.email

    def postsave(self):
    # send email after save
        return
