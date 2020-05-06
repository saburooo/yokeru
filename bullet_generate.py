import os
from random import randint
import json

# 考えてみればjsonファイルにちまちまデータ書かなくてもpythonで書き出せば良いジャンカ！！

def generate():
    obj = {
        "enemies":[],
        "enemies_2":[]
    } 

    for timing in range(0, 2700, 30):
        obj["enemies"].append({
            "x":randint(0, 144),
            "y":20,
            "speed":randint(1,2),
            "timing":timing,
        })
        obj["enemies_2"].append({
            "x":randint(0, 144),
            "y":20,
            "timing":timing,
            "speed":randint(1,2),
            "radian":randint(45, 135)
        })

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "data.json")
    out_file  = open(path, "w", encoding='utf-8')
    json.dump(obj, out_file, ensure_ascii=False, indent=4)
    out_file.close()

generate()