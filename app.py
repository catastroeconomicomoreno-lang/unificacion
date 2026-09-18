import os
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Liquidador de Tasas Municipales (2023 - 2025)",
    layout="wide",
)

# Estilos CSS con regla para imprimir solo la pestaña/año activo en 1 hoja A4
st.markdown(
    """
    <style>
        .stApp, html, body, [data-testid="stAppViewContainer"],
        label, p, span, div, [data-testid="stWidgetLabel"] p, .stMarkdown p {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-size: 11px !important;
        }
        
        [data-testid="stWidgetLabel"] {
            margin-bottom: 1px !important;
            padding-bottom: 0px !important;
        }
        
        div.row-widget.stRadio > div {
            flex-direction: row !important;
            gap: 8px !important;
        }
        
        .resultado-box {
            background-color: #ffffff !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 2px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            text-align: center !important;
            min-height: 24px !important;
        }
        
        .resultado-box-tabla {
            background-color: #ffffff !important;
            padding: 3px 6px !important;
            border-radius: 4px !important;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 2px !important;
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            text-align: left !important;
            min-height: 24px !important;
        }
        
        .tabla-header {
            background-color: #ffffff !important;
            color: #1e293b !important;
            font-weight: normal;
            text-align: left;
            padding: 4px 6px !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 4px !important;
            font-size: 10px !important;
            text-transform: uppercase;
            min-height: 24px !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }
        
        .titulo-seccion-tabla {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 4px 8px;
            font-weight: normal;
            text-align: center;
            margin-bottom: 4px;
            border-radius: 4px;
            font-size: 11px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }
        
        .resultado-label, .resultado-valor {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-weight: normal !important;
            font-size: 11px !important;
        }
        
        .stButton>button {
            background-color: #0284c7 !important;
            color: white !important;
            font-weight: normal !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 4px 10px !important;
            width: 100% !important;
            font-size: 11px !important;
        }

        /* Configuración de Impresión A4 para imprimir SOLO el año activo */
        @media print {
            @page {
                size: A4 portrait;
                margin: 8mm;
            }
            body, .stApp, [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
                color: #000000 !important;
                font-size: 8pt !important;
            }
            header, [data-testid="stSidebar"], [data-testid="stHeader"], .stDeployButton, [data-testid="stDecoration"], .stTabs [role="tablist"], .stButton {
                display: none !important;
            }
            [data-testid="stAppViewContainer"] {
                overflow: visible !important;
                position: static !important;
            }
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                max-width: 100% !important;
            }
            .resultado-box, .resultado-box-tabla, .tabla-header, .titulo-seccion-tabla {
                border: 1px solid #cbd5e1 !important;
                page-break-inside: avoid !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Encabezado común
ruta_base = os.path.dirname(__file__)
ruta_encabezado = os.path.join(ruta_base, "encabezado.png")
if os.path.exists(ruta_encabezado):
  st.image(ruta_encabezado, use_container_width=True)

# ==============================================================================
# INICIALIZACIÓN DE SESSION STATE (MEMORIA COMPARTIDA ENTRE AÑOS)
# ==============================================================================
if "partida" not in st.session_state:
  st.session_state["partida"] = ""
if "estado" not in st.session_state:
  st.session_state["estado"] = "EDIFICADO"
if "uso" not in st.session_state:
  st.session_state["uso"] = "RESIDENCIAL"
if "acceso" not in st.session_state:
  st.session_state["acceso"] = "NO"
if "zonif" not in st.session_state:
  st.session_state["zonif"] = "A/B"
if "bc" not in st.session_state:
  st.session_state["bc"] = "NO"
if "da" not in st.session_state:
  st.session_state["da"] = "NO"
if "be" not in st.session_state:
  st.session_state["be"] = "NO"
if "edenor" not in st.session_state:
  st.session_state["edenor"] = "0,00"
if "sup_terreno" not in st.session_state:
  st.session_state["sup_terreno"] = "300,00"
if "sup_edificada" not in st.session_state:
  st.session_state["sup_edificada"] = "0,00"
if "va" not in st.session_state:
  st.session_state["va"] = "300000,00"
if "liq_previa" not in st.session_state:
  st.session_state["liq_previa"] = "0,00"

# Formateador auxiliar
def fmt(val):
  return f"${val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ==============================================================================
# PANEL DE DATOS GENERALES (SE TRASLADAN A TODOS LOS AÑOS)
# ==============================================================================
st.markdown(
    "### 📋 DATOS DE LA PROPIEDAD (Se comparten para todas las liquidaciones)"
)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p2:
  st.session_state["partida"] = st.text_input(
      "PARTIDA MUNICIPAL N°:", value=st.session_state["partida"]
  )

col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
  st.session_state["estado"] = st.radio(
      "Estado:",
      ["EDIFICADO", "BALDIO"],
      index=["EDIFICADO", "BALDIO"].index(st.session_state["estado"]),
  )
with col_f2:
  st.session_state["uso"] = st.radio(
      "Uso:",
      ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"],
      index=["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"].index(
          st.session_state["uso"]
      ),
  )
with col_f3:
  st.session_state["acceso"] = st.radio(
      "Acceso Principal:",
      ["NO", "SI"],
      index=["NO", "SI"].index(st.session_state["acceso"]),
  )
with col_f4:
  st.session_state["zonif"] = st.selectbox(
      "Zonificación:",
      ["A/B", "F", "OTRA"],
      index=["A/B", "F", "OTRA"].index(st.session_state["zonif"]),
  )

col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
  st.session_state["bc"] = st.radio(
      "Buen Contribuyente (BC 10%):",
      ["NO", "SI"],
      horizontal=True,
      index=["NO", "SI"].index(st.session_state["bc"]),
  )
with col_d2:
  st.session_state["da"] = st.radio(
      "Débito Automático (DA 10%):",
      ["NO", "SI"],
      horizontal=True,
      index=["NO", "SI"].index(st.session_state["da"]),
  )
with col_d3:
  st.session_state["be"] = st.radio(
      "Boleta Electrónica (BE 5%):",
      ["NO", "SI"],
      horizontal=True,
      index=["NO", "SI"].index(st.session_state["be"]),
  )
with col_d4:
  st.session_state["edenor"] = st.text_input(
      "EDENOR ($):", value=st.session_state["edenor"]
  )

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
  st.session_state["sup_terreno"] = st.text_input(
      "Superficie Terreno (m²):", value=st.session_state["sup_terreno"]
  )
with col_s2:
  st.session_state["sup_edificada"] = st.text_input(
      "Superficie Edificada (m²):", value=st.session_state["sup_edificada"]
  )
with col_s3:
  st.session_state["va"] = st.text_input(
      "Valuación Fiscal ($):", value=st.session_state["va"]
  )
with col_s4:
  st.session_state["liq_previa"] = st.text_input(
      "Última liquidación año anterior ($):",
      value=st.session_state["liq_previa"],
  )

st.markdown("---")

# ==============================================================================
# PESTAÑAS POR EJERCICIO FISCAL (2023, 2024, 2025)
# ==============================================================================
tab_2023, tab_2024, tab_2025 = st.tabs(
    ["EJERCICIO 2023", "EJERCICIO 2024", "EJERCICIO 2025"]
)

# ------------------------------------------------------------------------------
# FUNCION GENERADORA DE LIQUIDACION POR AÑO
# ------------------------------------------------------------------------------
def render_liquidador(
    anio_ejercicio,
    ca_default,
    minimos,
    tabla_base,
    pct_aumentos,
    cuota1_pct_notope,
    cuotas_no_edenor,
):
  st.markdown(f"### LIQUIDACIÓN EJERCICIO FISCAL {anio_ejercicio}")

  col_sub1, col_sub2, col_sub3 = st.columns(3)
  with col_sub1:
    var_tope = st.radio(
        f"Liberar Tope {anio_ejercicio}:", ["NO", "SI"], key=f"tope_{anio_ejercicio}"
    )
  with col_sub2:
    anio_val = st.selectbox(
        f"Valuación año {anio_ejercicio}:",
        ["Anterior a 2023", "2024", "2025"],
        key=f"val_anio_{anio_ejercicio}",
    )

  # Cálculo Coeficiente CA según el año
  if anio_val == "Anterior a 2023":
    ca = 6.10
  elif anio_val == "2024":
    ca = 2.00
  else:
    ca = 1.00

  # Conversiones
  try:
    sup_t = (
        float(st.session_state["sup_terreno"].replace(".", "").replace(",", "."))
        if st.session_state["sup_terreno"]
        else 0.0
    )
    va = (
        float(st.session_state["va"].replace(".", "").replace(",", "."))
        if st.session_state["va"]
        else 0.0
    )
    monto_edenor = (
        float(st.session_state["edenor"].replace(".", "").replace(",", "."))
        if st.session_state["edenor"]
        else 0.0
    )
    liq_prev_num = (
        float(st.session_state["liq_previa"].replace(".", "").replace(",", "."))
        if st.session_state["liq_previa"]
        else 0.0
    )
  except ValueError:
    st.error("Por favor verifique los números ingresados.")
    return

  uso_sel = st.session_state["uso"]
  estado_sel = st.session_state["estado"]

  cu = (
      1.0
      if uso_sel == "RESIDENCIAL"
      else 1.1
      if uso_sel == "COMERCIAL"
      else 1.25
  )
  if estado_sel == "EDIFICADO":
    cb = 1.0
  else:
    cb = 1.6 if sup_t <= 500 else 1.7 if sup_t <= 5000 else 2.0

  if st.session_state["acceso"] == "SI":
    cap = (
        1.2
        if (uso_sel == "RESIDENCIAL" and estado_sel == "EDIFICADO")
        else 1.6
        if estado_sel == "BALDIO"
        else 1.5
    )
  else:
    cap = 1.0

  bi = round(va * ca * cu * cb * cap, 2)

  lim_inf, cfa_val, alic = 0.0, 0.0, 0.0
  for limite_sup, l_inf, cfa, alic_val in tabla_base:
    if bi <= limite_sup:
      lim_inf, cfa_val, alic = l_inf, cfa, alic_val
      break

  excedente = max(0.0, bi - lim_inf)
  tasa_anual = round(((excedente * alic) + cfa_val), 2)
  tasa_mensual = round(tasa_anual / 12, 2)

  tasa_proteccion = round(tasa_mensual * 0.095, 2)
  tasa_salud = round(tasa_mensual * 0.105, 2)

  monto_bc = (
      round(tasa_mensual * 0.10, 2) if st.session_state["bc"] == "SI" else 0.0
  )
  base_da = tasa_mensual - monto_bc
  monto_da = (
      round(base_da * 0.10, 2) if st.session_state["da"] == "SI" else 0.0
  )
  base_be = base_da - monto_da
  monto_be = (
      round(base_be * 0.05, 2) if st.session_state["be"] == "SI" else 0.0
  )

  subtotal_con_desc = tasa_mensual - monto_bc - monto_da - monto_be
  tasa_total = round(
      subtotal_con_desc + tasa_proteccion + tasa_salud - monto_edenor, 2
  )

  minimo_uso = minimos.get(uso_sel, 0.0)
  if var_tope == "NO" and tasa_total < minimo_uso:
    tasa_total = minimo_uso

  # Mostrar Resumen Base Imponible y Coeficientes
  c_bi, c_ca, c_cu, c_cb, c_cap = st.columns(5)
  with c_bi:
    st.markdown(
        f'<div class="resultado-box"><span class="resultado-label">BI:</span>'
        f' <span class="resultado-valor">{fmt(bi)}</span></div>',
        unsafe_allow_html=True,
    )
  with c_ca:
    st.markdown(
        f'<div class="resultado-box"><span class="resultado-label">CA:</span>'
        f' <span class="resultado-valor">{ca}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cu:
    st.markdown(
        f'<div class="resultado-box"><span class="resultado-label">CU:</span>'
        f' <span class="resultado-valor">{cu}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cb:
    st.markdown(
        f'<div class="resultado-box"><span class="resultado-label">CB:</span>'
        f' <span class="resultado-valor">{cb}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cap:
    st.markdown(
        f'<div class="resultado-box"><span class="resultado-label">CAP:</span>'
        f' <span class="resultado-valor">{cap}</span></div>',
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      f'<div class="titulo-seccion-tabla">Aplicación Tabla de Incrementos por'
      f" Cuota ({anio_ejercicio})</div>",
      unsafe_allow_html=True,
  )

  col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns(
      [1.3, 1, 1, 1, 1, 1, 1]
  )
  with col_t1:
    st.markdown('<div class="tabla-header">CUOTAS</div>', unsafe_allow_html=True)
  with col_t2:
    st.markdown(
        '<div class="tabla-header">Subtotal</div>', unsafe_allow_html=True
    )
  with col_t3:
    st.markdown(
        '<div class="tabla-header">Desc. BC</div>', unsafe_allow_html=True
    )
  with col_t4:
    st.markdown(
        '<div class="tabla-header">Desc. DA</div>', unsafe_allow_html=True
    )
  with col_t5:
    st.markdown(
        '<div class="tabla-header">Desc. BE</div>', unsafe_allow_html=True
    )
  with col_t6:
    st.markdown(
        '<div class="tabla-header">Desc. Edenor</div>', unsafe_allow_html=True
    )
  with col_t7:
    st.markdown('<div class="tabla-header">TOTAL</div>', unsafe_allow_html=True)

  sub_c_acumulado = 0.0

  for i in range(1, 13):
    pct = pct_aumentos[i - 1]

    if i == 1:
      if var_tope == "NO":
        sub_c_acumulado = round(
            liq_prev_num * (1.0 + (cuota1_pct_notope / 100.0)), 2
        )
        nombre_cuota = f"CUOTA 1-{anio_ejercicio} ({cuota1_pct_notope}%)"
      else:
        sub_c_acumulado = tasa_mensual
        nombre_cuota = f"CUOTA 1-{anio_ejercicio} (0%)"
    else:
      nombre_cuota = f"CUOTA {i}-{anio_ejercicio} ({pct}%)"
      if pct > 0:
        sub_c_acumulado = round(sub_c_acumulado * (1.0 + (pct / 100.0)), 2)

    sub_c = sub_c_acumulado

    m_bc_c = (
        round(sub_c * 0.10, 2) if st.session_state["bc"] == "SI" else 0.0
    )
    base_da_c = sub_c - m_bc_c
    m_da_c = (
        round(base_da_c * 0.10, 2) if st.session_state["da"] == "SI" else 0.0
    )
    base_be_c = base_da_c - m_da_c
    m_be_c = (
        round(base_be_c * 0.05, 2) if st.session_state["be"] == "SI" else 0.0
    )

    sub_desc_c = sub_c - m_bc_c - m_da_c - m_be_c
    prot_c = round(sub_c * 0.095, 2)
    salud_c = round(sub_c * 0.105, 2)

    m_edenor_c = 0.0 if i in cuotas_no_edenor else monto_edenor

    total_cuota = round(sub_desc_c + prot_c + salud_c - m_edenor_c, 2)
    if var_tope == "NO" and total_cuota < minimo_uso:
      total_cuota = minimo_uso

    r_c1, r_c2, r_c3, r_c4, r_c5, r_c6, r_c7 = st.columns([1.3, 1, 1, 1, 1, 1, 1])
    with r_c1:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-label">{nombre_cuota}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c2:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(sub_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c3:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(m_bc_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c4:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(m_da_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c5:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(m_be_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c6:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(m_edenor_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c7:
      st.markdown(
          f'<div class="resultado-box-tabla"><span class="resultado-valor"'
          f' style="color:#0284c7;">{fmt(total_cuota)}</span></div>',
          unsafe_allow_html=True,
      )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button(
      f"🖨️ IMPRIMIR INFORME {anio_ejercicio} EN A4",
      key=f"btn_print_{anio_ejercicio}",
  ):
    st.markdown("""<script>window.print();</script>""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# PARÁMETROS ESPECÍFICOS POR AÑO
# ------------------------------------------------------------------------------
TABLA_2025 = [
    (1800000.0, 0.0, 79911.52, 0.0),
    (2025000.0, 1800000.0, 79911.52, 0.0150),
    (2295000.0, 2025000.0, 91179.53, 0.0152),
    (2565000.0, 2295000.0, 105066.59, 0.0154),
    (4050000.0, 2565000.0, 119136.38, 0.0156),
    (6750000.0, 4050000.0, 243206.31, 0.0160),
    (9450000.0, 6750000.0, 480748.17, 0.0164),
    (12150000.0, 9450000.0, 621446.03, 0.0169),
    (14850000.0, 12150000.0, 812393.14, 0.0170),
    (float("inf"), 14850000.0, 967708.96, 0.0172),
]

with tab_2023:
  render_liquidador(
      anio_ejercicio="2023",
      ca_default=6.10,
      minimos={"RESIDENCIAL": 3000.0, "COMERCIAL": 8000.0, "INDUSTRIAL": 15000.0},
      tabla_base=TABLA_2025,
      pct_aumentos=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      cuota1_pct_notope=0.0,
      cuotas_no_edenor=[],
  )

with tab_2024:
  render_liquidador(
      anio_ejercicio="2024",
      ca_default=2.00,
      minimos={"RESIDENCIAL": 5000.0, "COMERCIAL": 12000.0, "INDUSTRIAL": 25000.0},
      tabla_base=TABLA_2025,
      pct_aumentos=[0, 0, 0, 5.0, 0, 0, 5.0, 0, 0, 5.0, 0, 0],
      cuota1_pct_notope=10.0,
      cuotas_no_edenor=[6, 8],
  )

with tab_2025:
  render_liquidador(
      anio_ejercicio="2025",
      ca_default=1.00,
      minimos={
          "RESIDENCIAL": 6662.0,
          "COMERCIAL": 18273.0,
          "INDUSTRIAL": 36546.0,
      },
      tabla_base=TABLA_2025,
      pct_aumentos=[0, 0, 0, 7.478, 0, 0, 8.2, 0, 0, 5.5, 0, 0],
      cuota1_pct_notope=10.76,
      cuotas_no_edenor=[6, 8, 9],
  )

# Pie de página
ruta_pie = os.path.join(ruta_base, "pie_pagina.png")
if os.path.exists(ruta_pie):
  st.markdown("<br>", unsafe_allow_html=True)
  st.image(ruta_pie, use_container_width=True)
