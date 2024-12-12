import streamlit as st
import numpy as np
import pandas as pd

# Main
st.title ("Esta es mi primera aplicación")
datos = pd.DataFrame(
	np.random.randn(20, 3),
	columns = ['a', 'b', 'c'])

st.line_chart(datos)
st.dataframe(datos)
