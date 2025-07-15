
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
import altair as alt

# ---------------------- CONFIG ----------------------
VARIAZIONI = {
    'Lunedì': 0,
    'Martedì': 0,
    'Mercoledì': 0,
    'Giovedì': 5,
    'Venerdì': 10,
    'Sabato': 20,
    'Domenica': 15,
}

STAGIONALITÀ = {
    1: 85,  2: 85,  3: 95,
    4: 100, 5: 110,
    6: 120, 7: 135,
    8: 150, 9: 120,
    10: 100, 11: 90,
    12: 100
}

GIORNI_IT = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
MESI_IT = [
    'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
    'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
]

# ---------------------- PAGINE ----------------------
st.set_page_config(page_title="Affitto Smart – Pietra Ligure", layout="centered")
pagina = st.sidebar.radio("📋 Naviga", ["📆 Calcolo Prezzi", "🗓️ Prenotazioni"])

if pagina == "📆 Calcolo Prezzi":
    st.title("📆 Calcolo prezzi affitto – Pietra Ligure")

    col1, col2 = st.columns(2)
    with col1:
        anno = st.selectbox("Anno", [2025, 2026], index=0)
    with col2:
        mese_nome = st.selectbox("Mese", MESI_IT, index=7)
        mese = MESI_IT.index(mese_nome) + 1

    prezzo_base = STAGIONALITÀ[mese]

    # Selezione intervallo date
    st.subheader("📅 Seleziona un soggiorno")
    data_inizio = st.date_input("Check-in", datetime(2025, mese, 1))
    data_fine = st.date_input("Check-out", datetime(2025, mese, 3))

    if data_fine <= data_inizio:
        st.warning("⚠️ Il check-out deve essere dopo il check-in.")
    else:
        giorni_soggiorno = pd.date_range(start=data_inizio, end=data_fine - timedelta(days=1))
        tabella = []

        for d in giorni_soggiorno:
            giorno_sett = GIORNI_IT[d.weekday()]
            extra = VARIAZIONI.get(giorno_sett, 0)
            prezzo = prezzo_base + extra
            guadagno = prezzo * 0.75
            tabella.append({
                "Data": d.strftime('%d/%m/%Y'),
                "Giorno": giorno_sett,
                "Prezzo Lordo (€)": prezzo,
                "Guadagno Netto (–25%)": round(guadagno)
            })

        df = pd.DataFrame(tabella)
        totale = df["Prezzo Lordo (€)"].sum()
        netto = df["Guadagno Netto (–25%)"].sum()

        st.subheader("💶 Tabella soggiorno")
        st.dataframe(df, use_container_width=True)

        st.markdown(f"**Totale soggiorno:** {round(totale)} €")
        st.markdown(f"**Guadagno netto (dopo commissioni):** {round(netto)} €")

    # Tabella mensile
    st.subheader("📊 Prezzi di tutto il mese")
    giorni_mese = calendar.monthrange(anno, mese)[1]
    date_range = pd.date_range(start=f"{anno}-{mese:02d}-01", end=f"{anno}-{mese:02d}-{giorni_mese}")
    tabella_mese = []
    for d in date_range:
        giorno = GIORNI_IT[d.weekday()]
        base = STAGIONALITÀ[mese]
        extra = VARIAZIONI.get(giorno, 0)
        lordo = base + extra
        netto = lordo * 0.75
        tabella_mese.append({
            "Data": d.strftime('%d/%m/%Y'),
            "Giorno": giorno,
            "Prezzo Lordo (€)": lordo,
            "Guadagno Netto (€)": round(netto)
        })
    df_mese = pd.DataFrame(tabella_mese)
    st.dataframe(df_mese, use_container_width=True)

elif pagina == "🗓️ Prenotazioni":
    st.title("🗓️ Calendario Prenotazioni")
    st.write("Segna le date già prenotate (verranno evidenziate).")

    mese_sel = st.selectbox("Scegli il mese", MESI_IT, index=7)
    mese_idx = MESI_IT.index(mese_sel) + 1
    giorni_mese = calendar.monthrange(2025, mese_idx)[1]
    date_range = pd.date_range(f"2025-{mese_idx:02d}-01", f"2025-{mese_idx:02d}-{giorni_mese}")

    # Selezione manuale delle date prenotate
    date_prenotate = st.multiselect("Seleziona le date già prenotate", [d.strftime('%d/%m/%Y') for d in date_range])

    st.subheader("📅 Calendario prenotazioni")
    df = pd.DataFrame({
        "Data": [d.strftime('%d/%m/%Y') for d in date_range],
        "Stato": ['🔴 Prenotata' if d.strftime('%d/%m/%Y') in date_prenotate else '🟢 Libera' for d in date_range]
    })

    st.dataframe(df, use_container_width=True, height=500)

st.markdown("---")
st.caption("Creato per la gestione affitti a Pietra Ligure • Ult. versione luglio 2025")
