
from bottle import route, run, static_file, template, request, response, redirect
import borza_db
from borza_model import vlagatelj
import borza_model





@route('/nov_uporabnik', method = 'POST')
def logiranje():
    uporabnik = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    rezultat=''
    if uporabnik=='' or geslo=='':
        rezultat='Za kreiranje novega računa obvezno vnesite uporabniško ime in geslo.'
    else:
        uporabnisko_ime = None
        geslo_uporabnika = None

        i = (len(borza_db.datoteka)-1)
        while i > -1 and borza_db.datoteka[i].ime != uporabnik:
            i -= 1
        if i == -1:
            nov_clovek = vlagatelj(uporabnik, geslo,[])
            borza_db.datoteka.append(nov_clovek)    
            borza_db.shrani123()
            response.set_cookie('user', uporabnik)
            return template('portfelj.html',ime_uporabnika = nov_clovek.ime, transakcije=nov_clovek.transakcije, podatki_uporabnika = nov_clovek.trenutni_portfelj(borza_db.datoteka), rezultat='Uporabnik uspešno kreiran.', povprecje=borza_model.povprecje(borza_db.datoteka), donosnost=nov_clovek.donosnost(borza_db.datoteka), stanje=nov_clovek.stanje(borza_db.datoteka))
        else:
            rezultat='Uporabnik s tem uporabniškim imenom že obstaja. Vnesite drugo ime.'
    
    if rezultat != '':
        return template('index_borza.html', datoteka = borza_db.datoteka, rezultat=rezultat)
    

@route('/logiranje', method = 'POST')
def logiranje():
    uporabnik = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    
    
    for oseba in borza_db.datoteka:
        if oseba.ime == uporabnik and oseba.geslo==geslo:
            response.set_cookie('user', uporabnik)
            return template('portfelj.html',ime_uporabnika = oseba.ime, podatki_uporabnika = oseba.trenutni_portfelj(borza_db.datoteka), transakcije = oseba.transakcije, rezultat='', povprecje=borza_model.povprecje(borza_db.datoteka), donosnost=oseba.donosnost(borza_db.datoteka), stanje=oseba.stanje(borza_db.datoteka))   
    

    return template('index_borza.html', datoteka = borza_db.datoteka, rezultat='Uporabnik s tem uporabniškim imenom in geslom ne obstaja.')

    
@route('/', method = 'GET')
def index():
    return template('index_borza.html', datoteka = borza_db.datoteka, rezultat='')
##Vnasanje nove transakcije
@route('/vnos', method = 'POST')
def vnos_post():
    rezultat = ''
    simbol = request.forms.get('simbol')
    vrsta_posla = request.forms.get('vrsta_posla')
    kolicina = request.forms.get('kolicina', type=int) 
    if vrsta_posla=='prodaja':
        kolicina = -kolicina
    
    datum = request.forms.get('datum')
    user = request.cookies.get('user')
    
    for oseba in borza_db.datoteka:
        if oseba.ime == user:
            try:
                borza_model.izbrani_datum(datum)
            except ValueError:
                rezultat='Prosim vnesi veljaven datum'

            if rezultat == '':
                if oseba.vnesi_transakcijo(kolicina, simbol, datum, borza_db.datoteka)==False:
                    rezultat = 'Vnos transakcije ni uspel.'
                else:
                    rezultat = 'Vnos transakcije je uspel.'
                    borza_db.shrani123()
            return template('portfelj.html',ime_uporabnika = oseba.ime, podatki_uporabnika = oseba.trenutni_portfelj(borza_db.datoteka), transakcije = oseba.transakcije, rezultat=rezultat, povprecje=borza_model.povprecje(borza_db.datoteka), donosnost=oseba.donosnost(borza_db.datoteka), stanje=oseba.stanje(borza_db.datoteka))


@route('/odjava', method = 'POST')
def odjava():
    response.delete_cookie('user')
    return template('index_borza.html', datoteka = borza_db.datoteka, rezultat='Odjava je uspela')


borza_db.nalozi()
run(host='localhost', port=8080, debug=True)
