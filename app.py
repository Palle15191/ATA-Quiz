import streamlit as st
import json
import random

st.set_page_config("📘 PDF-Quiz", layout="wide")
st.title("🧠 Dein KI-Quiz aus E-Book")

# Lade Fragen aus JSON-Datei
with open("data/300_Fragen_Deepseek.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Auswahl der Fragenanzahl vor dem Quizstart
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if not st.session_state.quiz_started:
    st.subheader("🔢 Wie viele Fragen möchtest du beantworten?")
    fragen_anzahl = st.radio("Anzahl der Fragen", [10, 20, 30], index=0)
    if st.button("🎬 Quiz starten"):
        st.session_state.quiz_started = True
        st.session_state.fragen = random.sample(all_questions, fragen_anzahl)
        st.session_state.index = 0
        st.session_state.antworten = []
        st.session_state.zeige_feedback = False
        st.rerun()

# Quiz läuft
else:
    total = len(st.session_state.fragen)

    if st.session_state.index < total:
        frage_block = st.session_state.fragen[st.session_state.index]
        frage = frage_block["frage"]
        antworten = frage_block["antworten"]
        richtige = frage_block["richtige_antwort"]
        begruendung = frage_block["begründung"]

        st.subheader(f"Frage {st.session_state.index + 1} von {total}")
        st.markdown(frage)

        # Falls Feedback noch nicht angezeigt wurde, Antwortmöglichkeiten anzeigen
        if not st.session_state.get("zeige_feedback", False):
            for key, value in antworten.items():
                if st.button(f"{key}) {value}", key=key):
                    ist_korrekt = key == richtige
                    st.session_state.antworten.append({
                        "frage": frage,
                        "gewaehlt": key,
                        "korrekt": richtige,
                        "begründung": begruendung,
                        "ist_korrekt": ist_korrekt
                    })
                    st.session_state.zeige_feedback = True
                    st.rerun()
        else:
            last = st.session_state.antworten[-1]
            korrekt = "✅ Richtig!" if last["ist_korrekt"] else "❌ Leider falsch."
            st.markdown(f"**{korrekt}**")
            st.markdown(f"- Richtige Antwort: **{richtige}**")
            st.markdown(f"- Begründung: {begruendung}")

            if st.button("➡️ Nächste Frage"):
                st.session_state.index += 1
                st.session_state.zeige_feedback = False
                st.rerun()

    # Quiz abgeschlossen
    else:
        st.success("🎉 Quiz beendet!")

        punkte = sum(1 for res in st.session_state.antworten if res["ist_korrekt"])
        st.markdown(f"**Dein Ergebnis:** {punkte} von {total} Punkten")

        for i, res in enumerate(st.session_state.antworten):
            korrekt = "✅" if res["ist_korrekt"] else "❌"
            st.markdown(f"**Frage {i + 1}:** {res['frage']}")
            st.markdown(f"- Deine Antwort: {res['gewaehlt']} {korrekt}")
            st.markdown(f"- Richtige Antwort: {res['korrekt']}")
            st.markdown(f"- Begründung: {res['begründung']}")
            st.markdown("---")

        if st.button("🔁 Neues Quiz starten"):
            for key in ["quiz_started", "fragen", "antworten", "index", "zeige_feedback"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()