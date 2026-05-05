import streamlit as st
import pandas as pd
import math
import io

st.set_page_config(page_title="Galletas Guapas", layout="centered")

# ======================
# 🎨 ESTILOS
# ======================
st.markdown("""
<style>
.stApp { background-color: #fff1f2; }

.block-container {
    max-width: 900px;
    margin: auto;
}

/* TITULO */
h1 {
    text-align: center;
    color: #7a0f2b;
    font-size: 30px;
    margin-bottom: 0;
}

/* SUBTITULO */
.subtitle {
    text-align: center;
    color: #9d174d;
    font-size: 14px;
}

/* TEXTO */
label, .stMarkdown, .stText {
    color: #111827 !important;
    font-weight: 500;
}

/* INPUTS */
.stNumberInput input {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
}

/* CARDS */
.card {
    border-radius: 16px;
    padding: 20px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* METRICAS */
.metric {
    font-size: 24px;
    font-weight: bold;
}

/* HR */
hr {
    border: none;
    height: 1px;
    background: #fecdd3;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown("""
<h1>🍪 Galletas Guapas</h1>
<p class="subtitle">Calculadora de producción y rentabilidad</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ======================
# CSV
# ======================


def cargar_costos(file):
    df = pd.read_csv(file, sep=None, engine="python", encoding="latin1")
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace("á", "a").str.replace("é", "e")
        .str.replace("í", "i").str.replace("ó", "o").str.replace("ú", "u")
    )
    return df


archivo = st.file_uploader("📂 Sube tu costos.csv", type=["csv"])

if archivo:
    costos_df = cargar_costos(archivo)
else:
    csv_default = """ingrediente,porcion,precio
mantequilla,360,80
azucar refinada,2000,82
huevos,30,67
vainilla,150,21
cocoa,200,142
harina,1000,17
fecula de maiz,425,46
bicarbonato,227,25
sal,750,21
queso philadelphia,180,48
nutella,650,169
almendra,907,183
chispas chocolate,300,125
arandano,120,44
pistache,340,215
"""
    costos_df = cargar_costos(io.StringIO(csv_default))

costos = {
    row["ingrediente"]: {"porcion": row["porcion"], "precio": row["precio"]}
    for _, row in costos_df.iterrows()
}

# ======================
# CONFIG
# ======================
st.subheader("⚙️ Configuración")

base = st.selectbox("Base", ["Chocolate", "Vainilla"])

usar_relleno = st.checkbox("¿Con relleno?")
relleno = st.selectbox(
    "Tipo", ["queso philadelphia", "nutella"]) if usar_relleno else None

toppings_sel = st.multiselect(
    "Toppings (200g total)",
    ["almendra", "chispas chocolate", "arandano", "pistache"]
)

toppings = {}
if toppings_sel:
    gramos = 200 / len(toppings_sel)
    for t in toppings_sel:
        toppings[t] = gramos

st.markdown("---")

# ======================
# RECETA
# ======================
base_choc = {
    "mantequilla": 220, "azucar refinada": 280, "huevos": 2,
    "vainilla": 10, "cocoa": 50, "harina": 420,
    "fecula de maiz": 40, "bicarbonato": 3, "sal": 4
}

base_vain = {
    "mantequilla": 200, "azucar refinada": 310, "huevos": 2,
    "vainilla": 15, "harina": 460,
    "fecula de maiz": 40, "bicarbonato": 4, "sal": 4
}

receta = base_choc.copy() if base == "Chocolate" else base_vain.copy()

if relleno:
    receta[relleno] = 225

receta.update(toppings)

# ======================
# INVENTARIO (2 COLUMNAS)
# ======================
st.subheader("📦 Inventario")

ingredientes = list(receta.keys())
inventario = {}

cols = st.columns(2)

for i, ing in enumerate(ingredientes):
    col = cols[i % 2]
    with col:
        if ing == "huevos":
            inventario[ing] = st.number_input(
                f"{ing} (pzas)", 0.0, 500.0, 0.0, key=f"inv_{ing}")
        else:
            inventario[ing] = st.number_input(
                f"{ing} (g)", 0.0, 10000.0, 0.0, key=f"inv_{ing}")

st.markdown("---")

# ======================
# PRODUCCIÓN
# ======================
total_g = sum([v if k != "huevos" else 0 for k, v in receta.items()])
total_g += receta.get("huevos", 0) * 50
galletas = total_g / 100

# ======================
# COSTOS
# ======================
costo_insumos = sum(
    (cant / costos[ing]["porcion"]) * costos[ing]["precio"]
    for ing, cant in receta.items() if ing in costos
)

gastos_fijos = costo_insumos * 0.33
costo_total = costo_insumos + gastos_fijos
costo_galleta = costo_total / galletas if galletas > 0 else 0

multiplicador = st.slider("Multiplicador de precio", 1.0, 5.0, 2.5)

precio_sugerido = costo_galleta * multiplicador
ganancia_por_galleta = precio_sugerido - costo_galleta
ganancia_total = ganancia_por_galleta * galletas

# ======================
# DASHBOARD
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
    <h3>📊 Producción</h3>
    <div class="metric">{round(galletas, 1)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
    <h3>💰 Costos</h3>
    <div class="metric">${round(costo_total, 2)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
    <h3>💵 Ganancia</h3>
    <div class="metric">${round(ganancia_total, 2)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================
# COMPRAS
# ======================
rows = []
costo_compra = 0

for ing, req in receta.items():
    disp = inventario.get(ing, 0)
    falt = max(req - disp, 0)

    if ing in costos:
        c = costos[ing]
        unidades = math.ceil(falt / c["porcion"]) if falt > 0 else 0
        costo = unidades * c["precio"]
    else:
        unidades = 0
        costo = 0

    costo_compra += costo

    rows.append({
        "Ingrediente": ing,
        "Faltante": round(falt, 2),
        "Comprar": unidades,
        "Costo": round(costo, 2)
    })

df = pd.DataFrame(rows).sort_values(by="Costo", ascending=False)

st.subheader("🛒 Compras necesarias")
st.dataframe(df, use_container_width=True, hide_index=True)

st.metric("Total compra", f"${round(costo_compra, 2)}")
