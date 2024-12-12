
from pathlib import Path
from shiny import App, render,reactive, ui
from shiny.types import FileInfo #Para utilizar input_file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
#Para hacer cosas con plotly
#import plotly.graph_objects as go
#from shinywidgets import output_widget, register_widget #instalado con pip install shinywidgets

datos_dir = Path(__file__).parent / "datos"

#sns.set_style('white')
sns.set_style('darkgrid')

#Interfaz de usuario
#Elegimos entorno multipagina navbarpage
app_ui = ui.page_navbar(
    
    # Interfaz de usuario AAA. Primera pestaña. Ingesta de datos.
    ui.nav("Carga de fichero",
            ui.h2("Ingesta de datos."),
            #Diseño de pagina layout sidebar
            ui.layout_sidebar(
                ui.panel_sidebar(ui.h4("Carga de fichero"),
                    #Elemento de entrada input file estático para cargar un solo fichero, de tipo csv
                    ui.input_file("Fichero_ID",
                            "Selecciona fichero",
                            accept=[".csv"],
                             multiple=False,
                             button_label="Fichero",
                             placeholder="No hay fichero"),
                    # Elemento de entrada para elegir descriptivos de alarmas construido en el servidor....
                    ui.output_ui('desplegable_variable_carga'),
                             
                ),
                ui.panel_main(
                    #Organizamos las cosas con ui.row y ui.column
                    ui.row(ui.column(9,ui.h2("Resumen estadísticos básicos del dataset"),offset=2)),
                    ui.hr(),
                    ui.row(ui.column(9,ui.panel_well(ui.output_table("resumen_estadistico")),offset=2)))
            )
        ),
    #Interfaz de usuario BBB.Segunda pestaña. Sistema experto.
    ui.nav("Sistema Experto",
    
    ),
    #Interfaz de usuario CCC y DDD. Tercera y cuarta pestaña. Análisis  estado máquina
    # menu de pestañas, nav_menu
    ui.nav_menu("Análisis estado máquina", # Agrupación de dos páginas
        
        #Interfaz de usuario CCC.Tercera pestaña. Detección anomalias.
        ui.nav("Detector de anómalias",
            
        ),
        #Interfaz de usuario DDD PASO 4.Cuarta pestaña. EDA Alarmas.
        ui.nav("EDA Alarmas global",
           
        )
    ),

    #Interfaz de usuario FFF.Quinta pestaña. Publicidad!
    ui.nav_spacer(),
    ui.nav_control(
            ui.a("Datamecum",
                href="http://www.datamecum.com",
                target='_blank')
        )
)   
    



def server(input, output, session):

    #INICIO PASO 1 Funciones server AAA. Primera pestaña. Ingesta de datos.
    
    #Variable reactiva para cargar el fichero en crudo tal y como viene del csv.
    @reactive.Calc
    def Datos():
        #f: list[FileInfo] = input.Fichero_ID() #las primeras versiones requerian de esto...
        f = input.Fichero_ID()
        df = pd.read_csv(f[0]["datapath"], parse_dates=['dia'])
        # Convertimos el datetime a date para comparar con la salida del input.date_range
        df["dia"]=pd.to_datetime(df["dia"]).dt.date 
        return df
    

    ##Salida objeto ui deplegable input.selectize de alarma  en Ingesta de datos
    @output
    @render.ui
    def desplegable_variable_carga():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            variables=tuple(Datos().columns)
            variables_ok=variables[-(len(variables)-3):] #Selecciono desde a1...203  indexando desde el final :)
            ui_0=ui.input_selectize("variable_dataset_0",
                            "Selecciona variable",
                            choices=variables_ok,
                            multiple=True,
                            selected=["a1","a3","a4","a6","p_orden"])
            return ui_0
    
    #Variable reactiva para conseguir data frame con la  selección alarmas/variables elegidas en el input. selectize
    @reactive.Calc
    def Datos_filt0():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            df0=Datos().copy()[list(input.variable_dataset_0())] #convertimos a lista la selección para seleccionar columnas
            return  df0


   ##Salida Table con el  resumen del dataset Datos_filt0()
    @output
    @render.table(index=True) # index=True Para sacar los estadisticos (indices del describe)
    def resumen_estadistico():
        #Condicionamos la creaciósn de la tabla resumen dataset a la presencia de fichero
        if input.Fichero_ID():
            resumen=Datos_filt0().describe()
            return resumen


    #FIN PASO 1 Funciones server AAA. 
    
    #INICIO PASO 2 Funciones server BBB. Segunda pestaña. Sistema Experto.

    # Creamos el objeto de salida de la UI desplegable de matriculas, del sistema experto



    ##Salida objeto de salida UI deplegable alarma, del sistema experto


    ##Salida objeto ui interruptor tiempo, del sistema experto


    ##Salida objeto UI selector periodo tiempo. del sistema experto


    #Variable reactiva para aplicar filtros pestaña Sistema experto (Máquina, alarmas, tiempo)

    ##Salida gráfico 1. Evolucion de probabilidad de orden en sistema experto


    #Salida gráfico 2 Evolucion de alarma  seleccionada en sistema experto.

    #FIN PASO 2 Funciones server BBB.   
    
    
    #INICIO PASO 3 Funciones server CCC. Tercera pestaña. Análisis estado máquina. Detector de anomalias.


    #Variable reactiva para obtener mediana de las alarmas y p_orden total dataset

    
    # Creamos el objeto de salida de la UI desplegable de matriculas en deteccion de anomalias


    # #Variable reactiva para obtener medina de alarmas, mediana p_orden y dataframe filtrado en maquina concreta


    ##Salida gráfico 02. Radar plot en deteccion de anomalias.. pushing the limits matplolib :)


    ##Salida gráfico 03, barplot p_orden en deteccion de anomalias


    #Salida Tabla  en deteccion de anomalias


    #FIN PASO 3 Funciones server CCC.
    
    #PASO 4 INICIO Funciones server DDD. Cuarta pestaña. Análisis estado máquina. EDA Alarmas global.
    
    ##Salida objeto ui deplegable de alarmas,  en EDA alarmas global


    ##Salida objeto ui interruptor remove outliers (valores por encima de mediana+1.5IQR) y ceros en EDA alarmas global



    #Variable reactiva para  crear dataset ordenado para pintar 
    # y remove outliers (valores por encima de mediana+1.5IQR) y ceros


    ##Salida gráfico 01. Boxplot  en EDA alarmas



    ##Salida gráfico 011. KDE plot en EDA alarmas.


#FIN PASO 4 Funciones server DDD.
app = App(app_ui, server, static_assets=datos_dir)