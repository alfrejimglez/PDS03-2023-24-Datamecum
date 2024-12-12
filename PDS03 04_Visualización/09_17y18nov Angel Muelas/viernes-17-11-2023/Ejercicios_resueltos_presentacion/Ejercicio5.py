import streamlit as st
from palmerpenguins import load_penguins
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Datos
pinguinos = load_penguins()
secs = np.random.normal(loc = 3, scale = 1, size = 1)[0]
time.sleep(secs)

# Comprobaciones tiempos
if 'tiempos' not in st.session_state:
    st.info("No hay registros previos. Guardando el tiempo. Vuelve a ejecutar el programa.")
    
else:
    if st.session_state.tiempos > secs:
        st.success("La función ha tardado MENOS tiempo en cargar los datos.")
    else:
        st.error("La función ha tardado MÁS tiempo en cargar los datos.")

st.session_state.tiempos = secs


# Sidebar
with st.sidebar:
    islas = set(pinguinos.island)
    islas.add("Mostrar todos")
    years = set(pinguinos.year)
    years.add("Mostrar todos")
    isla_proc = st.selectbox("Selecciona isla", islas)
    year = st.selectbox("Selecciona año", years)

if isla_proc != "Mostrar todos":
    pinguinos = pinguinos.loc[pinguinos.island == isla_proc]

if year != "Mostrar todos":
    pinguinos = pinguinos.loc[pinguinos.year == year]

# Main
st.title("Solución del ejercicio 4.")
fig, ax = plt.subplots(ncols=2, figsize=(15, 10))

frecuencias = pd.crosstab(index = pinguinos.species, columns='frec')
frecuencias.plot.bar(ax = ax[0])
ax[0].get_legend().set_visible(False)

for especie in set(pinguinos.species):
    subset = pinguinos.loc[pinguinos.species == especie]
    ax[1].scatter(x = subset.flipper_length_mm, 
                y = subset.bill_depth_mm)
                
ax[1].legend(set(pinguinos.species))

st.pyplot(fig)
