import json
from ncp.post.ent_normalizers import Molec_Normalize as m

samples_path = "test/ent_samples.json"
with open(samples_path, "r") as samples_f:
    samples_j = json.load(samples_f)
    markers = [[marker] for marker in samples_j["MOLEC_MARKER"]]

markers = markers[30:60]
mn =  m.Molec_Normalize()

print("\n====================")
print("TOTAL: ", len(markers))
print("====================\n")

for m in markers:
    print("\n====================")
    result = {
        "old": m,
        "new": mn.normalize(m)
    }
    
    print(json.dumps(result, indent=4))
    print("====================\n")
