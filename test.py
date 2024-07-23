from ncp.pipelines import NCP
from ncp.models import Note
from globals import *

ncp = NCP(ACRONYMS, GOOD_VALUES, MAMA_MODEL_PATH, NEG_UNCERT_MODEL_PATH)

out = ncp.pipeline(Note(text="Carcinoma de mama ductal infiltrante con tratamiento quimioterapia", ehr=2))

print(out)

# Out
"""
ehr=2 text='Carcinoma de mama ductal infiltrante con tratamiento quimioterapia' 
text_pre='Carcinoma de mama ductal infiltrante con tratamiento quimioterapia' 
creation_date='2024-07-23' entities=[Entity(name='CANCER_CONCEPT', value='Carcinoma'), 
Entity(name='CANCER_LOC', value='mama'), Entity(name='CANCER_TYPE', value='ductal'), 
Entity(name='CANCER_EXP', value='infiltrante'), Entity(name='TRAT', value='quimioterapia')] 
diags=[Diag(concept='carcinoma', date=None, loc='mama', tnm=None, exp='infiltrante', grade=None, type='ductal', subtype=None)] 
treatms=[Treatment(concept='quimioterapia', date=None, drug=None, freq=None, interval=None, quantity=None, schme=None)] metastasis=None recaidas=None

"""
