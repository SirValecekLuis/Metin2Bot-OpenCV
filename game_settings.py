FILE_NAME = "game_settings.cfg"
VALUES = {}


# TODO: check if this is good solution to do it like that (prob. not)
def get_values_from_file():
    try:
        with open(FILE_NAME, "r") as f:
            text = f.readlines()
            for line in text:
                if line.startswith("#"):
                    continue
                line = line.replace(" ", "").strip("\n").split("=")
                if len(line) == 2:
                    value = float(line[1])
                    if round(value) == float(value):
                        VALUES[line[0]] = int(line[1])
                    else:
                        VALUES[line[0]] = float(line[1])
    except Exception as e:
        print("Chyba se souborem / v souboru.\n", e)
        exit(-1)


if len(VALUES) == 0:
    get_values_from_file()
