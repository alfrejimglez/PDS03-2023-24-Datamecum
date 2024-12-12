from pathlib import Path
from shiny import App, render,reactive, ui
from shiny.types import FileInfo #Para utilizar input_file, aunque creo que ya no es necesario, de la versión alfa..
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

datos_dir = Path(__file__).parent / "datos"

#Datos=pd.read_csv('./datos/PrediccionesMaquina.csv',parse_dates=['dia']) #convertimos día a datetime

sns.set_style('white')
#sns.set_style('darkgrid')

#Interfaz de usuario
app_ui = ui.page_fluid(
    #Titulo
    ui.panel_title("Ejercicio 4. Reactividad I. Datamecum."),
    
    #layout sidebar
    ui.layout_sidebar(
         
         # Panel lateral
         ui.panel_sidebar(
            ui.h2("Carga de fichero"),
            ui.input_file("Fichero_ID",
                            "Selecciona fichero",
                            accept=[".csv"],
                             multiple=False,
                             button_label="Fichero",
                             placeholder="No hay fichero"),
            ui.h2("Opciones de filtrado"),
            
            #No podemos construirlo aquí, porque no podemos usar Datos() aquí. Al server que nos vamos!
              
              #ui.input_select("matricula_id","Selecciona una máquina", 
              #                choices = list(Datos.matricula.unique())),

            ui.output_ui('desplegable_matriculas'),
  
            
            
            #Desplegable creado en el server...
            ui.output_ui('desplegable_variable')
            ),
        #Panel principal
        ui.panel_main(
            ui.h2("Salida sistema experto"),
            ui.output_plot("grafico1"),
            ui.h2("Nivel de alarma"),
            ui.output_plot("grafico2"),
            ui.h2("Dataframe después de filtrar"),
            ui.output_table("tabla1"),
            )
        )
    )
    



#El server vacio con pass
def server(input, output, session):
    
    #Variable reactiva para cargar el fichero
    @reactive.Calc
    def Datos():
        
        #f: list[FileInfo] = input.Fichero_ID() #f es una lista de diccionarios, tantos como ficheros seleccionemos. 
        f  = input.Fichero_ID() #f es una lista de diccionarios, tantos como ficheros seleccionemos. 
        df = pd.read_csv(f[0]["datapath"], parse_dates=['dia']) #La clave "datapath" del diccionario contiene el path 

        return df
    
    # Creamos el objeto de salida de la UI desplegable de matriculas, hecho en el server
    @output
    @render.ui
    #Condicionamos la creación del desplegable matricula a un evento en input.Fichero
    @reactive.event(input.Fichero_ID) 
    def desplegable_matriculas():
        
        return ui.input_select("matricula_id","Selecciona una máquina",
                                 choices = list(Datos().matricula.unique()))


    #Salida objeto ui deplegable alarma
    @output
    @render.ui
    #Condicionamos la creación del desplegable variable a un evento en input.matricula
    @reactive.event(input.matricula_id)
    def desplegable_variable():
        
        variables=tuple(Datos().columns)
        variables_ok=variables[-(len(variables)-3):-1] #Selecciono desde a1...203  indexando desde el final :)
        ui_1=ui.input_select("variable_dataset",
                            "Selecciona variable",
                            choices=variables_ok,
                            selected="a1")
        
        return ui_1


    #Salida gráfico 1
    @output
    @render.plot
   #Condicionamos la creación del grafico 1 a un evento en input.matricula
    @reactive.event(input.matricula_id)
    
    def grafico1():
        graf1=sns.relplot(x="dia",y="p_orden",data=Datos().loc[Datos().matricula==input.matricula_id(),:],kind="line")
        graf1.fig.suptitle("Evolución de la probabilidad de avería")
        plt.xticks(rotation=45)
        return graf1

    #Salida gráfico 2
    @output
    @render.plot
    #Condicionamos la creación del grafico 12 a un evento en input.variable_dataset
    @reactive.event(input.variable_dataset)
    def grafico2():

        graf2=sns.relplot(x="dia",y=input.variable_dataset(),data=Datos().loc[Datos().matricula==input.matricula_id(),:],kind="line")
        graf2.fig.suptitle("Evolución de la intensidad de alarma")
        plt.xticks(rotation=45)
        return graf2
    
   #Salida Tabla 
    @output
    @render.table
    #Condicionamos la creación del grafico 12 a un evento en input.variable_dataset
    @reactive.event(input.variable_dataset)
    def tabla1():
        return Datos().loc[Datos().matricula==input.matricula_id(),:]



app = App(app_ui, server, static_assets=datos_dir)