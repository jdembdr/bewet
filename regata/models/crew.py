from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_profile( sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        userProfile = Crew(user=user)
        userProfile.save()

post_save.connect(create_profile, sender=User)

# Create your models here.
class CrewRole(models.Model):
    name = models.CharField(max_length=30)

class Language(models.Model):
    language = models.CharField(max_length=10)

class Crew(models.Model):
    # subscription
    # name
    MALE = 'BOY'
    FEMALE = 'GIR'
    GENDER_CHOICE = (
            ( MALE, _('boy')),
            ( FEMALE, _('girl'))
            )


    BEGINNER='BEG'
    INTERMEDIATE='INT'
    EXPERIMENTED='EXP'
    PROFESSIONAL='PRO'
    LEVEL_CHOICE=(
            ( BEGINNER, _('beginner')),
            ( INTERMEDIATE, _('occasional')),
            ( EXPERIMENTED, _('expert')),
            ( PROFESSIONAL, _('professional'))
            )

    SKIPPER='SKP'
    NUM_1='NB1'
    NUM_2='NB2'
    BARREUR='BAR'
    TACTICIAN = 'TAC'
    NAVIGATOR = 'NAV'
    MAINSAIL = 'MNS'
    WINCHER = 'WCH'
    FRONTSAIL = 'FTS'
    COMPETENCE_CHOICE=(
            ( SKIPPER, _('skipper')),
            ( BARREUR, _('sailor')),
            ( NUM_1, _('number 1')),
            ( NUM_2, _('number 2/Pitman')),
            ( TACTICIAN, _('tactician')),
            ( NAVIGATOR, _('navigator')),
            ( MAINSAIL, _('mainsail')),
            ( WINCHER, _('wincher')),
            ( FRONTSAIL, _('frontsail')),
            )

    picture = models.ImageField(upload_to='documents/%Y/%m/%d', default='default.png', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
            max_length=3,
            blank=True,
            null=True,
            choices=GENDER_CHOICE)

    size = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    licence_id = models.IntegerField(blank=True, null=True)
    isaf_id = models.IntegerField(blank=True, null=True)

    level = models.CharField(
            max_length=3,
            choices=LEVEL_CHOICE,
            default=BEGINNER, null=True)

    description = models.TextField(null=True, blank=True)
    best_results = models.TextField(null=True, blank = True)

    language = models.ManyToManyField(Language, blank=True)
    user = models.OneToOneField(User)

