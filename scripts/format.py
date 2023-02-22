import json

entities = json.loads(open("./registry/data/osmosis/osmosis-1/contracts.json").read())
sorted_entities = sorted(entities, key=lambda k: k["slug"])

json.dump(sorted_entities, open("./registry/data/osmosis/osmosis-1/contracts.json", "w"), indent=2)
