import json



veg = []
with open("veg_raw.txt","r") as w:
    for line in w:
        veg.append(line.lower().rstrip())


with open("veg_format.txt","x+") as v:
    json.dump(veg,v)
