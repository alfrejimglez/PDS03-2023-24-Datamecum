from shiny import App, ui

app_ui = ui.page_navbar(
    # Opciones definidas con ui.nav
    ui.nav("Consumibles",
            ui.h2("Ejemplo de page_navbar"),
           "Cosas referentes a consumibles"),
    ui.nav("Inventariable",
            ui.h2("Ejemplo de page_navbar"),
           "Cosas referentes a inventariables"),
    title= "Gestión de stocks", #Título de la barra de navegación
    selected="Inventariable", #Opción de arranque
    bg="IndianRed", #Color barra navegacion css,html
    window_title="Cuadro de mando empresa ACME",# Título en el navegador 
    lang="es" #Lenguaje 
    
    )


app = App(app_ui, None)