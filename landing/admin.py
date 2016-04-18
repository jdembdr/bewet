from django.contrib import admin

# Register your models here.
from .models import ExternalMailingListSubscriber

@admin.register(ExternalMailingListSubscriber)
class ExternalMailingListSubscriberAdmin(admin.ModelAdmin):
    fields = ('email','subscription_date',)

