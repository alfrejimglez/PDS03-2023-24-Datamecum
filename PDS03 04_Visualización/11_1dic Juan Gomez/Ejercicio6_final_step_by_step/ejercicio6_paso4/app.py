
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
            ui.h2("Detección visual de anómalias."),
            ui.layout_sidebar(
                ui.panel_sidebar(ui.h4("Detección de anomalias por comparación visual"),
                                ui.hr(),
                                ui.output_ui('desplegable_matriculas_outliers'),
                                ui.output_ui('desplegable_variable_outliers')),
                ui.panel_main(ui.row(ui.column(7,ui.h2("Estado de la máquina y causa raiz alarmas"),offset=3)),
                                    ui.row(ui.hr()),
                                    ui.row(ui.column(5,ui.output_plot("grafico21"),offset=1),
                                    ui.column(6,ui.output_plot("grafico22")),
                                    ),
                                    ui.row(ui.hr()),
                                    ui.row(ui.column(9,ui.h2("Detalle de la máquina, Dataframe de la máquina."),offset=3)),
                                    ui.row(ui.column(7,ui.panel_well(ui.output_table("tabla1")),offset=3)),
                                    #)
                            ) 
            )
        ),
        #Interfaz de usuario DDD.Cuarta pestaña. EDA Alarmas.
        ui.nav("EDA Alarmas global",
            ui.layout_sidebar(
                ui.panel_sidebar(ui.h4("Filtrado de alarmas"),
                                ui.hr(),
                                ui.output_ui('desplegable_variable_alarmas'),
                                ui.output_ui('checkbox_out')),
                ui.panel_main(ui.h2("Comparación distribución de alarmas. Boxplots"),
                            ui.hr(),
                            ui.output_plot("grafico31"),
                            ui.h2("Comparación distribución de alarmas. Densidad de probabilidad."),
                            ui.hr(),
                            ui.column(10,ui.output_plot("grafico32"),offset=2),
                            )
            )
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

    #INICIO Funciones server AAA. Primera pestaña. Ingesta de datos.
    
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

    #FIN Funciones server AAA. 
    
    #INICIO Funciones server BBB. Segunda pestaña. Sistema Experto.

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
    #FIN Funciones server BBB.   
    
    
    #INICIO Funciones server CCC. Tercera pestaña. Análisis estado máquina. Detector de anomalias.

    ##Salida objeto ui deplegable alarma en deteccion anomalias 
    @output
    @render.ui
    def desplegable_variable_outliers():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            variables=tuple(Datos().columns)
            variables_ok=variables[-(len(variables)-3):-1] #Selecciono desde a1...203  indexando desde el final :)
            ui_02=ui.input_selectize("variable_dataset_02",
                            "Selecciona Alarmas",
                            choices=variables_ok,
                            multiple=True,
                            selected=["a1","a3","a4"])
            return ui_02

    #Variable reactiva para obtener mediana de las alarmas y p_orden total dataset
    @reactive.Calc
    def Datos_filt02_mediana():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            df02=Datos().copy()[['p_orden']+list(input.variable_dataset_02())] #convertimos a lista la selección para seleccionar columnas
            df02.dropna(inplace=True)
            mediana_total=df02.median(axis=0)
            return  [mediana_total[1:], mediana_total[0]] # Lista que contiene mediana de alarmas y mediana de p_orden
    
    # Creamos el objeto de salida de la UI desplegable de matriculas en deteccion de anomalias
    @output
    @render.ui
    def desplegable_matriculas_outliers():
        #Condicionamos la creación del desplegable matricula a un evento en input.Fichero
        if input.Fichero_ID():
            return ui.input_select("matricula_id_outliers","Selecciona una máquina",
                                 choices = tuple(Datos().matricula.unique()))

    # #Variable reactiva para obtener medina de alarmas, mediana p_orden y dataframe filtrado en maquina concreta
    @reactive.Calc
    def Datos_filt02_mediana_maquina():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            df02=Datos().copy()[['p_orden']+list(input.variable_dataset_02())] #convertimos a lista la selección para seleccionar columnas
            condicion_filt1_A= (Datos().matricula == input.matricula_id_outliers()) #Filtro matriculas
            df02_filt=df02.loc[condicion_filt1_A,:]
            df02_filt.dropna(inplace=True)
            mediana_maquina=df02_filt.median(axis=0)
            
            condicion_filt1_A_tot=reactive.Value(Datos().matricula == input.matricula_id_outliers()) #Filtro matriculas
            df02_total=Datos().copy().loc[condicion_filt1_A_tot.get() ,['dia', "matricula","p_orden"]+list(input.variable_dataset_02())]
            df02_total.dropna(inplace=True)
            # Lista que contiene mediana de alarmas, mediana de p_orden y dataframe de máquina concreta
            return  [mediana_maquina[1:],mediana_maquina[0], df02_total] 

    ##Salida gráfico 02. Radar plot en deteccion de anomalias.. pushing the limits matplolib :)
    @output
    @render.plot
    def grafico21():
        #Condicionamos la creación del grafico 02 a un evento en input.Fichero_ID
        if input.Fichero_ID():


            categories = list(Datos_filt02_mediana_maquina()[0].index) #es una serie!
            categories = [*categories, categories[0]]
            
            mediana_total = list(Datos_filt02_mediana()[0]) #[0] Accedemos solo a las alarmas
            mediana_total = [*mediana_total, mediana_total[0]]

            mediana_total_maquina = list(Datos_filt02_mediana_maquina()[0]) #[0] Accedemos solo a las alarmas
            mediana_total_maquina = [*mediana_total_maquina, mediana_total_maquina[0]]
            
            label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(mediana_total))
            
            graf21 = plt.figure(figsize=(5, 10))
            ax = plt.subplot(polar=True)
            ax.plot(label_loc, mediana_total, label='Normal')
            ax.plot(label_loc, mediana_total_maquina, label=input.matricula_id_outliers())
            ax.set_title('Comparacion máquinas con radar plot')#, size=20, y=1.05)
            lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
            ax.legend(loc='upper right')
            return graf21

    ##Salida gráfico 03, barplot p_orden en deteccion de anomalias
    @output
    @render.plot
    def grafico22():
        #Condicionamos la creación del grafico 01 a un evento en input.variable_dataset
        if input.Fichero_ID():
            categories=[ 'P_orden Normal', 'P_orden '+input.matricula_id_outliers()]
            p_ordenes= [ Datos_filt02_mediana()[1], Datos_filt02_mediana_maquina()[1]] #[1] P_orden
            graf22=sns.barplot(x=categories, y=p_ordenes)
            graf22.set_title("Probabilidad de intervención")
            plt.xticks(rotation=45)
            return graf22

            
    
    
   #Salida Tabla  en deteccion de anomalias
    @output
    @render.table
    def tabla1():
        #Condicionamos la creación de la tabla1 a un evento en input.variable_dataset
        if input.Fichero_ID():
            return Datos_filt02_mediana_maquina()[2]
            #return Datos_filt1()
    #FIN Funciones server CCC.
    
    #INICIO Funciones server DDD. Cuarta pestaña. Análisis estado máquina. EDA Alarmas global.
    
    ##Salida objeto ui deplegable de alarmas,  en EDA alarmas global
    @output
    @render.ui
    def desplegable_variable_alarmas():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            variables=tuple(Datos().columns)
            variables_ok=variables[-(len(variables)-3):-1] #Selecciono desde a1...203  indexando desde el final :)
            ui_01=ui.input_selectize("variable_dataset_01",
                            "Selecciona Alarmas",
                            choices=variables_ok,
                            multiple=True,
                            selected=["a1","a3","a4"])
            return ui_01

    ##Salida objeto ui interruptor remove outliers (valores por encima de mediana+1.5IQR) y ceros en EDA alarmas global
    @output
    @render.ui
    def checkbox_out():
        if input.Fichero_ID():
            return ui.input_checkbox('filt_out','Activación eliminación de outliers',value=True)


    #Variable reactiva para  crear dataset ordenado para pintar 
    # y remove outliers (valores por encima de mediana+1.5IQR) y ceros
    @reactive.Calc
    def Datos_filt01():
        #Condicionamos la creación del desplegable variable a un evento en input.FicheroID
        if input.Fichero_ID():
            df01=Datos().copy()[['dia']+list(input.variable_dataset_01())] #convertimos a lista la selección para seleccionar columnas
            df01.dropna(inplace=True)
            #Transformamos el dataset con melt dia, Alarma, Intensidd Alarm
            df01_tidy0 = (df01.melt(id_vars='dia', var_name='Alarma',value_name='Intensidad_Alarma').sort_values('dia').reset_index(drop=True))
            if input.filt_out():
                df01_tidy0=df01_tidy0.loc[df01_tidy0['Intensidad_Alarma']!=0,:]
                q3,q2, q1 = np.percentile(df01_tidy0['Intensidad_Alarma'], [75, 50, 25])
                outlier_umbral= q2+(1.5*(q3 - q1))
                df01_tidy=df01_tidy0.loc[df01_tidy0['Intensidad_Alarma'] < outlier_umbral,:]
                return  df01_tidy
            else:
                df01_tidy=df01_tidy0
                return  df01_tidy

    ##Salida gráfico 01. Boxplot  en EDA alarmas
    @output
    @render.plot
    def grafico31():
        #Condicionamos la creación del grafico 01 a un evento en input.variable_dataset
        if input.Fichero_ID():
            graf31=sns.boxplot(data=Datos_filt01() ,x='Alarma', y='Intensidad_Alarma',hue='Alarma')
            return graf31


 ##Salida gráfico 011. KDE plot en EDA alarmas.
    @output
    @render.plot
    def grafico32():
        #Condicionamos la creación del grafico 01 a un evento en input.variable_dataset
        if input.Fichero_ID():
        
            graf32=sns.displot(data=Datos_filt01(), x='Intensidad_Alarma', hue='Alarma', kind="kde")
            return graf32

#FIN Funciones server DDD.
app = App(app_ui, server, static_assets=datos_dir)