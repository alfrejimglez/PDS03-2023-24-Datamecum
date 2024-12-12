from shiny import *

app_ui = ui.page_fluid(
    ui.h2("Selectize modificado en el server con funciones update!"),
    ui.input_selectize("x", "Selecciona una opción", 
                       choices = ['Hola','Viejo','Mundo'], multiple=True),
    ui.input_action_button('btn',
    "Actualiza el selectize en el server, empleando update function"),

    ui.output_ui("desplegable"),
    ui.input_action_button('btn2', "Crea un selectize en el server")
)

def server(input: Inputs, output: Outputs, session: Session):
    
    #Actualizamos un selectize  creado en la UI
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
        ui.update_selectize(
            "x",
            choices=[f"Selección {i}" for i in range(10)],
            selected=["Selección 0", "Selección 1"],
            server=True)
    
    #Construimos un selectize en el server
    @output
    @render.ui
    @reactive.event(input.btn2)
    def desplegable():
        
        return ui.input_selectize(
            "x2",
            "Selectize construido en el server",
            choices=[f"Selección {i}" for i in range(10)],
            selected=["Selección 0", "Selección 1","Selección 2"],
            multiple=True
            #server=True
        )
#

app = App(app_ui, server, debug=True)