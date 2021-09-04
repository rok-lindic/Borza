###MODEL

####ne moreš prodat preveč

#import db_borza
#import os.path

import urllib.request, json
from datetime import datetime, timedelta
import sys

#datoteka = []

#vrednostni_papirji =[]


#url = 'https://rest.ljse.si/web/Bvt9fe2peQ7pwpyYqODM/price-list/XLJU/2021-08-27/json'
url = 'https://rest.ljse.si/web/Bvt9fe2peQ7pwpyYqODM/price-list/XLJU/'+'2021-08-27'+'/json'
response = urllib.request.urlopen(url)
data = json.loads(response.read())##potegne z neta podatke
#print(round(float(data['securities'][1]['close_price'])*5,3))
datum = datetime.today().strftime('%Y-%m-%d')
#print(datetime.today()-timedelta(days=2))
#print(datetime.today().weekday())
#for i in range(len(data['securities'])):
#    if data['securities'][i]['symbol']=='KRKG':
#        print(data['securities'][i]['close_price'])

#db_borza='borza.json'
"""
def shrani():
    file = open(db_borza, 'w')
    dic = {
        'uporabniki': [vlagatelj.__dict__ for vlagatelj in datoteka],
        ###'vrednostni_papirji':[igralec.__dict__ for igralec in nekajnekaj]
    }
    json.dump(dic, file,indent='  ')
    file.close()
"""
def danasnji_dan():
    if datetime.today().weekday() == 6:
        datum = datetime.today()-timedelta(days=2)
    elif datetime.today().weekday() == 5:
        datum = datetime.today()-timedelta(days=1)
    else:
        datum = datetime.today()
    return datum.date()

def izbrani_datum(dan):
    if datetime.strptime(dan.replace(' ',''), '%d.%m.%Y').weekday() == 6:
        izbrani_dan = datetime.strptime(dan.replace(' ',''), '%d.%m.%Y')-timedelta(days=2)
    elif datetime.strptime(dan.replace(' ',''), '%d.%m.%Y').weekday() == 5:
        izbrani_dan = datetime.strptime(dan.replace(' ',''), '%d.%m.%Y')-timedelta(days=1)
    else:
        izbrani_dan = datetime.strptime(dan.replace(' ',''), '%d.%m.%Y')
    return izbrani_dan.date()

def podatki_danes():
    if datetime.today().weekday() == 6:
        podatki = url + str(datetime.today()-timedelta(days=2)) + '/json'
    elif datetime.today().weekday() == 5:
        podatki = url + str(datetime.today()-timedelta(days=1)) + '/json'
    else:
        podatki = url + str(datetime.today()) + '/json'
    return podatki
podatki= podatki_danes()

class vlagatelj:

    def __init__(self, ime=None, geslo=None, transakcije=None):
            self.ime = ime
            self.geslo = geslo
            self.transakcije = transakcije
            
    def shrani_uporabnika(self, datoteka):      
        zeobstaja=False  
        for uporabnik in datoteka:
            if uporabnik.ime == self.ime:
                zeobstaja=True#uporabnik že obstaja
        if zeobstaja==True:
            return False #ze obstaja
        else:    
            datoteka.append(self)
        
    ####shrani()
    
    def poisci_ime(self, datoteka):
        if datoteka == []:
            print('xxxxxxx')
            return 0
        else:
            for vlagatelj in datoteka:
                if vlagatelj.ime == self.ime:
                    return datoteka.index(self)
    

    def preveri_uporabnika(self, geslo):
        if geslo == self.geslo():
            return True
        else:
            return False

    def dobi_podatke (self, datoteka):
        for i in range(len(datoteka)):
            if datoteka[i][0]==self.ime:
                return self
#        return self.ime, self.geslo, datoteka[self.ime]
#    def poisci_ime(self):
#        for i in range(len(datoteka)):
#            if datoteka[i][0]==self.ime:
#                return i

##['janez','janezovo_geslo',[janezova_trasakcija1, janezova_transakcija2,...]]
##janezova_transakcija1=[st_papirjev, oznaka, datum, vrednost, stanje ###st_papirjev_zdaj###, saldo]
    def dodaj_v_dat(self, datoteka):
        datoteka.append(self)
        #print(datoteka)
        #shrani()

    def vnesi_transakcijo(self, st_papirjev, simbol, datum, datoteka):
        danes = danasnji_dan()
        datum = izbrani_datum(datum)
        if danes >= datum:
            url = 'https://rest.ljse.si/web/Bvt9fe2peQ7pwpyYqODM/price-list/XLJU/'+ str(datum) + '/json'
        else:
            return False
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        nr=0
        stanje = 0
        saldo = 0
        for n in range(len(data['securities'])):
            if data['securities'][n]['symbol']==simbol:
                nr= n
        for uporabnik in datoteka:
            if uporabnik.ime == self.ime:
                if uporabnik.transakcije != []:
                    i = (len(uporabnik.transakcije) - 1)
                    while i>-1 and uporabnik.transakcije[i][1] != simbol:
                        i -= 1
                    if uporabnik.transakcije[i][1] == simbol:
                        saldo = uporabnik.transakcije[i][5]
                        stanje = uporabnik.transakcije[i][4]
        
        stanje = stanje + int(st_papirjev)
        if stanje >= 0:
            vrednost = round(float(data['securities'][nr]['close_price']),2)
            saldo = saldo - vrednost * st_papirjev                     
            
            for uporabnik in datoteka:
                if uporabnik.ime == self.ime:
                    uporabnik.transakcije.append([st_papirjev, simbol, str(datum), vrednost, stanje, saldo])
        else:
            return False

#        shrani()


    def trenutni_portfelj(self, datoteka):#izpiše simbol, št enot, današnja vrendost ### self ###
        
        portfelj = dict()
        datum = danasnji_dan()
        url = 'https://rest.ljse.si/web/Bvt9fe2peQ7pwpyYqODM/price-list/XLJU/'+ str(datum) + '/json'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        nr = 0
        vrednost = 0
        for uporabnik in datoteka:
            if uporabnik.ime == self.ime:
                for transakcija in uporabnik.transakcije[::-1]:
                    if transakcija[1] not in portfelj:
                        for n in range(len(data['securities'])):
                            if data['securities'][n]['symbol']==transakcija[1]:
                                nr= n
                        vrednost = round(float(data['securities'][nr]['close_price']),2)
                        portfelj[transakcija[1]]=[transakcija[4], vrednost, round(float(vrednost * transakcija[4]),2)]
        return portfelj
        
    def stanje(self, datoteka) :#vrednost portfelja
        stanje = 0
        vrednost = 0
        nr = 0
        datum = danasnji_dan()
        url = 'https://rest.ljse.si/web/Bvt9fe2peQ7pwpyYqODM/price-list/XLJU/'+ str(datum) + '/json'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        for oseba in datoteka:
            if oseba.ime == self.ime:
                for vrednostni_papir in oseba.trenutni_portfelj(datoteka):
                    
                    for n in range(len(data['securities'])):
                            if data['securities'][n]['symbol']==vrednostni_papir:
                                nr= n
                    vrednost = round(float(data['securities'][nr]['close_price']),2)
                    stanje += round(float(oseba.trenutni_portfelj(datoteka)[vrednostni_papir][0] * vrednost),2)
                    
        return stanje
    
    def vplacila(self, datoteka):
        vplacila = 0
        for oseba in datoteka:
            if oseba.ime == self.ime:
                for transakcija in oseba.transakcije:
                    if transakcija[0] > 0:
                        vplacila += round(float(transakcija[0] * transakcija[3]),2)
        return vplacila
    
    def izplacila(self, datoteka):
        izplacila = 0
        for oseba in datoteka:
            if oseba.ime == self.ime:
                for transakcija in oseba.transakcije:
                    if transakcija[0] < 0:
                        izplacila += round((-float(transakcija[0]) * transakcija[3]),2)
        return izplacila


    def profit(self, datoteka):#izplacila - vplacila + vrednost 
        profit = 0
        for oseba in datoteka:
            if oseba.ime == self.ime:
                profit = oseba.izplacila(datoteka) - oseba.vplacila(datoteka) + oseba.stanje(datoteka)
        return profit
    
    def donosnost(self, datoteka):
        donosnost = 0
        for oseba in datoteka:
            if oseba.ime == self.ime:
                try:
                    donosnost = round((oseba.profit(datoteka) / oseba.vplacila(datoteka)),2)
                except ZeroDivisionError:
                    return 0.0
        return donosnost
    
def povprecje(datoteka):
    povprecje = 0
    skupna_donosnost = 0
    osebe = 0
    for oseba in datoteka:
        skupna_donosnost += oseba.donosnost(datoteka)
        osebe += 1
    return round((skupna_donosnost / osebe),2)