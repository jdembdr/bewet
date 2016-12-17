import urllib
from pyquery import PyQuery
import dryscrape
import urlparse
import re
import time
import csv
from optparse import OptionParser

session = None

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            global session
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    print "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    time.sleep(mdelay)
                    dryscrape.stop_xvfb()
                    session = None
                    mtries -= 1
                    mdelay *= backoff
                    lastException = e
            raise lastException
        return f_retry # true decorator
    return deco_retry


@retry(Exception, tries=3)
def request_body(url):
    global session
    if session is None:
        dryscrape.start_xvfb()
        session = dryscrape.Session(base_url="http://www.ffvoile.fr/ffv/")
        session.set_attribute("auto_load_images",False)

    response = session.visit(url)
    body = PyQuery(session.body())
    return body

def request_url( type, id=None):
    options = None

    if type == "club":
        url = "web/carto/StructureDetail.asp?"
        options = urllib.urlencode({"stcode":id, "struct":"club", "annee":""})
    elif type=="club_list":
        url = "web/carto/Structureliste.asp?"
        options = urllib.urlencode({"dpt":"%.2d"%id, "struct":"club"})
    elif type == "regatta":
        url = "sportif/Calendrier/Fiche_Detail.aspx?"
        options = urllib.urlencode({"id":id})
    elif type == "calendar_club":
        url = "sportif/calendrier/calendrier.aspx?"
        options=urllib.urlencode({"st_code":id, "SecteurPratique":"H", "Date":"365"})
    elif type == "calendar":
        url = "sportif/Calendrier/Calendrier.aspx?search&"
        options = urllib.urlencode({"Date":365})
    elif type == "licence":
        pass
    elif type =="league_list":
        url = "web/carto/Structureliste.asp?"
        options = urllib.urlencode({"struct":"ligue"})
    elif type =="league":
        url = "web/carto/StructureDetail.asp?"
        options = urllib.urlencode({"stcode":id, "annee":2016, "struct":"ligue"})

    return "%s%s" % (url, options) if options else url

def extract_club( html):
    elts = html.children("td")
    club = dict()
    club["name"]     = elts[0].text_content()
    club["id"]      = urlparse.parse_qs(urlparse.urlparse(elts.eq(0).find("a").attr.href).query)["stcode"][0]
    club["postal"]  = elts[1].text_content()
    club["city"]    = elts[2].text_content()
    club["phone"]   = "".join(re.findall("(\d+)",elts[3].text))
    club["email"]   = elts[4].text
    club["site"]    = elts[5].text
    return club

def extract_club_details( id ):
    body = request_body(request_url("club", id=id))

    club=dict()
    club["name"] = body("div#conteneur h1")[0].text_content()
    club["id"] = id

    details_table = body("table.petitcarto tbody")
    club["address"] = details_table("tr").eq(1).find("td").eq(0).find("p").eq(0).text()

    latlon = re.findall("(\d+,\d+)", details_table("tr").eq(1).find("td").eq(0).find("p").eq(1).text())
    if len(latlon) > 1:
        club["lat"] = latlon[0]
        club["long"] = latlon[1]

    contact_fields = details_table("tr").eq(1).find("td").eq(2)

    def extract_contact(i, elt):
        if "phone" in elt.text_content():
            club["phone"] = "".join(re.findall("(\d+)",elt.text))
        elif "Fax" in elt.text_content():
            club["fax"] = "".join(re.findall("(\d+)",elt.text))
        elif "Courriel" in elt.text_content():
            club["email"] = re.findall("mailto:([\w\@\.]+)", elt.find("a").attrib["href"])[0]
        elif "Site" in elt.text_content():
            club["site"] = elt.find("a").attrib["href"]
    contact_fields.find("p").map(extract_contact)

    information_fields = details_table("tr").eq(2).find("td").eq(0).find("p")
    club["summary"] = information_fields[0].text
    club["description"] = information_fields[1].text
    club["opening"] = information_fields[2].text

    return club



def get_clubs(dpt, details=False ):
    clubs = []

    print "Retrieve Clubs for dpt %d"%dpt
    body = request_body(request_url("club_list", id=dpt))

    club_tables = body ("table.petitcarto")
    if len(club_tables) >= 2:
        root = club_tables.eq(0).children("tbody tr")
        for i in range(1, len(root)):
            # fast extraction from pri;ary result page
            club = extract_club(root.eq(i))

            if details:
                # extract details from specific description page
                club.update(extract_club_details(club["id"]))

            clubs.append(club)

    return clubs

def get_calendar(club):
    regattas = []
    print "Retrieve Regattas for club %s"%club
    body = request_body(request_url("calendar_club", id=club))

    regatta_tables = body("table#ContentPlaceHolder1_GridView1 tbody tr")

    def extract_regatta( html ):
        regatta = dict()
        elts = html.children("td")

        regatta["name"] = elts[2].text_content()
        regatta["id"] = urlparse.parse_qs(urlparse.urlparse(elts.eq(2).find("a").attr.href).query)["id"][0]

        dates = re.findall("[\d\/]+", elts[1].text_content())
        regatta["start"] = dates[0]
        regatta["end"] = dates[1] if len(dates) >1 else dates[0]
        regatta["grade"] = elts[4].text_content()
        regatta["classe"] = elts[5].text_content()
        regatta["club_id"] = club
        return regatta

    regattas = [extract_regatta(regatta_tables.eq(i)) for i in range(1, len(regatta_tables))]
    return regattas



def write_csv( output, headers, elts):
    with open( output, "ab") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(headers)

        for elt in elts:
            writer.writerow([ elt.get(key).encode("utf8") if elt.get(key) else ""  for key in headers] )


def ffv_vacuum(dpt_list=range(0,100), output_format="csv", regattas_file=None, clubs_file=None, details=False):
    try:
        clubs = []
        for dpt in dpt_list:
            clubs.extend(get_clubs(dpt, details = details))

        planning = []
        for club in clubs:
            planning.extend(get_calendar(club["id"]))

        if clubs_file is not None:
            infos = ["id", "name", "address", "city", "postal", "lat", "long", "phone", "fax", "email", "site", "summary", "description", "opening"]
            write_csv(clubs_file, infos, clubs)

        if regattas_file is not None:
            infos = ["id", "name", "club_id", "start", "end", "grade", "classe"]
            write_csv(regattas_file, infos, planning)


        print "%d Clubs"% len(clubs)
        print "%d Regates"% len(planning)

    except Exception, e:
        import traceback
        traceback.print_exc()

def parse_dpt(option, opt_str, value, parser):
    values = value.split(',')
    result = []

    for val in values[:]:
        if '-' in val:
            a,b = map(int, val.split('-'))
            result.extend(range(int(a),int(b)+1))
        else:
            result.append(int(val))
    if hasattr(parser.values, 'departments_list'):
        parser.values.departments_list.extend(result)
    else :
        parser.values.departments_list= result


def main():
    parser = OptionParser()
    parser.add_option("--details", action="store_true")
    parser.add_option("--output-clubs", type="string")
    parser.add_option("--output-regattas", type="string")
    parser.add_option("-d", "--departments", action="callback", type="string",
            callback=parse_dpt,
            help="specify departments number separated by comma. range are accepted by using -. ex: 13,10,9,20-30")

    (options, args) = parser.parse_args()

    ffv_vacuum(
            dpt_list = options.departments_list,
            regattas_file = options.output_regattas,
            clubs_file = options.output_clubs,
            details = options.details)



if __name__ == "__main__":
    main()

