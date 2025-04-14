# https://xkcd.com/1319/

import json, re, math
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
from mcdata import *

OUTPUT_FOLDER = Path("./generator_data/font_output")

unifont_charset = set(range(256))
INCLUDE_ALL_CODEPOINTS = False

def build_charset(repo_archive: ZipFile, /):
  filename_pattern = re.compile(r".*/assets/minecraft/lang/[a-z]+_[a-z]+\.json")
  key_patterns = [re.compile(r"key\.keyboard\..+")]
  for lang_filename in repo_archive.namelist():
    if not filename_pattern.match(lang_filename):
      continue
    with repo_archive.open(lang_filename) as lang_file:
      translation = json.loads(lang_file.read())
      unifont_charset.update(ord(c) for k, v in translation.items() if any(p.match(k) for p in key_patterns) for c in v)
  default_font = json.loads(repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/minecraft/font/include/default.json").read())["providers"]
  for provider in default_font:
    if provider["type"] == "bitmap":
      unifont_charset.update(ord(c) for row in provider["chars"] for c in row)

def pixel_width(glyph: str, /):
  row_width = len(glyph) // 16
  mask = 0
  for i in range(16):
    row = glyph[i * row_width: i * row_width + row_width]
    mask |= int(row, 16)
  if mask == 0:
    return len(glyph) // 4
  return len(f"{mask:032b}".strip("0"))

def read_unihex_archive(repo_archive: ZipFile, /, unihex_zip_id: str, *, width_overrides: dict[int, int]):
  result = width_overrides
  namespace, path = resource_location(unihex_zip_id)
  with ZipFile(repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/{namespace}/{path}")) as unihex_archive:
    for filename in unihex_archive.namelist():
      if not filename.endswith(".hex"):
        continue
      with unihex_archive.open(filename) as unihex_file:
        for unihex_entry in unihex_file.read().decode("utf-8").split("\n"):
          if not unihex_entry:
            continue
          codepoint, glyph = unihex_entry.split(":")
          codepoint = int(codepoint, 16)
          if should_unifont_include(codepoint) and codepoint not in result and codepoint not in [0, ord(" ")]:
            result[codepoint] = pixel_width(glyph)
  return result

def read_bitmap(repo_archive: ZipFile, /, font_id: str):
  result = {}
  namespace, path = resource_location(font_id)
  with repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/{namespace}/font/{path}.json") as font_file:
    for provider in json.loads(font_file.read())["providers"]:
      if provider["type"] != "bitmap":
        continue
      png_namespace, png_path = resource_location(provider["file"])
      codepoints = provider["chars"]
      height = provider.get("height", 8)
      texture = Image.open(repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/{png_namespace}/textures/{png_path}")).convert("RGBA")
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

def read_space(repo_archive: ZipFile, /, font_id: str):
  result = {}
  namespace, path = resource_location(font_id)
  with repo_archive.open(f"mcmeta-{VERSION_NAME}-assets/assets/{namespace}/font/{path}.json") as space_font_file:
    for provider in json.loads(space_font_file.read())["providers"]:
      if provider["type"] != "space":
        continue
      result |= {ord(k): v for k, v in provider["advances"].items()}
  return result

def resource_location(namespaced_id: str):
  m = re.match(r"^(?:([a-z0-9_.]*):)?([a-z0-9_./]+)$", namespaced_id)
  if m:
    return (m.group(1) or "minecraft", m.group(2))
  raise ValueError(f"Invalid resource location {namespaced_id}")

def should_unifont_include(codepoint: int, /):
  return INCLUDE_ALL_CODEPOINTS or codepoint in unifont_charset

def pack_number(number: float | int, /):
  return int(number) if number == int(number) else number

if not OUTPUT_FOLDER.is_dir():
  OUTPUT_FOLDER.mkdir()

assets_path = require_mcdata("assets")

unifont_widths = {}
unifont_jp_widths = {}
default_widths = {}
alt_widths = {}
il_alt_widths = {}
space_widths = {}
with ZipFile(assets_path) as asset_archive:
  # Build charset
  build_charset(asset_archive)
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
with open(OUTPUT_FOLDER / "uniform_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "uniform_half_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "default_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "default_half_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "alt_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "alt_half_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "illageralt_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "illageralt_half_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "space_neg.json", "w") as file:
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
with open(OUTPUT_FOLDER / "space_half_neg.json", "w") as file:
  json.dump(space_half_negative, file, indent=2)
with open("resourcepack/assets/maputil/font/include/space_half_neg.json", "w") as file:
  json.dump(space_half_negative, file)
