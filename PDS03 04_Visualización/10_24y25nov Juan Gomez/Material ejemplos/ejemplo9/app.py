from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.h2("Ejemplo de uso de reactive.Value"),
    ui.input_action_button("toggle",
                           "Invierte el valor del booleano"),
    ui.output_text_verbatim("txt"),
)

def server(input, output, session):
    x = reactive.Value(True)

    @reactive.Effect
    @reactive.event(input.toggle)
    def _():
        x.set(not x())

    @output
    @render.text
    def txt():
        return str(x())

app = App(app_ui, server)