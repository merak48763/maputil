# https://xkcd.com/1319/

import requests, json, re, math
from pathlib import Path
from tqdm import tqdm
from zipfile import ZipFile
from PIL import Image

VERSION_NAME = "25w10a"
UNIFONT_CHARSET = set(range(256)) | set(ord(c) for c in "")

ROOT_FOLDER = Path("./font_generator_data")
ASSETS_FILENAME = f"cache-{VERSION_NAME}-assets.zip"

def should_unifont_include(codepoint: int):
  #return True
  return codepoint in UNIFONT_CHARSET

def download_github():
  with requests.get(f"https://github.com/misode/mcmeta/archive/refs/tags/{VERSION_NAME}-assets.zip", stream=True) as res:
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

def read_unihex_archive(repo_archive: ZipFile, unihex_zip_path: str, *, width_overrides: dict[int, int]):
  result = width_overrides
  with ZipFile(repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/{unihex_zip_path}")) as unihex_archive:
    for hex_filename in filter(lambda n: n.endswith(".hex"), unihex_archive.namelist()):
      with unihex_archive.open(hex_filename) as unihex_file:
        for unihex_entry in unihex_file.read().decode("utf-8").split("\n"):
          if not unihex_entry:
            continue
          codepoint, glyph = unihex_entry.split(":")
          codepoint = int(codepoint, 16)
          if should_unifont_include(codepoint) and codepoint not in result and codepoint not in [0, ord(" ")]:
            result[codepoint] = pixel_width(glyph)
  return result

def read_bitmap(repo_archive: ZipFile, font_id: str):
  result = {}
  with repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/{font_id}.json") as font_file:
    for provider in json.loads(font_file.read())["providers"]:
      if provider["type"] != "bitmap":
        continue
      png_id = re.sub(r"^minecraft:", "", provider["file"])
      codepoints = provider["chars"]
      height = provider.get("height", 8)
      texture = Image.open(repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/textures/{png_id}")).convert("RGBA")
      row_count = len(codepoints)
      for y, row in enumerate(codepoints):
        col_count = len(row)
        glyph_height = texture.height // row_count
        glyph_width = texture.width // col_count
        for x, codepoint in enumerate(row):
          if ord(codepoint) in [0, ord(" ")]:
            continue
          pos_x = x * glyph_width
          pos_y = y * glyph_height
          for i in range(glyph_width - 1, -1, -1):
            if any(texture.getpixel((pos_x + i, pos_y + j))[3] != 0 for j in range(glyph_height)):
              result[ord(codepoint)] = (i + 1) * height / glyph_height
              break
            result[ord(codepoint)] = 0
  return result

def read_space(repo_archive: ZipFile, font_id: str):
  result = {}
  with repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/{font_id}.json") as space_font_file:
    for provider in json.loads(space_font_file.read())["providers"]:
      if provider["type"] != "space":
        continue
      result |= {ord(k): v for k, v in provider["advances"].items()}
  return result

def pack_number(number: float | int):
  return int(number) if number == int(number) else number

if not ROOT_FOLDER.is_dir():
  ROOT_FOLDER.mkdir()
if not (ROOT_FOLDER / "output").is_dir():
  (ROOT_FOLDER / "output").mkdir()
if not (ROOT_FOLDER / ASSETS_FILENAME).is_file():
  download_github()

unifont_widths = {}
unifont_jp_widths = {}
default_widths = {}
alt_widths = {}
il_alt_widths = {}
space_widths = {}
with ZipFile((ROOT_FOLDER / ASSETS_FILENAME).as_posix()) as asset_archive:
  # Unihex width overrides
  with asset_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/include/unifont.json") as width_override_file:
    # Workaround for MC-278459 (the trailing comma in "Hangul Syllables" range comment field)
    # Why, Mojang? Why?
    fixed_file_content = re.sub(r",\s*]", "]", width_override_file.read().decode("utf-8"))
    for provider in json.loads(fixed_file_content)["providers"]:
      if provider["type"] != "unihex":
        continue
      is_jp_variant = provider.get("filter", {}).get("jp", False)
      for override in provider["size_overrides"]:
        for codepoint in range(ord(override["from"]), ord(override["to"]) + 1):
          if not should_unifont_include(codepoint):
            continue
          if is_jp_variant:
            unifont_jp_widths[codepoint] = override["right"] - override["left"] + 1
          else:
            unifont_widths[codepoint] = override["right"] - override["left"] + 1
  # Unihex
  unifont_widths = read_unihex_archive(asset_archive, "font/unifont.zip", width_overrides=unifont_widths)
  # Unihex JP
  unifont_jp_widths = read_unihex_archive(asset_archive, "font/unifont_jp.zip", width_overrides=unifont_jp_widths)
  # Bitmap
  default_widths = read_bitmap(asset_archive, "include/default")
  alt_widths = read_bitmap(asset_archive, "alt")
  il_alt_widths = read_bitmap(asset_archive, "illageralt")
  # Space
  space_widths = read_space(asset_archive, "include/space")

# Export
uniform_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -(v // 2 + 1) for k, v in sorted(unifont_jp_widths.items(), key=lambda x: x[0]) if v != unifont_widths.get(k, 0)},
      "filter": {
        "jp": True
      }
    },
    {
      "type": "space",
      "advances": {chr(k): -(v // 2 + 1) for k, v in sorted(unifont_widths.items(), key=lambda x: x[0])}
    }
  ]
}
if len(unifont_jp_widths) == 0:
  del uniform_negative["providers"][0]
with open((ROOT_FOLDER / "output/uniform_neg.json").as_posix(), "w") as file:
  json.dump(uniform_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/uniform_neg.json", "w") as file:
  json.dump(uniform_negative, file)

uniform_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): pack_number(-(v // 2 + 1) / 2) for k, v in sorted(unifont_jp_widths.items(), key=lambda x: x[0]) if v != unifont_widths.get(k, 0)},
      "filter": {
        "jp": True
      }
    },
    {
      "type": "space",
      "advances": {chr(k): pack_number(-(v // 2 + 1) / 2) for k, v in sorted(unifont_widths.items(), key=lambda x: x[0])}
    }
  ]
}
if len(unifont_jp_widths) == 0:
  del uniform_half_negative["providers"][0]
with open((ROOT_FOLDER / "output/uniform_half_neg.json").as_posix(), "w") as file:
  json.dump(uniform_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/uniform_half_neg.json", "w") as file:
  json.dump(uniform_half_negative, file)

default_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -(math.ceil(v) + 1) for k, v in sorted(default_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/default_neg.json").as_posix(), "w") as file:
  json.dump(default_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/default_neg.json", "w") as file:
  json.dump(default_negative, file)

default_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): pack_number(-(math.ceil(v) + 1) / 2) for k, v in sorted(default_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/default_half_neg.json").as_posix(), "w") as file:
  json.dump(default_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/default_half_neg.json", "w") as file:
  json.dump(default_half_negative, file)

alt_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -(math.ceil(v) + 1) for k, v in sorted(alt_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/alt_neg.json").as_posix(), "w") as file:
  json.dump(alt_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/alt_neg.json", "w") as file:
  json.dump(alt_negative, file)

alt_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): pack_number(-(math.ceil(v) + 1) / 2) for k, v in sorted(alt_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/alt_half_neg.json").as_posix(), "w") as file:
  json.dump(alt_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/alt_half_neg.json", "w") as file:
  json.dump(alt_half_negative, file)

il_alt_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -(math.ceil(v) + 1) for k, v in sorted(il_alt_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/illageralt_neg.json").as_posix(), "w") as file:
  json.dump(il_alt_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/illageralt_neg.json", "w") as file:
  json.dump(il_alt_negative, file)

il_alt_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): pack_number(-(math.ceil(v) + 1) / 2) for k, v in sorted(il_alt_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/illageralt_half_neg.json").as_posix(), "w") as file:
  json.dump(il_alt_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/illageralt_half_neg.json", "w") as file:
  json.dump(il_alt_half_negative, file)

space_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): -v for k, v in sorted(space_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/space_neg.json").as_posix(), "w") as file:
  json.dump(space_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/space_neg.json", "w") as file:
  json.dump(space_negative, file)

space_half_negative = {
  "providers": [
    {
      "type": "space",
      "advances": {chr(k): pack_number(-v / 2) for k, v in sorted(space_widths.items(), key=lambda x: x[0])}
    }
  ]
}
with open((ROOT_FOLDER / "output/space_half_neg.json").as_posix(), "w") as file:
  json.dump(space_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/space_half_neg.json", "w") as file:
  json.dump(space_half_negative, file)
