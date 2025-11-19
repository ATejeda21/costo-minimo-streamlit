import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog

#Título de app
st.title("Modelo de Costo Mínimo")

#Ingresar tamaño de matriz
n_filas = st.number_input("Número de filas (ofertas):", min_value=1, value=3, step=1)
n_columnas = st.number_input("Número de columnas (demandas):", min_value=1, value=3, step=1)

#Entrada de la matriz de costos
st.write("Ingreso de los costos de transporte:")
costos = np.zeros((n_filas, n_columnas))  # Inicializa la matriz de costos
for i in range(n_filas):
    for j in range(n_columnas):
        #Deja al usuario ingresar el costo de transporte
        costos[i, j] = st.number_input(f"Costo [{i+1}, {j+1}]:", min_value=0.0)

#Ingresar ofertas y demandas
ofertas = []
demandas = []

st.write("Ingrese de las ofertas de los proveedores:")
for i in range(n_filas):
    #Deja al usuario ingresar las ofertas de los proveedores
    oferta = st.number_input(f"Oferta del proveedor {i+1}:", min_value=0.0)
    ofertas.append(oferta)

st.write("Ingrese las demandas de los clientes:")
for j in range(n_columnas):
    #Deja al usuario ingresar las demandas de los clientes
    demanda = st.number_input(f"Demanda del cliente {j+1}:", min_value=0.0)
    demandas.append(demanda)

#Se asegura de que las ofertas y demandas sean iguales
if sum(ofertas) != sum(demandas):
    #Muestra error si la suma de las ofertas no es igual a la de las demandas
    st.error("La suma de las ofertas debe ser igual a la suma de las demandas.")
else:
    #Resuelve el problema de costo mínimo usando scipy
    c = costos.flatten()  #Aplana la matriz de costos para el problema de optimización
    A_eq = []  #Matriz para las restricciones de igualdad

    #Restricciones de oferta (cada fila debe cumplir su oferta)
    for i in range(n_filas):
        fila = [0] * (n_filas * n_columnas)  #Inicializa la fila
        for j in range(n_columnas):
            fila[i * n_columnas + j] = 1  #Agrega 1s para la oferta del proveedor
        A_eq.append(fila)

    #Restricciones de demanda (cada columna debe cumplir su demanda)
    for j in range(n_columnas):
        columna = [0] * (n_filas * n_columnas)  #Inicializa la columna
        for i in range(n_filas):
            columna[i * n_columnas + j] = 1 #Agrega 1s para la demanda del cliente
        A_eq.append(columna)

    b_eq = np.concatenate([ofertas, demandas])  #Combina ofertas y demandas en un solo vector

    #Ejecuta la optimización
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs')

    if result.success:
        #Muestra los resultados si la optimización fue exitosa
        st.write("Solución óptima:")
        x = result.x.reshape((n_filas, n_columnas))  # Da forma a la solución
        df_result = pd.DataFrame(x, columns=[f"Cliente {i+1}" for i in range(n_columnas)],
                                 index=[f"Proveedor {i+1}" for i in range(n_filas)])
        st.write(df_result)  #Muestra la tabla con la solución
        st.write(f"Costo mínimo total: {result.fun}")  #Muestra el costo mínimo total
    else:
        #Muestra un error si no se encontró una solución óptima
        st.error("No se encontró una solución óptima.")
