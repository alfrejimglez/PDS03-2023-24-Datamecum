
from pathlib import Path
from shiny import ui, render, App


app_ui = ui.page_fluid(
    ui.column(6,ui.tags.h2("Cargamos una imagen..."), #también va ui.h2 
    ui.column(6,ui.tags.img(width=50,
                            height = 50, 
                            src="logo.png")) # también va ui.img
    )
)

imagenes_dir = Path(__file__).parent / "imagenes"
app = App(app_ui, None, static_assets=imagenes_dir)
