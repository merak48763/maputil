import json

filename = "datapack/data/mu/tags/" + input("filename: datapack/data/mu/tags/")
if not filename.endswith(".json"):
  filename += ".json"

with open(filename) as file:
  data = json.load(file)
data["values"] = sorted(data["values"])
with open(filename, "w") as file:
  json.dump(data, file, indent=2)
  file.write("\n")
