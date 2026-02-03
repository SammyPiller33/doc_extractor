import afp

with open("./sample/start.afp", 'rb') as f:
    for sf in afp.stream(
            f,
            allow_unknown_fields = True,
           allow_unknown_triplets = True,
           allow_unknown_functions = True,
           strict = False):
        print(sf)


