from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2('Creación de objetos de la UI en el server'),
    ui.input_switch("switch1","Selecciona Rango slider",value=False),
    
    #Elementos de salida, en este caso un elemento de la UI
    #en particular, un slider construido en el server.
    ui.h2('Elemento de entrada de la UI made in server!'),
    ui.output_ui("slider_made_server")
)

def server(input, output, session):
    @output
    @render.ui
    def slider_made_server():
        if not input.switch1():
            g=ui.input_slider("slider1",
            "Slider de 1 a 1000",1,1000,500)
        else:
            g=ui.input_slider("slider1",
            "Slider de 1001 a 2000",1001,2000,1500)     
        return g

app = App(app_ui, server)