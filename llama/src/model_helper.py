from typing import Any
import json_fix
import json

def get_model_key(name: str) -> int:
    if name == "gpt4":
            return 0
    else:
        name_split = name.split("_")
        epoch_string = name_split[1][:-1]
        if len(name_split) == 2:
            epoch_int = int(epoch_string, 10)*3
        else:
            if name_split[2] == "v100":
                epoch_int = int(epoch_string, 10)*3 + 1
            else:
                epoch_int = int(epoch_string, 10)*3 + 2
            
        return epoch_int+1

def get_model_name(file_name: str) -> str:
    if file_name.startswith("gpt4"):
        return "gpt4"
    else:
        name_split = file_name.split("_")
        if len(name_split) >= 3 and (name_split[2] == "v100" or name_split[2] == "a30"):
            return name_split[0] + '_' + name_split[1] + '_' + name_split[2]
        else:
            return name_split[0] + '_' + name_split[1]
        
class ModelHeatMap:   
    def __init__(self, models: dict[str, "TypeHeatMap"] | None = None) -> None:
        if models is None:
            self.models: dict[str, TypeHeatMap] = {}
        else:
            self.models = models
    def get_value(self, model_name: str, type_name: str, source_name: str, value_name: str):
        if model_name not in self.models:
            return None
        if type_name not in self.models[model_name].types:
            return None
        if source_name not in self.models[model_name].types[type_name].sources:
            return None
        if value_name not in self.models[model_name].types[type_name].sources[source_name]:
            return None
        return self.models[model_name].types[type_name].sources[source_name][value_name]
    def set_value(self, model_name: str, type_name: str, source_name: str, value_name: str, value: Any):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        self.models[model_name].types[type_name].sources[source_name][value_name] = value
    def update_value(self, model_name: str, type_name: str, source_name: str, value_name: str, value: int):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        if value_name not in self.models[model_name].types[type_name].sources[source_name]:
            self.models[model_name].types[type_name].sources[source_name][value_name] = 0
        self.models[model_name].types[type_name].sources[source_name][value_name] += value
    def append_value(self, model_name: str, type_name: str, source_name: str, value_name: str, value: Any):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        if value_name not in self.models[model_name].types[type_name].sources[source_name]:
            self.models[model_name].types[type_name].sources[source_name][value_name] = []
        self.models[model_name].types[type_name].sources[source_name][value_name].append(value)
    def get_heatmap(self, model_name: str, value_name: str):
        dict_values = self.models[model_name]
        y_labels = list(dict_values.types.keys())
        x_labels = list(dict_values.types[y_labels[0]].sources.keys())
        values: list[list[Any]] = []
        for type_name in y_labels:
            x_values = []
            for source_name in x_labels:
                if value_name not in dict_values.types[type_name].sources[source_name]:
                    x_values.append(0)
                elif source_name not in dict_values.types[type_name].sources:
                    x_values.append(0)
                elif type_name not in dict_values.types:
                    x_values.append(0)
                else:
                    x_values.append(self.models[model_name].types[type_name].sources[source_name][value_name])
            values.append(x_values)
        return y_labels, x_labels, values
    def __json__(self):
        return self.__dict__
    
    @staticmethod
    def _load_from_json(values):
        instance = ModelHeatMap()
        for model_name, model_values in values["models"].items():
            for type_name, type_values in model_values["types"].items():
                for source_name, source_values in type_values["sources"].items():
                    for value_name, value in source_values.items():
                        instance.set_value(model_name, type_name, source_name, value_name, value)
        return instance
    
    
    @staticmethod
    def read_json(file_name) -> "ModelHeatMap":
        with open(file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return ModelHeatMap._load_from_json(data)
    
    def save_json(self, file_name):
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(self, json_file, default=lambda o: o.__json__(), indent=4)

class TypeHeatMap:
    def __init__(self, types: dict[str, "SourceHeatMap"] | None = None) -> None:
        if types is None:
            self.types: dict[str, SourceHeatMap] = {}
        else:
            self.types = types
    def __json__(self):
        return self.__dict__

class SourceHeatMap:
    def __init__(self, values: dict[str, Any]) -> None:
        self.sources: dict[str, Any] = {}
    def __json__(self):
        return self.__dict__