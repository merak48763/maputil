import json
from zipfile import ZipFile
from PIL import Image
from mcdata import *

registries_path = require_mcdata("registries")

with ZipFile(registries_path) as registries_archive:
  with registries_archive.open(f"mcmeta-{VERSION_NAME}-registries/trim_pattern/data.min.json") as file:
    trim_patterns: list[str] = json.loads(file.read())
  with registries_archive.open(f"mcmeta-{VERSION_NAME}-registries/trim_material/data.min.json") as file:
    trim_materials: list[str] = json.loads(file.read())

Image.new("RGBA", (1, 1), (255, 255, 255, 255)).save("resourcepack/assets/mu/textures/trims/color_palettes/placeholder.png")

empty_elytra_texture = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
for pattern in trim_patterns:
  empty_elytra_texture.save(f"resourcepack/assets/minecraft/textures/trims/entity/wings/{pattern}.png")

paletted_permutations = {
  "type": "paletted_permutations",
  "palette_key": "mu:trims/color_palettes/placeholder",
  "permutations": {material: "mu:trims/color_palettes/placeholder" for material in trim_materials},
  "textures": [f"trims/entity/wings/{pattern}" for pattern in trim_patterns]
}
with open("resourcepack/assets/minecraft/atlases/armor_trims.json", "w") as file:
  json.dump({ "sources": [paletted_permutations] }, file, indent=2)
