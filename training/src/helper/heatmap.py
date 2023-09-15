from textwrap import wrap
import json
from typing import Any
from helper.plot_helper import PlotParams


def show_heatmap(
    heatmap_data: tuple[list[str], list[str], list[list[float]]],
    x_label: str,
    y_label: str,
    title: str,
    file_name: str,
) -> None:
    """Generates a heatmap and saves it to a file.

    Args:
        heatmap_data (tuple[list[str], list[str], list[list[float]]]): Heatmap data. Structure is [y_labels, x_labels, values].
        x_label (str): the label for the x axis
        y_label (str): the label for the y axis
        title (str): the title of the plot
        file_name (str): the file name to save the plot to
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn

    # read in data
    y_labels = heatmap_data[0]
    x_labels = heatmap_data[1]
    values = np.array(heatmap_data[2])
    # if less than 4 columns, we shrink the size of the plot
    if len(x_labels) < 4:
        fig_size = PlotParams.small_heatmap
    else:
        fig_size = PlotParams.big_heatmap
    # create figure
    fig = plt.figure(figsize=fig_size)
    axis = fig.subplots()

    # plot the heatmap
    # only used for makrof1, therefore vmin and vmax are hard coded
    seaborn.heatmap(
        values, xticklabels=x_labels, yticklabels=y_labels, ax=axis, vmin=1, vmax=0 # type: ignore
    )
    # update fontsizes
    axis.tick_params(axis="both", labelsize=PlotParams.font_size)
    axis.collections[0].colorbar.ax.tick_params(labelsize=PlotParams.font_size)
    axis.set_xlabel(x_label, fontsize=PlotParams.font_size)
    axis.set_ylabel(y_label, fontsize=PlotParams.font_size)
    # se the title
    axis.set_title(
        # wrap the title to fit the plot
        "\n".join(wrap(title, 40)),
        pad=PlotParams.title_padding,
        fontsize=PlotParams.title_font_size,
        loc="center",
    )
    # and save the figure
    fig.tight_layout()
    fig.savefig(file_name)


class ModelHeatMap:
    """Represents a singular MapStructure containing all Data for all Models, Types, Sources and Values.
    """
    def __init__(self, models: dict[str, "TypeHeatMap"] | None = None) -> None:
        """Initialze the structure. Can be optionally initialized with preexisting data. This is used for json loading.

        Args:
            models (dict[str, &quot;TypeHeatMap&quot;] | None, optional): Optional preexisting data. Defaults to None.
        """
        if models is None:
            self.models: dict[str, TypeHeatMap] = {}
        else:
            self.models = models

    def get_value(
        self, model_name: str, type_name: str, source_name: str, value_name: str
    ) -> (Any | None):
        """Returns a value from the structure. If the value does not exist, None is returned.

        Args:
            model_name (str): Name of the model
            type_name (str): Name of the type
            source_name (str): Name of the source
            value_name (str): Name of the value

        Returns:
            (Any | None): Possibly returns value if found. Otherwise None.
        """
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
        """Sets a given value in the structure. If the value or any of the keys do not exist, they are created.

        Args:
            model_name (str): Name of the model
            type_name (str): Name of the type
            source_name (str): Name of the source
            value_name (str): Name of the value
            value (Any): Value to set
        """
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
        """Updates an integer value by increasing it by the given value. If the value or any of the keys do not exist, they are created.

        Args:
            model_name (str): Name of the model
            type_name (str): Name of the type
            source_name (str): Name of the source
            value_name (str): Name of the value
            value (int): Amount to increase the value by
        """
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
        """Updates a value by appending the given value to it. If the value or any of the keys do not exist, they are created.

        Args:
            model_name (str): Name of the Model
            type_name (str): Name of the Type
            source_name (str): Name of the Source
            value_name (str): Name of the Value
            value (Any): Value to append to the existing value
        """
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
        """Reorders the models by setting the given model to the given position. If the position is negative, it is counted from the end of the list.

        Args:
            model_name (str): Name of the model to reorder
            position (int): Position to move the model to
        """
        if model_name not in self.models:
            return
        # if position is negative, count from the end of the list
        if position < 0:
            position = len(self.models) + position
        # if position is larger than the length of the list, count from the beginning
        if position >= len(self.models):
            position = position % len(self.models)
        # pop the model
        model = self.models.pop(model_name)

        # save reference for iteration
        model_copy = self.models
        # and reset the models
        self.models = {}
        # iterate over the models and insert the model at the given position
        for i, (k, v) in enumerate(model_copy.items()):
            if i == position:
                self.models[model_name] = model
            self.models[k] = v
        # if the model was not inserted yet, insert it at the end
        if position == len(self.models):
            self.models[model_name] = model

    def get_heatmap_by_model(self, model_name: str, value_name: str) -> tuple[list[str], list[str], list[list[Any]]]:
        """Returns heatmap data for the given model and value.

        Args:
            model_name (str): name of the model
            value_name (str): name of the value

        Returns:
            tuple[list[str], list[str], list[list[Any]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
        dict_values = self.models[model_name]
        # we assume identical types and sources for each model and type
        y_labels = list(dict_values.types.keys())
        x_labels = list(dict_values.types[y_labels[0]].sources.keys())
        values: list[list[Any]] = []
        # for each type and source, we get the value
        for type_name in y_labels:
            x_values = []
            for source_name in x_labels:
                # if the current type and source do not exist, we set the value to 0
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

    def get_makrof1_heatmap_total_by_model(self) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the makrof1 heatmap data for all models.

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
        example_model = list(self.models.keys())[0]
        y_labels = list(self.models[example_model].types.keys())
        x_labels = list(self.models[example_model].types[y_labels[0]].sources.keys())
        makrof1_values: list[list[float]] = []
        # for each type and source, we get the f1 values
        for type_name in y_labels:
            type_makrof1_values = []
            for source_name in x_labels:
                source_f1_values = []
                # for each model, we get the f1 values
                for model_name in self.models.keys():
                    source_f1_values.extend(
                        self.models[model_name]
                        .types[type_name]
                        .sources[source_name]["f1"]
                    )
                # and calculate the average
                source_makro_f1 = sum(source_f1_values) / len(source_f1_values)
                # and append it to the list
                type_makrof1_values.append(source_makro_f1)
            makrof1_values.append(type_makrof1_values)
        return y_labels, x_labels, makrof1_values

    def get_avgvalue_heatmap_total_by_model(self, value_name: str) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the average value heatmap data for all models.

        Args:
            value_name (str): name of the value to average over

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_makrof1_heatmap_total_by_type(self) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the makrof1 heatmap data for all types.

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_avgvalue_heatmap_total_by_type(self, value_name: str) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the average value heatmap data for all types.

        Args:
            value_name (str): name of the value to average over

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_makrof1_heatmap_total_by_source(self) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the makrof1 heatmap data for all sources.

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_avgvalue_heatmap_total_by_source(self, value_name: str) -> tuple[list[str], list[str], list[list[float]]]:
        """Returns the average value heatmap data for all sources.

        Args:
            value_name (str): name of the value to average over

        Returns:
            tuple[list[str], list[str], list[list[float]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_heatmap_by_type(self, type_name: str, value_name: str) -> tuple[list[str], list[str], list[list[Any]]]:
        """Returns heatmap data for the given type and value.

        Args:
            type_name (str): name of the type
            value_name (str): name of the value

        Returns:
            tuple[list[str], list[str], list[list[Any]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def get_heatmap_by_source(self, source_name: str, value_name: str) -> tuple[list[str], list[str], list[list[Any]]]:
        """Returns heatmap data for the given source and value.

        Args:
            source_name (str): name of the source
            value_name (str): name of the value

        Returns:
            tuple[list[str], list[str], list[list[Any]]]: tuple representing the heatmap data. Structure is [y_labels, x_labels, values].
        """
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

    def __json__(self) -> dict[str, Any]:
        """Returns the json representation of the structure.

        Returns:
            dict[str, Any]: json representation of the structure
        """
        return self.__dict__

    @staticmethod
    def _load_from_json(values: Any) -> "ModelHeatMap":
        """Loads the structure from a json representation.

        Args:
            values (Any): json representation of the structure

        Returns:
            ModelHeatMap: the loaded structure
        """
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
    def read_json(file_name: str) -> "ModelHeatMap":
        """Reads the structure from a json file.

        Args:
            file_name (str): path of the file to read from

        Returns:
            ModelHeatMap: the loaded structure
        """
        with open(file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return ModelHeatMap._load_from_json(data)

    def save_json(self, file_name: str) -> None:
        """Saves the structure to a json file.

        Args:
            file_name (str): path of the file to save to
        """
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(self, json_file, default=lambda o: o.__json__(), indent=4)


class TypeHeatMap:
    """Represents a singular MapStructure containing all Data for all Types, Sources and Values.
    """
    def __init__(self, types: dict[str, "SourceHeatMap"] | None = None) -> None:
        """Initialze the structure. Can be optionally initialized with preexisting data. This is used for json loading.

        Args:
            types (dict[str, &quot;SourceHeatMap&quot;] | None, optional): Optional preexisting data. Defaults to None.
        """
        if types is None:
            self.types: dict[str, SourceHeatMap] = {}
        else:
            self.types = types

    def __json__(self):
        return self.__dict__


class SourceHeatMap:
    """Represents a singular MapStructure containing all Data for all Sources and Values.
    """
    def __init__(self, values: dict[str, Any] | None = None) -> None:
        """Initialze the structure. Can be optionally initialized with preexisting data. This is used for json loading.

        Args:
            values (dict[str, Any]): Optional preexisting data. Defaults to None.
        """
        if values is None:
            self.sources: dict[str, Any] = {}
        else:
            self.sources: dict[str, Any] = values

    def __json__(self):
        return self.__dict__
