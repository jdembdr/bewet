#!/usr/bin/python
# coding: utf8

import os
from adaptor.model import CsvDbModel, CsvModel
from adaptor.fields import *
from regata.models.club import Club
from regata.models.regata import Regata

class ClubCsvModel(CsvModel):

    """
    02002;
    ASSOCIATION VOILES DU SOISSONNAIS ;
    BASE NAUTIQUE Rue de la vallée 02200 POMMIERS;
    POMMIERS;
    02200;
    49,3906295383024;
    3,26950318252564;
    0323734760;
    ;
    avsoissonnais@gmail.com;
    http://www.avs-soissonnais.org/;
    ;12 activités : école de voile, école de sport et activité sportive. Activité voile traditionnelle et croisière mer. Activité découverte de la rivière. Activité fluviale. Activité de formation permis bateau OEI, OC, hauturière et moniteur voile.;
    """
    club_id = CharField()
    name = CharField()
    address = CharField()
    city = CharField()
    postal = CharField()
    #lat = FloatField(prepare= lambda x: 0 if x == ''  else x)
    #lon = FloatField(prepare= lambda x: 0 if x == ''  else x)
    phone = CharField()
    fax = CharField()
    email = CharField()
    site = CharField()
    summary = CharField()
    description = CharField()
    scheduling = CharField()

    class Meta:
        delimiter=";"
        dbModel = Club
        silent_failure = False
        update = {'keys': ['club_id',]}


class RegataCsvModel(CsvModel):
    regata_id = IntegerField()
    name = CharField()
    club = DjangoModelField(Club)
    start = DateField(format="%Y-%m-%d")
    end = DateField(format="%Y-%m-%d")

    class Meta:
        delimiter=";"
        dbModel = Regata
        slent_failure = True
        exclude = ['tour','jauge','grade','documents']
        update = {'keys': ['regata_id',]}


def import_clubs(csv_file="ffv_clubs.csv"):
    if os.path.exists(csv_file):
        clubs = ClubCsvModel.import_from_filename(csv_file)

def import_regatas(csv_file="ffv_regattas.csv"):
    if os.path.exists(csv_file):
        RegataCsvModel.import_from_filename(csv_file)


def import_all():
    try:
        import_clubs()
        import_regatas()
    except Exception, e:
        import traceback
        traceback.print_exc()
    return
