from shiny import *

app_ui = ui.page_fluid(
    ui.h2('Ejemplo de uso de @reactive.Effect'),
    ui.input_action_button("btn", "Púlsame!"),
    
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    
    def _():
        if input.btn()!=0:
            ui.insert_ui(ui.p("Número de clicks al botón: ",
                              input.btn()), 
                         selector="#btn",
                         where="afterEnd"
        )


app = App(app_ui, server)