
import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import altair as alt

# ---------------------- CONFIG ----------------------
VARIAZIONI = {
    'Monday': 0,
    'Tuesday': 0,
    'Wednesday': 0,
    'Thursday': 0,
    'Friday': 10,
    'Saturday': 20,
    'Sunday': 15,
}
FESTIVITA_EXTRA = 0.15  # +15% nei festivi

st.set_page_config(page_title="Affitto Smart – Prezzi Dinamici", layout="centered")
st.title("🏠 Affitto Smart – Calcolatore Prezzi Giornalieri")
st.caption("Versione migliorata per affitti brevi a Pietra Ligure")

# ---------------------- INPUT ----------------------
col1, col2 = st.columns(2)
with col1:
    anno = st.selectbox("📅 Anno", [2025, 2026], index=0)
with col2:
    mese_nome = st.selectbox("🗓️ Mese", list(calendar.month_name)[1:], index=7)
    mese = list(calendar.month_name).index(mese_nome)

prezzo_base = st.slider("💶 Prezzo base (per notte)", min_value=80, max_value=200, value=135, step=5)
considera_festivi = st.checkbox("📌 Aggiungi sovrapprezzo per festività", value=True)

# ---------------------- CALCOLO ----------------------
giorni_mese = calendar.monthrange(anno, mese)[1]
date_range = pd.date_range(start=f"{anno}-{mese:02d}-01", end=f"{anno}-{mese:02d}-{giorni_mese}")
tabella = []

for d in date_range:
    giorno_sett = d.strftime('%A')
    extra = VARIAZIONI.get(giorno_sett, 0)
    prezzo = prezzo_base + extra
    if considera_festivi and giorno_sett in ['Saturday', 'Sunday']:
        prezzo += prezzo * FESTIVITA_EXTRA
    tabella.append({
        "Data": d.strftime('%Y-%m-%d'),
        "Giorno": giorno_sett,
        "Prezzo (€)": round(prezzo)
    })

df = pd.DataFrame(tabella)

# ---------------------- OUTPUT ----------------------
st.subheader("📊 Prezzi giornalieri")
chart = alt.Chart(df).mark_line(point=True).encode(
    x='Data',
    y='Prezzo (€)',
    tooltip=['Data', 'Prezzo (€)']
).properties(width=700, height=300)
st.altair_chart(chart, use_container_width=True)

st.subheader("📅 Tabella completa")
st.dataframe(df, use_container_width=True, height=500)

st.markdown("---")
st.caption("Creato con ❤️ con Streamlit – Ultimo aggiornamento: luglio 2025")
