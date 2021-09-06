import json
import os.path
from borza_model import vlagatelj

datoteka = []

db_borza = "borza.json"

def shrani123():
    file = open(db_borza, 'w')
    dic = {
        'uporabniki': [vlagatelj.__dict__ for vlagatelj in datoteka],
        ##
    }
    json.dump(dic, file,indent='  ')
    file.close()



def nalozi():


    if not os.path.isfile(db_borza):
        shrani123()
    file = open(db_borza, 'r')
    dic = json.load(file)
    for p in dic['uporabniki']:
        Vlagatelj = vlagatelj()
        Vlagatelj.__dict__ = p
        datoteka.append(Vlagatelj)
    file.close()
