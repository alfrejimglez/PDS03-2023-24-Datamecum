
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
        ui.h2("Análisis de necesidad de mantenimiento"),
        #Diseño de pagina layout sidebar
        ui.layout_sidebar(
            # Panel lateral
            ui.panel_sidebar(
                ui.h4("Ajustes de filtrado"),
                ui.hr(),
                ui.output_ui('desplegable_matriculas_experto'),
                #Desplegable alarmas experto
                ui.output_ui('desplegable_variable'),
                ui.hr(),
                #Interruptor de filtrado temporal, hecho en el server
                ui.output_ui('switch_temp'),
                #Elemento de selección  temporal, hecho en el server
                ui.output_ui('date_range') 
            ),
        #Panel principal
            ui.panel_main(
                ui.h2("Salida sistema experto"),
                ui.hr(),
                #Gráfico evolucion p_orden
                ui.output_plot("grafico11"),
                ui.h2("Nivel de alarma"),
                ui.hr(),
                #Gráfico evolucion alarma
                ui.output_plot("grafico12"),
                
            )
        )
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
        f: list[FileInfo] = input.Fichero_ID()
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
        #Condicionamos la creación de la tabla resumen dataset a la presencia de fichero
        if input.Fichero_ID():
            resumen=Datos_filt0().describe()
            return resumen

    #FIN PASO 1 Funciones server AAA. 
    
    #INICIO PASO 2 Funciones server BBB. Segunda pestaña. Sistema Experto.

    # Creamos el objeto de salida de la UI desplegable de matriculas, del sistema experto
    @output
    @render.ui
    def desplegable_matriculas_experto():
        #Condicionamos la creación del desplegable matricula a un evento en input.Fichero
        if input.Fichero_ID():
            return ui.input_select("matricula_id","Selecciona una máquina",
                                 choices = tuple(Datos().matricula.unique()))


    ##Salida objeto de salida UI deplegable alarma, del sistema experto
    @output
    @render.ui
    def desplegable_variable():
        #Condicionamos la creación del desplegable variable a un evento en input.matricula
        if input.matricula_id():
            variables=tuple(Datos().columns)
            variables_ok=variables[-(len(variables)-3):-1] #Selecciono desde a1...203  indexando desde el final :)
            ui_1=ui.input_select("variable_dataset",
                            "Selecciona variable",
                            choices=variables_ok,
                            selected="a1")
        
        return ui_1

    ##Salida objeto ui interruptor tiempo, del sistema experto
    @output
    @render.ui
    def switch_temp():
        if input.matricula_id():
            return ui.input_switch('filt_temp','Activación filtrado temporal',value=True)

    ##Salida objeto UI selector periodo tiempo. del sistema experto
    @output
    @render.ui
    def date_range():
        #Condicionamos la creacion del date range  a un evento en input.filt_temp
        if input.filt_temp():
            min_Datos= Datos().dia.min().strftime('%Y-%m-%d')#Convertimos el datetime a str
            max_Datos= Datos().dia.max().strftime('%Y-%m-%d')#Convertimos el datetime a str
            temp_in=ui.input_date_range('temp_range',
                                        'Selecciona periodo',
                                         start = '2016-03-01',
                                         end= '2016-06-01',
                                         min= min_Datos, #Mínima fecha que puedo seleccionar en calendario
                                         max= max_Datos, #Máxima fecha que puedo seleccionar en calendario
                                         format= "yyyy-mm-dd",
                                         separator = "a",
                                         weekstart = 1,
                                         language="es"
                                        )
            return temp_in
        else:
            return ui.h6('Resultados de histórico completo de la máquina '+ input.matricula_id())

    #Variable reactiva para aplicar filtros pestaña Sistema experto (Máquina, alarmas, tiempo)
    @reactive.Calc
    def Datos_filt1():

        condicion_filt1_A=reactive.Value(Datos().matricula == input.matricula_id()) #Filtro matriculas
        condicion_filt1_B=Datos().dia>=input.temp_range()[0] #Fecha de inicio en formato date()
        condicion_filt1_C=Datos().dia<=input.temp_range()[1] #Fecha de fin en formato date()
    
        if input.filt_temp():
            df1=Datos().copy().loc[(condicion_filt1_A.get() & condicion_filt1_B & condicion_filt1_C)  ,:]
            return  df1
        else:
            df1=Datos().copy().loc[condicion_filt1_A.get() ,:]
            
            return df1
    
    ##Salida gráfico 1. Evolucion de probabilidad de orden en sistema experto
    @output
    @render.plot
    def grafico11():
        #Condicionamos la creación del grafico 2 a un evento en input.variable_dataset
        if input.variable_dataset():
            graf11=sns.relplot(x="dia",y="p_orden",data=Datos_filt1(),kind="line")
            graf11.fig.suptitle("Evolución de la probabilidad de avería de la  "+input.matricula_id())
            plt.xticks(rotation=45)
            return graf11

    #Salida gráfico 2 Evolucion de alarma  seleccionada en sistema experto.
    @output
    @render.plot
    def grafico12():
        #Condicionamos la creación del grafico 2 a un evento en input.variable_dataset
        if input.variable_dataset():
            graf12=sns.relplot(x="dia",y=input.variable_dataset(),data=Datos_filt1(),kind="line")
            graf12.fig.suptitle("Evolución de la intensidad de " +
                              input.variable_dataset() +
                              " en la " +
                              input.matricula_id())
            plt.xticks(rotation=45)
    
            return graf12
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