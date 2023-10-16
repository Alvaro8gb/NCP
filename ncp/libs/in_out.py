import csv
import json
from pymongo import MongoClient

from datetime import datetime
from models import Note
from typing import List

def load_db(in_path:str)-> List[Note]:
    notes = []
    with open(in_path) as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quoting = csv.QUOTE_ALL)
                cols = reader.__next__() #omitimos los nombres de las columnas
                #notes_index = { col : cols.index(col) for col in cols }

                notes = [ Note(text=text, ehr=ehr, creation_date=datetime.strptime(creation_date, "%Y-%m-%d").isoformat()) for id_note, ehr, creation_date, text, template, service in reader]

    return notes

def dump2files(struct_notes:List[Note], out_path:str):
    out_path_no_diags = out_path + "/no_diags/"
    out_path_multiple_diags = out_path +"/multiple/"
    out_path_one_diag = out_path + "/one_diag/"

    for n in struct_notes:
        
        if n.events != None:
            n_events = len(n.events)

            if n_events > 1:
                path = out_path_multiple_diags
            else: 
                path = out_path_one_diag 
        else :
            path = out_path_no_diags

        path += str(n.ehr)

        with open(path + ".json","w") as f:
            json.dump(n.dict(), f, indent=4)


def dump2mongo_db(struct_notes):

    client = MongoClient(port=27017)
    collection = client.Clarify.Prueba_1

    for good, info in struct_notes:
        collection.insert_one(info)

