FILE_NAME = "./game_settings.cfg"
VALUES = dict()


def get_values_from_file():
    try:
        with open(FILE_NAME, "r") as f:
            text = f.readlines()
            for line in text:
                if line.startswith("#"):
                    continue
                line = line.replace(" ", "").strip("\n").split("=")
                if len(line) == 2:
                    VALUES[line[0]] = float(line[1])
    except Exception as e:
        print("Chyba se souborem / v souboru.\n", e)
        exit(-1)


get_values_from_file()
