import os
from functools import cache

@cache
def get_dir_size(path:str, isFile: bool = False) -> int:
    found_dirs = 0
    for item in os.listdir(path):
        if item == ".info": continue
        if (not isFile) and os.path.isdir(f"{path}{'/' if path[-1] != '/' else ''}{item}"):
            found_dirs += 1
        elif isFile and os.path.isfile(f"{path}{'/' if path[-1] != '/' else ''}{item}"):
            found_dirs += 1
    return found_dirs


sizes: dict[str,int] = {
    "ll": get_dir_size("static/samples/letters/lower"),
    "lu": get_dir_size("static/samples/letters/upper"),
    "nums": get_dir_size("static/samples/numbers"),
    "syms": get_dir_size("static/samples/symbols", isFile=True)
}

fonts: dict[str,dict[str,str]] = {}

for key in list(sizes.keys()):
    if key == "syms": continue

    fonts[key] = {}
    for i in range(1, sizes[key]+1):
        name = ""
        if i < 10: name = f"00{i}"
        elif 10 < i < 100: name = f"0{i}"
        else: name = f"{i}"

        path = ""
        if key == "ll":
            path = "static/samples/letters/lower/"
        if key == "lu":
            path = "static/samples/letters/upper/"
        if key == "nums":
            path = "static/samples/numbers/"

        fonts[key][name] = path + name