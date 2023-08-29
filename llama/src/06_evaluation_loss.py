import os
import argparse
import json
import matplotlib.pyplot as plt

from helper.plot_helper import PlotParams


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="evaluation/criterias/loss/loss_data.json",
    )
    parser.add_argument("-o", "--output", type=str, default="evaluation/criterias/loss")

    args = parser.parse_args()
    with open(args.input) as f:
        input_data = json.load(f)

    plot_df = {}

    for gpu_type in input_data:
        name = gpu_type["name"]
        data = gpu_type["data"]
        validation_loss = []
        loss = []
        x = []
        x_label = []
        for model in data:
            validation_loss.append(model["validation_loss"])
            loss.append(model["training_loss"])
            x.append(model["epochs"])
            x_label.append(model["name"])
        plot_df[name] = {
            "validation_loss": validation_loss,
            "loss": loss,
            "x": x,
            "x_label": x_label,
        }
    fig1 = plt.figure(figsize=PlotParams.fig_size)
    fig2 = plt.figure(figsize=PlotParams.fig_size)
    axis1 = fig1.subplots()
    axis2 = fig2.subplots()

    for gpu_type, values in plot_df.items():
        axis1.plot(values["x"], values["validation_loss"], label=gpu_type, marker="o")
        axis1.set_xticks(
            ticks=values["x"], labels=values["x"], fontsize=PlotParams.font_size
        )
        axis2.plot(values["x"], values["loss"], label=gpu_type, marker="o")
        axis2.set_xticks(
            ticks=values["x"], labels=values["x"], fontsize=PlotParams.font_size
        )
    axis1.tick_params(axis="both", labelsize=PlotParams.font_size)
    axis2.tick_params(axis="both", labelsize=PlotParams.font_size)
    axis1.set_ylim(bottom=0)
    axis2.set_ylim(bottom=0)
    axis1.set_xlabel("Epochen", fontsize=PlotParams.font_size)
    axis1.set_ylabel("Validierung Fehler", fontsize=PlotParams.font_size)
    axis1.set_title("Validierung Fehler", fontsize=PlotParams.title_font_size)
    axis1.legend(fontsize=PlotParams.font_size)

    axis2.set_xlabel("Epochen", fontsize=PlotParams.font_size)
    axis2.set_ylabel("Training Fehler", fontsize=PlotParams.font_size)
    axis2.set_title("Training Fehler", fontsize=PlotParams.title_font_size)
    axis2.legend(fontsize=PlotParams.font_size)

    fig1.savefig(os.path.join(args.output, "validation_loss.png"))
    fig2.savefig(os.path.join(args.output, "loss.png"))


if __name__ == "__main__":
    main()
