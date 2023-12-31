import shutil

NAME = "tmp"

x = {
    "y": 5,
}

y = {
    "fd": 567,
}

x.update(y)


print("RES", x)
