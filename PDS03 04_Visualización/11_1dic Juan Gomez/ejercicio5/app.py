
from pathlib import Path
from shiny import App, render,reactive, ui
from shiny.types import FileInfo #Para utilizar input_file



#Interfaz de usuario
#Elegimos entorno multipagina navbarpage
app_ui = ui.page_navbar(
    
    # Interfaz de usuario AAA. Primera pestaña. Ingesta de datos.
    ui.nav("Carga de fichero",
            ui.h2("Ingesta de datos.")    
        ),
    #Interfaz de usuario BBB.Segunda pestaña. Sistema experto.
    ui.nav("Sistema Experto",
        ui.h2("Análisis de necesidad de mantenimiento")
        ),
    #Interfaz de usuario CCC y DDD. Tercera y cuarta pestaña. Análisis  estado máquina
    # menu de pestañas, nav_menu
    ui.nav_menu("Análisis estado máquina", # Agrupación de dos páginas
        
        #Interfaz de usuario CCC.Tercera pestaña. Detección anomalias.
        ui.nav("Detector de anómalias",
            ui.h2("Detección visual de anómalias."),
            ),
        #Interfaz de usuario DDD.Cuarta pestaña. EDA Alarmas.
        ui.nav("EDA Alarmas global",
            ui.h2("EDA Alarmas."),
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
    
    @reactive.Effect
    def _():
        a=1


app = App(app_ui, server)