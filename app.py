import streamlit as st
import math
import pandas as pd

st.title("🍪 Calculadora de Insumos para Galletas")

# INPUT
galletas = st.number_input(
    "¿Cuántas galletas quieres hacer?", min_value=1, value=20)

# Supuesto
GALLETAS_BASE = 15
factor = galletas / GALLETAS_BASE

# RECETAS
receta = {
    "mantequilla": 220,
    "azúcar refinada": 280,
    "huevos": 2,
    "vainilla": 10,
    "cocoa": 50,
    "harina": 420,
    "fécula de maíz": 40,
    "bicarbonato": 3,
    "sal": 4,
    "queso philadelphia": 225,
    "nutella": 225,
    "toppings": 200
}

# COSTOS (presentación)
costos = {
    "mantequilla": {"porcion": 360, "precio": 80},
    "azúcar refinada": {"porcion": 2000, "precio": 82},
    "huevos": {"porcion": 30, "precio": 67},
    "vainilla": {"porcion": 150, "precio": 21},
    "cocoa": {"porcion": 200, "precio": 142},
    "harina": {"porcion": 1000, "precio": 17},
    "fécula de maíz": {"porcion": 425, "precio": 46},
    "bicarbonato": {"porcion": 227, "precio": 25},
    "sal": {"porcion": 750, "precio": 21},
    "queso philadelphia": {"porcion": 180, "precio": 48},
    "nutella": {"porcion": 650, "precio": 169},
    "toppings": {"porcion": 907, "precio": 183}
}

# CALCULO
resultados = []

costo_total = 0

for ingrediente, cantidad in receta.items():
    necesario = cantidad * factor
    presentacion = costos[ingrediente]["porcion"]
    precio = costos[ingrediente]["precio"]

    unidades = math.ceil(necesario / presentacion)
    costo = unidades * precio

    costo_total += costo

    resultados.append({
        "Ingrediente": ingrediente,
        "Necesario (g/unid)": round(necesario, 2),
        "Comprar (unidades)": unidades,
        "Costo": costo
    })

df = pd.DataFrame(resultados)

st.subheader("🛒 Insumos necesarios")
st.dataframe(df)

st.subheader("💰 Costo total estimado")
st.success(f"${costo_total} MXN")
