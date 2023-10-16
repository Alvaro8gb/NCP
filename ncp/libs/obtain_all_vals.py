import json

def classificator(notes, index_text):
    classificator = nlp.NLP_NER(__MAMA_MODEL_PATH, __NEG_UNCERT_MODEL_PATH)

    samples = { "examples" : { l : [] for l in classificator.get_labels()} }
    for n in notes:
        try:
            ents = classificator.get_ents(n[index_text])
            for e in ents:
                if e.label_ in classificator.get_labels():
                    samples["examples"][e.label_].append(e.text)
        except Exception as e:
            print(e)
            raise e

    for l in samples["examples"]:
        samples["examples"][l] = list(set(samples["examples"][l]))

    with open("examples.json", "w") as f:
        json.dump(samples, f, indent=4)

    return classificator.get_labels()
