from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_numeric("x", "Enter a value to add to the list:", 1),
    ui.input_action_button("submit", "Add Value"),
    ui.p(
        ui.output_text_verbatim("out")
    ),
)

def server(input, output, session):
    # Stores all the values the user has submitted so far
    user_provided_values = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.submit)
    def add_value_to_list():
        
        #Evaluar las tres pruebas en clase!
        
        ## PRUEBA Uso de objetos mutables suceptibles de comportamientos ERRÁTICOS
        
        values = user_provided_values()
        values.append(input.x())
        user_provided_values.set(values)

        # PRUEBA Uso de objetos mutables  CORRECTO OPCIÓN 1
        
        #  values = user_provided_values().copy()
        #  values.append(input.x())
        #  user_provided_values.set(values)

        ## PRUEBA Uso de objetos mutables  CORRECTO OPCIÓN 2
        
        # user_provided_values.set(user_provided_values() + [input.x()])
        
        

    @output
    @render.text
    def out():
        return f"Values: {user_provided_values()}"

app = App(app_ui, server)