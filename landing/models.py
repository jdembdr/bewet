from django.db import models
from django.db.models import EmailField

# Create your models here.
class ExternalMailingListSubscriber(models.Model):
    email = EmailField(blank=False)

    def postsave(self):
    # send email after save
        return
