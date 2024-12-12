from shiny import App, reactive, render, ui
import asyncio #Funcinoes para crear funcinoes de ejcución asincrona

app_ui = ui.page_fluid(
    ui.h2("Ejemplo de uso de with reactive.isolate()"),
    ui.input_slider("n", "N", min=1, max=100, value=1),
    ui.input_action_button("compute", "Haz el cálculo!"),
    ui.output_text_verbatim("result", placeholder=True),
)

def server(input, output, session):

    @output
    @render.text
    async def result():
        input.compute()        # Hace que la salida depaenda de la entrada botón
        await asyncio.sleep(2) # Espera 2 segundos (simulando un cálculo largo)

        with reactive.isolate():
            # Con el bloque isolate evitamos la reaccion ante el cambio 
            # del slider input.n().
            return f"Result: {input.n()}"

app = App(app_ui, server)
