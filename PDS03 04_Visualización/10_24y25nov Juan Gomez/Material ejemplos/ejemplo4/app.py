import random
import time
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

from shiny import *

app_ui = ui.page_fluid(
    ui.h2('Ejemplo de @reactive.Calc'),
    ui.input_slider("Numero_muestras", 
    "Selecciona el número de muestras",1,1000,500),
    ui.input_numeric("Numero_bins",
     "Selecciona el numero de bins",50),
#    ui.br(),
    ui.output_plot("result"),
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def data():
        return numpy.random.randn(input.Numero_muestras())
    @output
    @render.plot
    def result():
        fig , ax = plt.subplots()
        ax.hist(data(), density=False, bins=input.Numero_bins())  
        ax.set_ylabel("Frecuencia")
        ax.set_xlabel('Datos')
        ax.set_title('Histograma de una distribución normal ')

        return fig
app = App(app_ui, server)