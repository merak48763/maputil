from pathlib import Path
from tqdm import tqdm
import requests

VERSION_NAME = "1.21.5"
CACHE_FOLDER = Path("./generator_data/mcdata_cache")

def require_mcdata(branch: str):
  if not CACHE_FOLDER.is_dir():
    CACHE_FOLDER.mkdir()

  cache_path = CACHE_FOLDER / f"{VERSION_NAME}-{branch}.zip"
  if cache_path.is_file():
    return cache_path

  with requests.get(f"https://github.com/misode/mcmeta/archive/refs/tags/{VERSION_NAME}-{branch}.zip", stream=True) as res:
    res.raise_for_status()
    with open(cache_path, "wb") as file:
      with tqdm(unit="B", unit_scale=True, desc=f"Downloading mcmeta/{VERSION_NAME}-{branch}") as progress:
        for chunk in res.iter_content(chunk_size=16384):
          progress.update(len(chunk))
          file.write(chunk)
  return cache_path

__all__ = [
  "require_mcdata",
  "VERSION_NAME"
]
