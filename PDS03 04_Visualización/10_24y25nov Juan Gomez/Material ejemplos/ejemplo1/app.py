import pandas as pd
from io import StringIO
from shiny import App, render, ui

# Creamos la UI como página fluida
app_ui = ui.page_fluid(
    ui.h2('Ejemplo 1, vamos a crear un dataframe a partir texto'),
    ui.input_text_area("csv_text", #Elemenrto de entrada de area de texto
     "Campo de entrada fichero csv",
     value="a, b\n1, 2\n3, 4"), #Valor por defecto de arranque del 
    
    ui.h2('Data frame de salida'),
    ui.output_table("parsed_data"),#Visualizamos la salida en la UI
)

# Creamos la función de servidor, donde todo se conecta...
def server(input, output, session):
    @output
    @render.table
    def parsed_data():
        #StringIO permite convertir la cadena de texto a un formato que 
        #pd.read_csv entienda
        file_text = StringIO(input.csv_text())
        data = pd.read_csv(file_text)
        #La función del objeto de salida parsed_date() devuelve un dataframe
        return data

# Creamos la app de shiny con la función App de shiny.
app = App(app_ui, server)
