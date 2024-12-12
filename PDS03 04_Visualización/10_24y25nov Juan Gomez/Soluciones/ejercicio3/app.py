from shiny import App, render, ui
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

Datos=pd.read_csv('./PrediccionesMaquina.csv',parse_dates=['dia']) #convertimos día a datetime
sns.set_style('white')
#sns.set_style('darkgrid')

#Interfaz de usuario
app_ui = ui.page_fluid(
    #Titulo
    ui.panel_title("Ejercicio 3. Combinando entradas y salidas en el server. Datamecum."),
    
    #layout sidebar
    ui.layout_sidebar(
         
         # Panel lateral
         ui.panel_sidebar(
            ui.h2("Opciones de filtrado"),
            ui.input_select("matricula_id","Selecciona una máquina", 
                            choices = list(Datos.matricula.unique())),
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
    
    #Salida gráfico 1
    @output
    @render.plot
    def grafico1():

        graf1=sns.relplot(x="dia",
                          y="p_orden",
                          data=Datos.loc[Datos.matricula==input.matricula_id(),:],
                          kind="line")
        graf1.fig.suptitle("Evolución de la probabilidad de avería")
        plt.xticks(rotation=45)
        return graf1

    #Salida gráfico 2
    @output
    @render.plot
    def grafico2():

        graf2=sns.relplot(x="dia",
                          y=input.variable_dataset(),
                          data=Datos.loc[Datos.matricula==input.matricula_id(),:],
                          kind="line")
        graf2.fig.suptitle("Evolución de la intensidad de alarma")
        plt.xticks(rotation=45)
        return graf2
    
   #Salida Tabla 
    @output
    @render.table
    def tabla1():
        return Datos.loc[Datos.matricula==input.matricula_id(),:]


    #Salida objeto ui deplegable alarma
    @output
    @render.ui
    def desplegable_variable():
        
        variables=tuple(Datos.columns)
        #variables=Datos.columns
        variables_ok=variables[-(len(variables)-3):-1] #Selecciono desde a1...203  indexando desde el final :)
        ui_1=ui.input_select("variable_dataset",
                             "Selecciona variable",
                             choices=variables_ok,
                             selected="a1")
        
        return ui_1



app = App(app_ui, server)
