from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

app_ui = ui.page_fluid(
    ui.panel_title("Visualización de una distribución normal"),

    ui.layout_sidebar(

      ui.panel_sidebar(
        ui.input_slider("n", "Tamaño de la muestra", 0, 1000, 250),
        ui.input_numeric("mean", "Media", 0),
        ui.input_numeric("std_dev", "Desviación típica", 1),
        ui.input_slider("n_bins", "Resolución del histograma", 0, 100, 20),
      ),

      ui.panel_main(
        ui.output_plot("plot")
      ),
    ),
)

def server(input, output, session):

    @output
    @render.plot
    def plot():
        x = np.random.normal(input.mean(), input.std_dev(), input.n())

        fig, ax = plt.subplots()
        ax.hist(x, input.n_bins(), density=False)
        ax.set_xlabel('Valores de la distribución')
        ax.set_ylabel('Frecuencia')
        return fig


app = App(app_ui, server)
