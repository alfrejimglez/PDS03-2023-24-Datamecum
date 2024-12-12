#Cargamos librerías que vamos a utilizar, shiny, pandas y seaborn
from shiny import App, render, ui
import pandas as pd
import seaborn as sns

#from pathlib import Path

sns.set_theme()

#Cargo el fichero donde tengo los datos
long_breeds = pd.read_csv("dog_traits_long.csv")

#Convertimos a lista las columnas rasgos (trait) y raza (breed) 
#para pasarlo como un argumento al selectize de entrada
options_traits = long_breeds["trait"].unique().tolist()
options_breeds = long_breeds["breed"].unique().tolist()

app_ui = ui.page_fluid(
    ui.h2('Selección de rasgos y raza'),
    #Elementos de entrada que serán dos selectizes multiples en la UI
    ui.input_selectize("traits", "Rasgos del perro", options_traits, multiple=True),
    ui.input_selectize("breeds", "Raza del perro", options_breeds, multiple=True),
    
    ui.h2('Resultados gráficos'),
    #Elementos de salida en la UI en este caso un gráfico
    ui.output_plot("barchart")
)


def server(input, output, session):
    @output
    @render.plot
    def barchart():
        # input.traits() contiene la selección del elemento de entrada traits
        # lo que hacemos con isin es filtrar las muestras de esos rasgos concretos
        indx_trait = long_breeds["trait"].isin(input.traits())
        # input.traits() contiene la selección del elemento de entrada traits
        # lo que hacemos con isin es filtrar las muestras de esos rasgos concretos
        indx_breed = long_breeds["breed"].isin(input.breeds())

        # subset data seleccionamos aquellos que verifican las dos opciones de filtrado
        sub_df = long_breeds[indx_trait & indx_breed]
        sub_df["dummy"] = 1

        # Hacemos un gráfico de barras, ponemos en x la variable "dummy",  asignamos color a "trait" y 
        # rating al eje y. Hacemos un grid por columnas (col=breed) separando por raza
        # saltando a la sigueinte fila cada 3 colmnas.
        g = sns.catplot(
            data=sub_df, kind="bar",
            y="rating", x="dummy", hue="trait",
            col="breed", col_wrap=3,
        )

        # Le damos un poquito de estilo... eliminamos etiquetas en x y ponemos títulos
        g.set_xlabels("")
        g.set_xticklabels("")
        g.set_titles(col_template="{col_name}")

        return g


app = App(app_ui, server)