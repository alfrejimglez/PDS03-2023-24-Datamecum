import streamlit as st
from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import pandas as pd

# Datos
pinguinos = load_penguins()

# Sidebar
with st.sidebar:
    islas = set(pinguinos.island)
    islas.add("Mostrar todos")
    years = set(pinguinos.year)
    years.add("Mostrar todos")
    isla_proc = st.selectbox("Selecciona isla", islas, index = 1)
    year = st.selectbox("Selecciona año", years, index = 2)

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