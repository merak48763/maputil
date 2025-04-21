import json

def exact_match(level: int):
  predicate = {
    "condition": "location_check",
    "predicate": {
      "light": {"light": level}
    }
  }
  with open(f"datapack/data/mu/predicate/_/light/{level}.json", "w") as file:
    json.dump(predicate, file, indent=2)
    file.write("\n")

def range_match(min: int, max: int):
  predicate = {
    "condition": "location_check",
    "predicate": {
      "light": {"light": {"min": min, "max": max}}
    }
  }
  with open(f"datapack/data/mu/predicate/_/light/{min}_{max}.json", "w") as file:
    json.dump(predicate, file, indent=2)
    file.write("\n")

for i in range(8):
  exact_match(i*2)
for i in range(4):
  range_match(i*4, i*4+1)
for i in range(2):
  range_match(i*8, i*8+3)
range_match(0, 7)

for i in [1, 2, 4, 8]:
  for j in range(i):
    lb1 = j * (16//i)
    rb1 = lb1 + (8//i) - 1
    lb2 = lb1 + (8//i)
    rb2 = lb1 + (16//i) - 1
    if lb1 == rb1:
      exact_match(lb1)
      with open(f"datapack/data/mu/function/_/light/{lb1}_{rb2}.mcfunction", "w") as file:
        file.write(f"execute if predicate mu:_/light/{lb1} run return {lb1}\n")
        file.write(f"return {rb2}\n")
    else:
      range_match(lb1, rb1)
      function_name = "query_light" if i == 1 else f"_/light/{lb1}_{rb2}"
      with open(f"datapack/data/mu/function/{function_name}.mcfunction", "w") as file:
        file.write(f"execute if predicate mu:_/light/{lb1}_{rb1} run return run function mu:_/light/{lb1}_{rb1}\n")
        file.write(f"return run function mu:_/light/{lb2}_{rb2}\n")
