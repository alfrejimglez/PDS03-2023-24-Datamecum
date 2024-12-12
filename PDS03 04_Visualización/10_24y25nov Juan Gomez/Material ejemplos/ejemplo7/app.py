from shiny import *

app_ui = ui.page_fluid(
    ui.h2('Ejemplo de uso de @reactive.Effect y reactive.event()'),
    ui.input_action_button("btn",
     "Púlsame para actualizar el número de pulsaciones de botón 2!"),
    ui.input_action_button("btn2", "Boton 2"  )
    
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
            ui.insert_ui(ui.p("Número de clicks al botón 2: ",
                              input.btn2()), 
                              selector="#btn2",
                              where="afterEnd"
        ) #ui.insert_ui permite insertar un elemento ui desde el servidor


app = App(app_ui, server)