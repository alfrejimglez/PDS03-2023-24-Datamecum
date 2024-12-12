from shiny import module, ui, render, reactive, event
@module.ui
def counter_ui(label: str = "contador incremental"):
    return ui.div(
        {"style": "border: 1px solid #ccc; border-radius: 5px; margin: 5px 0;"},
        ui.h2("Esto es un " + label),
        ui.input_action_button(id="button", label=label),
        ui.output_text_verbatim(id="out"),
    )


@module.server
def counter_server(input, output, session, starting_value = 0):
    count = reactive.Value(starting_value)

    @reactive.Effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)

    @output
    @render.text
    def out():
        return f"La cuenta va por {count()}"
