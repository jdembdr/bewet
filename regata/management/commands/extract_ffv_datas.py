from django.core.management.base import BaseCommand, CommandError
from regata.models.club import Club
from regata.models.regata  import Regata, Class, Grade
from django.contrib.gis.geos import Point
import ffv_extract as F

from datetime import datetime as D

class Command(BaseCommand):
    help = 'Extract datas from FFV site and update DB regatas and clubs tables'

    def add_arguments(self, parser):
        parser.add_argument('dpt_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for dpt_id in options['dpt_id']:
            try:
                clubs = F.get_clubs(dpt_id, details=True)
            except Exception, e:
                raise CommandError('Can\'t retrieve clubs for dpt %s : %s' % (dpt_id, e))


            for _club in clubs:
                print _club
                try:
                    club = Club(pk=_club.pop('club_id'))
                    # extract coordinates from dict and get the Geographical point
                    lat = float(_club.pop('lat', 43))
                    lon = float(_club.pop('lon', 8))

                    _club['position'] = Point(lon, lat)

                    # save club datas
                    for k,v in _club.iteritems():
                        setattr(club, k, v)

                    club.save()
                except Exception, e:
                    raise CommandError('Can\'t save clubs %s for dpt %s: %s'%( _club['club_id'], dpt_id, str(e)))

                try:

                    regatas = F.get_calendar(club.pk)
                    for _regata in regatas:
                        print _regata
                        regata = Regata(pk=_regata.pop('regata_id'), name=_regata['name'], club=club)
                        try:
                            regata.end = D.strptime(_regata['end'],'%d/%m/%Y' )
                        except ValueError:
                            continue

                        try:
                            regata.start = D.strptime(_regata['start'],'%d/%m/%Y' )
                        except ValueError:
                            regata.start = D.strptime(_regata['start'],'%d/%m').replace(regata.end.year)


                        regata.save()

                        #search for grades
                        for _grade in _regata.pop('grade').replace(' ','').split(','):
                            grade = Grade(pk=_grade)
                            grade.save()
                            regata.grades.add(grade)

                        #search for class
                        for _class in _regata.pop('class').replace(' ','').split(','):
                            myclass = Class(pk=_class)
                            myclass.save()
                            regata.classes.add(myclass)



                except Exception, e:
                    raise CommandError('Can\'t save  regatas for club %s : %s'%(club.pk, e))


            self.stdout.write(self.style.SUCCESS('Successfully save club "%s"' % club))


        self.stdout.write(self.style.SUCCESS('Successfully Extract FFV site'))

