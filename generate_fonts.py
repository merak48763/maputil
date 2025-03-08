import requests, json, re
from pathlib import Path
from tqdm import tqdm
from zipfile import ZipFile

VERSION_NAME = "25w10a"
ASSETS_URL = f"https://github.com/misode/mcmeta/archive/refs/tags/{VERSION_NAME}-assets.zip"
ROOT_FOLDER = Path("./font_generator_data")
ASSETS_FILENAME = f"cache-{VERSION_NAME}-assets.zip"

if not (ROOT_FOLDER / ASSETS_FILENAME).is_file():
  with requests.get(ASSETS_URL, stream=True) as res:
    res.raise_for_status()
    with open((ROOT_FOLDER / ASSETS_FILENAME).as_posix(), "wb") as file:
      with tqdm(unit="B", unit_scale=True, desc=f"Downloading {VERSION_NAME}-assets") as progress:
        for chunk in res.iter_content(chunk_size=16384):
          progress.update(len(chunk))
          file.write(chunk)

def pixel_width(glyph: str):
  row_width = len(glyph) // 16
  mask = 0
  for i in range(16):
    row = glyph[i * row_width: i * row_width + row_width]
    mask |= int(row, 16)
  if mask == 0:
    return len(glyph) // 4
  return len(f"{mask:032b}".strip("0"))

widths = {}
with ZipFile((ROOT_FOLDER / ASSETS_FILENAME).as_posix()) as asset_archive:
  with asset_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/include/unifont.json") as width_override_file:
    # Workaround for the trailing comma in "Hangul Syllables" range comment field
    # Why, Mojang? Why?
    fixed_file_content = re.sub(r",\s*]", "]", width_override_file.read().decode("utf-8"))
    for provider in json.loads(fixed_file_content)["providers"]:
      if provider["type"] != "unihex":
        continue
      for override in provider["size_overrides"]:
        for codepoint in range(ord(override["from"]), ord(override["to"]) + 1):
          widths[codepoint] = override["right"] - override["left"] + 1
  with ZipFile(asset_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/unifont.zip")) as unifont_archive:
    for hex_filename in filter(lambda n: n.endswith(".hex"), unifont_archive.namelist()):
      with unifont_archive.open(hex_filename) as unihex_file:
        for unihex_entry in unihex_file.read().decode("utf-8").split("\n"):
          if not unihex_entry:
            continue
          codepoint, glyph = unihex_entry.split(":")
          codepoint = int(codepoint, 16)
          if codepoint not in widths:
            widths[codepoint] = pixel_width(glyph)

uniform_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -(v // 2 + 1) for k, v in sorted(widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "uniform_neg.json").as_posix(), "w") as file:
  json.dump(uniform_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/uniform_neg.json", "w") as file:
  json.dump(uniform_negative, file)

def half_neg_width(width: int):
  result = -(width // 2 + 1) / 2
  return int(result) if result == int(result) else result
uniform_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): half_neg_width(v) for k, v in sorted(widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "uniform_half_neg.json").as_posix(), "w") as file:
  json.dump(uniform_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/uniform_half_neg.json", "w") as file:
  json.dump(uniform_half_negative, file)
