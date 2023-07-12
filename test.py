from ncp.modules import NCP_single

model = NCP_single("ncp/pre/acronimos.json", "ncp/models/")

json = model.pipeline("Carcinoma de mama")

print(json)