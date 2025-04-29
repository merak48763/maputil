import json, re

class TagEncoder(json.JSONEncoder):
  OPTIONAL_ENTRY_PATTERN = re.compile(r"\{\s*\"id\":\s*\"(\w+)\",\s*\"required\":\s*false\s*\}")
  def encode(self, obj):
    json_repr = super().encode(obj)
    return TagEncoder.OPTIONAL_ENTRY_PATTERN.sub(r'{"id": "\g<1>", "required": false}', json_repr)

filename = "datapack/data/mu/tags/" + input("filename: datapack/data/mu/tags/")
if not filename.endswith(".json"):
  filename += ".json"

with open(filename) as file:
  data = json.load(file)
data["values"] = sorted(data["values"], key=lambda v: v if type(v) is str else v["id"])
with open(filename, "w") as file:
  file.write(json.dumps(data, indent=2, cls=TagEncoder))
  file.write("\n")
