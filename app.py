
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Prezzi base
BASE_PREZZO = 135
VARIAZIONI = {
    'Monday': 0,
    'Tuesday': 0,
    'Wednesday': 0,
    'Thursday': 0,
    'Friday': 10,
    'Saturday': 20,
    'Sunday': 15,
}
FESTIVITA_EXTRA = 0.15  # +15%

st.set_page_config(page_title="Affitto Smart – Pietra Ligure", layout="centered")
st.title("🏡 Affitto Smart – Pietra Ligure")
st.write("Calcola il prezzo per notte del tuo appartamento nel centro storico di Pietra Ligure (agosto 2025).")

# Data di riferimento
data = st.date_input("📅 Scegli una data", min_value=datetime(2025, 8, 1), max_value=datetime(2025, 8, 31))
festivita = st.checkbox("📌 È una festività o ponte?", value=False)

# Calcolo prezzo
giorno_settimana = data.strftime('%A')
variazione = VARIAZIONI.get(giorno_settimana, 0)
prezzo = BASE_PREZZO + variazione
if festivita:
    prezzo += prezzo * FESTIVITA_EXTRA

st.markdown(f"**🗓️ Giorno:** {giorno_settimana}")
st.markdown(f"**💶 Prezzo suggerito:** {round(prezzo)} €")

st.divider()

# Tabella intero mese
st.subheader("📆 Tabella prezzi – Agosto 2025")

date_range = pd.date_range(start="2025-08-01", end="2025-08-31")
tabella = []
for d in date_range:
    giorno = d.strftime('%A')
    base = BASE_PREZZO + VARIAZIONI.get(giorno, 0)
    tabella.append({
        'Data': d.strftime('%d/%m/%Y'),
        'Giorno': giorno,
        'Prezzo base': BASE_PREZZO,
        'Variazione': VARIAZIONI.get(giorno, 0),
        'Prezzo finale': round(base),
    })

df = pd.DataFrame(tabella)
st.dataframe(df, use_container_width=True)

st.caption("Creato con ❤️ per ottimizzare gli affitti brevi a Pietra Ligure.")
