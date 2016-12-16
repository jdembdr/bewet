import urllib
from pyquery import PyQuery
import dryscrape
import urlparse
import re

def request_url( type, id=None):
    options = None

    if type == 'club':
        url = 'web/carto/StructureDetail.asp?'
        options = urllib.urlencode({'stcode':id, 'struct':'club', 'annee':''})
    elif type=='club_list':
        url = 'web/carto/Structureliste.asp?'
        options = urllib.urlencode({'dpt':"%.2d"%id, 'struct':'club'})
    elif type == 'regatta':
        url = 'sportif/Calendrier/Fiche_Detail.aspx?'
        options = urllib.urlencode({'id':id})
    elif type == 'calendar_club':
        url = 'sportif/calendrier/calendrier.aspx?'
        options=urllib.urlencode({'st_code':id, 'SecteurPratique':'H', 'Date':'365'})
    elif type == 'calendar':
        url = 'sportif/Calendrier/Calendrier.aspx?search&'
        options = urllib.urlencode({'Date':365})
    elif type == 'licence':
        pass
    elif type =='league_list':
        url = 'web/carto/Structureliste.asp?'
        options = urllib.urlencode({'struct':'ligue'})
    elif type =='league':
        url = 'web/carto/StructureDetail.asp?'
        options = urllib.urlencode({'stcode':id, 'annee':2016, 'struct':'ligue'})

    return "%s%s%s" % (base_url, url, options) if options else "%s%s" % (base_url, url)

def extract_club( html):
    elts = html.children('td')
    club = dict()
    club['name']     = elts[0].text_content()
    club['id']      = urlparse.parse_qs(urlparse.urlparse(elts.eq(0).find('a').attr.href).query)['stcode'][0]
    club['postal']  = elts[1].text_content()
    club['city']    = elts[2].text_content()
    club['phone']   = ''.join(re.findall('(\d+)',elts[3].text))
    club['email']   = elts[4].text
    club['site']    = elts[5].text
    return club

def extract_club_details( id ):
    response = session.visit(request_url('club', id=id))
    body = PyQuery(session.body())

    club=dict()
    club['name'] = body('div#conteneur h1')[0].text_content()
    club['id'] = id

    details_table = body('table.petitcarto tbody')
    club['address'] = details_table('tr').eq(1).find('td').eq(0).find('p').eq(0).text()

    latlon = re.findall('(\d+,\d+)', details_table('tr').eq(1).find('td').eq(0).find('p').eq(1).text())
    if len(latlon) > 1:
        club['lat'] = latlon[0]
        club['long'] = latlon[1]

    contact_fields = details_table('tr').eq(1).find('td').eq(2)

    def extract_contact(i, elt):
        if 'phone' in elt.text_content():
            club['phone'] = ''.join(re.findall('(\d+)',elt.text))
        elif 'Fax' in elt.text_content():
            club['fax'] = ''.join(re.findall('(\d+)',elt.text))
        elif 'Courriel' in elt.text_content():
            club['email'] = re.findall('mailto:([\w\@\.]+)', elt.find('a').attrib['href'])[0]
        elif 'Site' in elt.text_content():
            club['site'] = elt.find('a').attrib['href']
    contact_fields.find('p').map(extract_contact)

    information_fields = details_table('tr').eq(2).find('td').eq(0).find('p')
    club['summary'] = information_fields[0].text
    club['description'] = information_fields[1].text
    club['opening'] = information_fields[2].text

    return club



def ligues():
    result = BeautifulSoup(request_url('league_list'), 'lxml')


def clubs( details=False ):
    clubs = []
    connection = False
    for dpt in range(1, 100):
        response = session.visit(request_url('club_list', id=dpt))
        body = PyQuery(session.body())

        club_tables = body ('table.petitcarto')
        if len(club_tables) >= 2:
            root = club_tables.eq(0).children('tbody tr')
            for i in range(1, len(root)):
                # fast extraction from pri;ary result page
                club = extract_club(root.eq(i))

                if details:
                    # find club unique id: stcode
                    club_href = root.eq(i).children('td').eq(0).find('a').attr.href
                    # extract details from specific description page
                    club.update(extract_club_details(club['id']))

                clubs.append(club)

    return clubs

def calendar(club):
    regattas = []
    response = session.visit(request_url('calendar_club', id=club))
    body = PyQuery(session.body())

    regatta_tables = body('table#ContentPlaceHolder1_GridView1 tbody tr')

    def extract_regatta( html ):
        regatta = dict()
        elts = html.children('td')

        regatta['name'] = elts[2].text_content()
        regatta['id'] = urlparse.parse_qs(urlparse.urlparse(elts.eq(2).find('a').attr.href).query)['id'][0]

        dates = re.findall('[\d\/]+', elts[1].text_content())
        regatta['start'] = dates[0]
        regatta['end'] = dates[1] if len(dates) >1 else dates[0]
        regatta['grade'] = elts[4].text_content()
        regatta['classe'] = elts[5].text_content()
        regatta['club_id'] = club
        return regatta

    regattas = [extract_regatta(regatta_tables.eq(i)) for i in range(1, len(regatta_tables))]
    return regattas


def test():
    print clubs()
    print calendar('10001')

base_url = 'http://www.ffvoile.fr/ffv/'
session = dryscrape.Session(base_url=base_url)
session.set_attribute('auto_load_images',False)

planning = []

import csv
try:
    _clubs = clubs(details=True)
    with open('ffv_clubs.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        infos = ['id', 'name', 'address', 'city', 'postal', 'lat', 'long', 'phone', 'fax', 'email', 'site', 'summary', 'description', 'opening']
        writer.writerow(infos)

        for club in _clubs:
            writer.writerow([ club.get(key).encode('utf8') if club.get(key) else ''  for key in infos] )

    with open('ffv_regattas.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        infos = ['id', 'name', 'club_id', 'start', 'end', 'grade', 'classe']
        writer.writerow(infos)

        for club in _clubs:
            planning_club = calendar(club['id'])
            planning.extend(planning_club)

            for regatta in planning_club:
                writer.writerow([regatta.get(key).encode('utf8') if regatta.get(key) else '' for key in infos] )


    print '%d Clubs'% len(_clubs)
    print '%d Regates'% len(planning)
    for p in planning:
        print p

except Exception, e:
    import traceback
    traceback.print_exc()


