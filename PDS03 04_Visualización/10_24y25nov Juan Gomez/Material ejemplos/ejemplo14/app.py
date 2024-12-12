from shiny import App, ui

app_ui = ui.page_fluid(
    ui.navset_tab_card(
        # left hand side ----
        ui.nav_menu("Menu", #Creamos un desplegable de opciones 
            ui.nav("Material Teórico",
                   "Contenido Material Teórico"),
                    "Teoría para entenderlo todo!", #Descripción de la opción
                    "----",# Craemos una barra horizontal en el menu
                    
            ui.nav("Material Práctico",
                   "Contenido Material Práctico"),
        ),
        ui.nav("Compliance",
               ui.h2("Filosofía Datamecum"),
               "Contenido Datmecum"    
        ),

        # creamos un gap en la navegación 
        ui.nav_spacer(), #Creamos un gap en la barra de navegación

        # Con nav_control creamos una pestaña sin contenido, un enlace?
        ui.nav_control(
            ui.a("Datamecum",
                 href="https://www.datamecum.com", target="_blank")
        ),
    ),
)

app = App(app_ui, None)