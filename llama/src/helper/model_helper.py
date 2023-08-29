def get_model_key(name: str) -> int:
    if name == "gpt4":
        return 0
    else:
        name_split = name.split("_")
        epoch_string = name_split[1][:-1]
        if len(name_split) == 2:
            epoch_int = int(epoch_string, 10) * 3
        else:
            if name_split[2] == "v100":
                epoch_int = int(epoch_string, 10) * 3 + 1
            else:
                epoch_int = int(epoch_string, 10) * 3 + 2

        return epoch_int + 1


def get_model_name(file_name: str) -> str:
    if file_name.startswith("gpt4"):
        return "gpt4"
    else:
        name_split = file_name.split("_")
        if len(name_split) >= 3 and (name_split[2] == "v100" or name_split[2] == "a30"):
            return name_split[0] + "_" + name_split[1] + "_" + name_split[2]
        else:
            return name_split[0] + "_" + name_split[1]
