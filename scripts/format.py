import json

entities = json.loads(open("./registry/data/entities.json").read())
sorted_entities = sorted(entities, key=lambda k: k["name"])

json.dump(sorted_entities, open("./registry/data/entities.json", "w"), indent=2)
