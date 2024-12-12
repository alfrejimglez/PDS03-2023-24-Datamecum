from shiny import App, render, ui

#Interfaz de usuario
app_ui = ui.page_fluid(
    ui.h2("Ejercicio 1. Todo en orden?"),

    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h3("Barra para poner cosas"),
            ui.p("Aqui pondré elementos de entrada")
        ),

        # Mostramos un texto de encabezado 1
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
