from ncp.pipelines import NCP_single

model = NCP_single("ncp/pre/acronimos.json", "ncp/models/")

model.pipeline("Carcinoma de mama")