@echo off
REM Starte Mistral-Server im Hintergrund (z. B. mit Ollama)
start "" /B ollama run mistral

REM Kurze Pause, um sicherzustellen, dass der Mistral-Server startet
timeout /t 5 > nul

REM Starte Streamlit-App
python -m streamlit run app.py

pause