import json
import os
import time
import requests

# ==== Lokales Sprachmodell verwenden (z. B. Ollama) ====
def run_local_llm(prompt, model="mistral"):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"❌ Fehler vom Modell: {response.text}"

# ==== Fragen aus Text generieren ====
def generate_questions_from_text(text, max_questions=500, chunk_size=2000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    questions = []

    for i, chunk in enumerate(chunks):
        if len(questions) >= max_questions:
            break

        prompt = f"""
Erstelle bitte jeweils 5 Multiple-Choice-Fragen zum folgenden Textausschnitt.
Jede Frage soll 4 Antwortmöglichkeiten (A–D) enthalten, eine richtige Lösung und eine kurze Begründung.

Gib bitte folgendes Format für **jede Frage einzeln** zurück:

Frage: ...
A) ...
B) ...
C) ...
D) ...
Richtige Antwort: ...
Begründung: ...

Text:
\"\"\"{chunk}\"\"\"
"""

        print(f"📚 Generiere Fragen für Abschnitt {i+1}...")
        try:
            response = run_local_llm(prompt)
            # Versuche jede einzelne Frage zu extrahieren
            parsed_questions = response.strip().split("Frage:")
            for raw_q in parsed_questions[1:]:
                q = "Frage:" + raw_q.strip()
                if q.count("A)") == 1 and "Richtige Antwort:" in q and "Begründung:" in q:
                    questions.append(q.strip())
                if len(questions) >= max_questions:
                    break
        except Exception as e:
            print(f"⚠️ Fehler bei Abschnitt {i+1}: {e}")

        time.sleep(1)  # kleine Pause, um Modell nicht zu überfordern

    return questions

# ==== Hauptfunktion ====
if __name__ == "__main__":
    input_path = "data/extracted_text.json"
    output_path = "data/quiz_fragen.json"

    if not os.path.exists(input_path):
        print("❌ PDF-Daten wurden noch nicht extrahiert. Bitte zuerst pdf_reader.py ausführen.")
        exit()

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        full_text = data["text"]

    print("🧠 Starte Fragegenerierung...")
    questions = generate_questions_from_text(full_text, max_questions=500)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(questions)} Fragen wurden gespeichert unter: {output_path}")