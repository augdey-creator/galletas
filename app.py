import streamlit as st
import math
import pandas as pd

st.title("🍪 Calculadora de Costos de Galletas")

# INPUT
galletas = st.number_input(
    "¿Cuántas galletas quieres hacer?", min_value=1, value=15)

# BASE
base = st.selectbox("Selecciona la base:", ["Chocolate", "Vainilla"])

# RELLENO
usar_relleno = st.checkbox("¿Lleva relleno?")
relleno = None
if usar_relleno:
    relleno = st.selectbox("Tipo de relleno:", [
                           "Queso Philadelphia", "Nutella"])

# TOPPINGS
st.subheader("Toppings (máx. 200g en total)")
toppings_opciones = ["Almendra", "Chispas chocolate", "Arándano", "Pistache"]
toppings_seleccionados = st.multiselect(
    "Selecciona toppings:", toppings_opciones)

toppings_total = 200
toppings_dict = {}

if toppings_seleccionados:
    gramos_por_topping = toppings_total / len(toppings_seleccionados)
    for t in toppings_seleccionados:
        toppings_dict[t.lower()] = gramos_por_topping

# 🔥 IMPORTANTE: receta base = 15 galletas
GALLETAS_BASE = 15
factor = galletas / GALLETAS_BASE

# RECETAS
base_chocolate = {
    "mantequilla": 220,
    "azúcar refinada": 280,
    "huevos": 2,
    "vainilla": 10,
    "cocoa": 50,
    "harina": 420,
    "fécula de maíz": 40,
    "bicarbonato": 3,
    "sal": 4
}

base_vainilla = {
    "mantequilla": 200,
    "azúcar refinada": 310,
    "huevos": 2,
    "vainilla": 15,
    "harina": 460,
    "fécula de maíz": 40,
    "bicarbonato": 4,
    "sal": 4
}

receta = base_chocolate.copy() if base == "Chocolate" else base_vainilla.copy()

# RELLENO
if usar_relleno:
    if relleno == "Queso Philadelphia":
        receta["queso philadelphia"] = 225
    elif relleno == "Nutella":
        receta["nutella"] = 225

# TOPPINGS
receta.update(toppings_dict)

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
    "almendra": {"porcion": 907, "precio": 183},
    "chispas chocolate": {"porcion": 300, "precio": 125},
    "arándano": {"porcion": 120, "precio": 44},
    "pistache": {"porcion": 340, "precio": 215}
}

# CALCULO
resultados = []
costo_total_real = 0

for ingrediente, cantidad in receta.items():
    necesario = cantidad * factor

    if ingrediente not in costos:
        continue

    presentacion = costos[ingrediente]["porcion"]
    precio = costos[ingrediente]["precio"]

    # 💡 costo proporcional (REAL)
    costo_real = (necesario / presentacion) * precio
    costo_total_real += costo_real

    # 💡 compra necesaria (opcional mostrar)
    unidades = math.ceil(necesario / presentacion)

    resultados.append({
        "Ingrediente": ingrediente,
        "Necesario (g/unid)": round(necesario, 2),
        "Costo real": round(costo_real, 2),
        "Comprar (unidades)": unidades
    })

df = pd.DataFrame(resultados)

# OUTPUT
st.subheader("🛒 Insumos necesarios")
st.dataframe(df)

st.subheader("💰 Costos")

st.metric("Costo total receta", f"${round(costo_total_real, 2)} MXN")

costo_por_galleta = costo_total_real / galletas
st.metric("Costo por galleta", f"${round(costo_por_galleta, 2)} MXN")

# EXTRA (nivel negocio 🔥)
precio_sugerido = costo_por_galleta * 2.5
st.subheader("💡 Sugerencia de venta")
st.write(f"Precio sugerido por galleta: **${round(precio_sugerido, 2)} MXN**")
