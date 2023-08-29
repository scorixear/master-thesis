import json
from typing import Any
from helper.plot_helper import PlotParams
from textwrap import wrap


def show_heatmap(
    heatmap_data: tuple[list[str], list[str], list[list[float]]],
    x_label: str,
    y_label: str,
    title: str,
    file_name: str,
):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn

    y_labels = heatmap_data[0]
    x_labels = heatmap_data[1]
    if len(x_labels) < 4:
        fig_size = PlotParams.small_heatmap
    else:
        fig_size = PlotParams.big_heatmap
    values = np.array(heatmap_data[2])
    fig = plt.figure(figsize=fig_size)
    axis = fig.subplots()

    seaborn.heatmap(
        values, xticklabels=x_labels, yticklabels=y_labels, ax=axis, vmin=1, vmax=0
    )
    axis.tick_params(axis="both", labelsize=PlotParams.font_size)
    axis.collections[0].colorbar.ax.tick_params(labelsize=PlotParams.font_size)
    axis.set_xlabel(x_label, fontsize=PlotParams.font_size)
    axis.set_ylabel(y_label, fontsize=PlotParams.font_size)
    axis.set_title(
        "\n".join(wrap(title, 40)),
        pad=PlotParams.title_padding,
        fontsize=PlotParams.title_font_size,
        loc="center",
    )
    fig.tight_layout()
    fig.savefig(file_name)


class ModelHeatMap:
    def __init__(self, models: dict[str, "TypeHeatMap"] | None = None) -> None:
        if models is None:
            self.models: dict[str, TypeHeatMap] = {}
        else:
            self.models = models

    def get_value(
        self, model_name: str, type_name: str, source_name: str, value_name: str
    ):
        if model_name not in self.models:
            return None
        if type_name not in self.models[model_name].types:
            return None
        if source_name not in self.models[model_name].types[type_name].sources:
            return None
        if (
            value_name
            not in self.models[model_name].types[type_name].sources[source_name]
        ):
            return None
        return self.models[model_name].types[type_name].sources[source_name][value_name]

    def set_value(
        self,
        model_name: str,
        type_name: str,
        source_name: str,
        value_name: str,
        value: Any,
    ):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        self.models[model_name].types[type_name].sources[source_name][
            value_name
        ] = value

    def update_value(
        self,
        model_name: str,
        type_name: str,
        source_name: str,
        value_name: str,
        value: int,
    ):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        if (
            value_name
            not in self.models[model_name].types[type_name].sources[source_name]
        ):
            self.models[model_name].types[type_name].sources[source_name][
                value_name
            ] = 0
        self.models[model_name].types[type_name].sources[source_name][
            value_name
        ] += value

    def append_value(
        self,
        model_name: str,
        type_name: str,
        source_name: str,
        value_name: str,
        value: Any,
    ):
        if model_name not in self.models:
            self.models[model_name] = TypeHeatMap()
        if type_name not in self.models[model_name].types:
            self.models[model_name].types[type_name] = SourceHeatMap({})
        if source_name not in self.models[model_name].types[type_name].sources:
            self.models[model_name].types[type_name].sources[source_name] = {}
        if (
            value_name
            not in self.models[model_name].types[type_name].sources[source_name]
        ):
            self.models[model_name].types[type_name].sources[source_name][
                value_name
            ] = []
        self.models[model_name].types[type_name].sources[source_name][
            value_name
        ].append(value)

    def reorder(self, model_name: str, position: int):
        if model_name not in self.models:
            return
        if position < 0:
            position = len(self.models) + position
        if position >= len(self.models):
            position = position % len(self.models)
        model = self.models.pop(model_name)

        model_copy = self.models
        self.models = {}
        for i, (k, v) in enumerate(model_copy.items()):
            if i == position:
                self.models[model_name] = model
            self.models[k] = v
        if position == len(self.models):
            self.models[model_name] = model

    def get_heatmap_by_model(self, model_name: str, value_name: str):
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
                    x_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
            values.append(x_values)
        return y_labels, x_labels, values

    def get_makrof1_heatmap_total_by_model(self):
        example_model = list(self.models.keys())[0]
        y_labels = list(self.models[example_model].types.keys())
        x_labels = list(self.models[example_model].types[y_labels[0]].sources.keys())
        makrof1_values: list[list[float]] = []
        for type_name in y_labels:
            type_makrof1_values = []
            for source_name in x_labels:
                source_f1_values = []
                for model_name in self.models.keys():
                    source_f1_values.extend(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name]["f1"]
                    )
                source_makro_f1 = sum(source_f1_values) / len(source_f1_values)
                type_makrof1_values.append(source_makro_f1)
            makrof1_values.append(type_makrof1_values)
        return y_labels, x_labels, makrof1_values

    def get_avgvalue_heatmap_total_by_model(self, value_name: str):
        example_model = list(self.models.keys())[0]
        y_labels = list(self.models[example_model].types.keys())
        x_labels = list(self.models[example_model].types[y_labels[0]].sources.keys())
        values: list[list[float]] = []
        for type_name in y_labels:
            type_values = []
            for source_name in x_labels:
                source_values = []
                for model_name in self.models.keys():
                    source_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
                source_avg_value = sum(source_values) / len(source_values)
                type_values.append(source_avg_value)
            values.append(type_values)
        return y_labels, x_labels, values

    def get_makrof1_heatmap_total_by_type(self):
        y_labels = list(self.models.keys())
        x_labels = list(self.models[y_labels[0]].types.keys())
        makrof1_values: list[list[float]] = []
        for model_name in y_labels:
            model_makrof1_values = []
            for type_name in x_labels:
                type_f1_values = []
                for source_name in (
                    self.models[model_name].types[type_name].sources.keys()
                ):
                    type_f1_values.extend(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name]["f1"]
                    )
                type_makro_f1 = sum(type_f1_values) / len(type_f1_values)
                model_makrof1_values.append(type_makro_f1)
            makrof1_values.append(model_makrof1_values)
        return y_labels, x_labels, makrof1_values

    def get_avgvalue_heatmap_total_by_type(self, value_name: str):
        y_labels = list(self.models.keys())
        x_labels = list(self.models[y_labels[0]].types.keys())
        values: list[list[float]] = []
        for model_name in y_labels:
            model_values = []
            for type_name in x_labels:
                type_values = []
                for source_name in (
                    self.models[model_name].types[type_name].sources.keys()
                ):
                    type_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
                type_avg_value = sum(type_values) / len(type_values)
                model_values.append(type_avg_value)
            values.append(model_values)
        return y_labels, x_labels, values

    def get_makrof1_heatmap_total_by_source(self):
        y_labels = list(self.models.keys())
        example_type = list(self.models[y_labels[0]].types.keys())[0]
        x_labels = list(self.models[y_labels[0]].types[example_type].sources.keys())
        makrof1_values: list[list[float]] = []
        for model_name in y_labels:
            model_makrof1_values = []
            for source_name in x_labels:
                source_f1_values = []
                for type_name in self.models[model_name].types.keys():
                    source_f1_values.extend(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name]["f1"]
                    )
                source_makro_f1 = sum(source_f1_values) / len(source_f1_values)
                model_makrof1_values.append(source_makro_f1)
            makrof1_values.append(model_makrof1_values)
        return y_labels, x_labels, makrof1_values

    def get_avgvalue_heatmap_total_by_source(self, value_name: str):
        y_labels = list(self.models.keys())
        example_type = list(self.models[y_labels[0]].types.keys())[0]
        x_labels = list(self.models[y_labels[0]].types[example_type].sources.keys())
        values: list[list[float]] = []
        for model_name in y_labels:
            model_values = []
            for source_name in x_labels:
                source_values = []
                for type_name in self.models[model_name].types.keys():
                    source_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
                source_avg_value = sum(source_values) / len(source_values)
                model_values.append(source_avg_value)
            values.append(model_values)
        return y_labels, x_labels, values

    def get_heatmap_by_type(self, type_name: str, value_name: str):
        y_labels = list(self.models.keys())
        x_labels = list(self.models[y_labels[0]].types[type_name].sources.keys())
        values: list[list[Any]] = []
        for model_name in y_labels:
            x_values = []
            for source_name in x_labels:
                if (
                    value_name
                    not in self.models[model_name].types[type_name].sources[source_name]
                ):
                    x_values.append(0)
                elif (
                    source_name not in self.models[model_name].types[type_name].sources
                ):
                    x_values.append(0)
                elif type_name not in self.models[model_name].types:
                    x_values.append(0)
                else:
                    x_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
            values.append(x_values)
        return y_labels, x_labels, values

    def get_heatmap_by_source(self, source_name: str, value_name: str):
        y_labels = list(self.models.keys())
        x_labels = list(self.models[y_labels[0]].types.keys())
        values: list[list[Any]] = []
        for model_name in y_labels:
            x_values = []
            for type_name in x_labels:
                if (
                    value_name
                    not in self.models[model_name].types[type_name].sources[source_name]
                ):
                    x_values.append(0)
                elif (
                    source_name not in self.models[model_name].types[type_name].sources
                ):
                    x_values.append(0)
                elif type_name not in self.models[model_name].types:
                    x_values.append(0)
                else:
                    x_values.append(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name][value_name]
                    )
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
                        instance.set_value(
                            model_name, type_name, source_name, value_name, value
                        )
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
