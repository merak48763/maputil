import json, re

class TagEncoder(json.JSONEncoder):
  OPTIONAL_ENTRY_RE = r'\{\s+"id":\s"(\w+)",\s+"required":\sfalse\s+\}'
  SIMPLIFIED_OPTIONAL_ENTRY = r'{"id": "\g<1>", "required": false}'
  def encode(self, obj):
    json_repr = super().encode(obj)
    return re.sub(TagEncoder.OPTIONAL_ENTRY_RE, TagEncoder.SIMPLIFIED_OPTIONAL_ENTRY, json_repr)

filename = "datapack/data/mu/tags/" + input("filename: datapack/data/mu/tags/")
if not filename.endswith(".json"):
  filename += ".json"

with open(filename) as file:
  data = json.load(file)
data["values"] = sorted(data["values"], key=lambda v: v if type(v) is str else v["id"])
with open(filename, "w") as file:
  file.write(json.dumps(data, indent=2, cls=TagEncoder))
  file.write("\n")
