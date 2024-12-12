from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Hola Mundo! Bienvenidos clase Datamecum."),
    #ui.input_slider( "n","N",0,100,0),


    ui.input_slider( id="n",label="Número Muestras", min=0, max=10, step=20, value=20),
    


    ui.output_text_verbatim("txt")
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"El valor de n*2 es {input.n() * 2}"


app = App(app_ui, server)
