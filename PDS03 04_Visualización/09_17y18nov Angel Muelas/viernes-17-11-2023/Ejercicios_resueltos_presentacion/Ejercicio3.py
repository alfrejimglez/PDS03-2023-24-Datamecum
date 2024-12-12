import streamlit as st
from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import pandas as pd

# Datos
pinguinos = load_penguins()
frecuencias = pd.crosstab(index = pinguinos.species, columns='frec')

# Main
st.title("Solución del ejercicio 3.")
fig, ax = plt.subplots(ncols=2, figsize=(15, 10))
frecuencias.plot.bar(ax = ax[0])
ax[0].get_legend().set_visible(False)

for especie in set(pinguinos.species):
    subset = pinguinos.loc[pinguinos.species == especie]
    ax[1].scatter(x = subset.flipper_length_mm, 
                y = subset.bill_depth_mm)
                
ax[1].legend(set(pinguinos.species))

st.pyplot(fig)