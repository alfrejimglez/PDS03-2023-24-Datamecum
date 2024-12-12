from shiny import App, render, ui

#Interfaz de usuario
app_ui = ui.page_fluid(
    #Titulo
    ui.panel_title("Ejercicio 2. Elementos de entrada. Datamecum."),
    
    #layout sidebar
    ui.layout_sidebar(
         
         # Panel lateral
         ui.panel_sidebar(
            ui.h3("Elementos de entrada"),
            ui.input_file("Fichero_ID", "Selecciona tu fichero de ID"),

            ui.input_select("Desplegable1","Selecciona asignatura", 
                            choices = {"VD":"Visualización de datos", "TD":"Tratamiento de datos"}),
            
            ui.input_radio_buttons("Radiobotones","Selecciona lo que quieres hacer en la asignatura",
                                    choices={"7":"Aprobar","3":"Suspender"}),
            ui.input_checkbox("Check","Repites la  asignatura", value = False),

            ui.input_checkbox_group("GrupoCheck1","En caso de repitición, ¿Cúal?",
                                    choices={"1":"Tratamiento de datos","2":"Visualización de datos"},
                                    inline=True),

             ui.input_date_range("Periodo1","Periodo a evaluar", 
                                start = "2020-01-01",end =  "2021-12-31",
                                min = "2018-01-01", max = "2022-01-01",
                                format = "yyyy-mm-dd", weekstart = 1,
                                language = "es", separator = "a"),

            ui.input_slider("Slider1","Elige tu nota numéricamente",
                            min= 0,max = 10,value = 5,step= 0.2),
            ),
        #Panel principal
        ui.panel_main(
            ui.h1("Hola Mundo, mi primer programa..."),
            ui.h3("Si estás viendo esto parece que todo funciona bien")
            )
        )
    )
    



#El server vacio con pass
def server(input, output, session):
    pass

app = App(app_ui, server)
