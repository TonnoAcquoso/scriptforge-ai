# ---------------------------------------------------------
# PER AVVIARE QUESTA APP, USA SEMPRE QUESTO COMANDO:
#    cd ~/Desktop
#    cd scriptforge_app
#    python -m streamlit run app.py
# ---------------------------------------------------------

# bg_url = "https://i.imgur.com/ujQBvFG.jpeg"
# import requests # type: ignore
import streamlit as st # type: ignore
import openai  # type: ignore
from openai import OpenAI  # type: ignore
from PIL import Image # type: ignore
import base64
from io import BytesIO


# === CONFIG ===
st.set_page_config(page_title="ScriptForge AI", layout="centered")

# === SFONDO ===
# response = requests.get(bg_url)
# bg_image = Image.open(BytesIO(response.content))
# bg_image = Image.open("bg.jpg") Se vuoi lanciarlo in locale
# buffered_bg = BytesIO()
# bg_image.save(buffered_bg, format="JPEG")
# bg_base64 = base64.b64encode(buffered_bg.getvalue()).decode() 

# === LOGO ===
logo_image = Image.open("banner_martello.jpg")
buffered_logo = BytesIO()
logo_image.save(buffered_logo, format="JPEG")
logo_base64 = base64.b64encode(buffered_logo.getvalue()).decode()

# === CSS DEFINITIVO ===
st.markdown(
    f"""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">

    <style>
    html, body, .main {{
        height: 100%;
        margin: 0;
        padding: 0;
        background: url("https://i.imgur.com/ujQBvFG.jpeg") no-repeat center center fixed;
        background-size: cover;
    }}

    .block-container {{
        background-color: rgba(0, 0, 0, 0.3);
        padding: 2rem;
        border-radius: 12px;
        max-width: 700px;
        margin: auto;
    }}

    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 20px;
        text-align: center;
    }}

    .header-logo {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #888;
        flex-shrink: 0;
    }}

    .header-title {{
        font-size: clamp(20px, 5vw, 28px);
        font-weight: bold;
        color: white;
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        line-height: 1.2;
    }}

    .section-title {{
        font-weight: bold;
        font-size: clamp(16px, 4vw, 20px);
        margin-top: 1.5rem;
        color: white;
        font-family: 'Montserrat', sans-serif;
        text-align: center;
    }}

    label, .stSelectbox label, .stTextInput label {{
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(14px, 3.5vw, 16px);
        font-weight: 600;
    }}

    .stButton button {{
        display: block;
        margin: 0 auto;
    }}

    /* Forza la manina su tutti gli elementi cliccabili */
    .stSelectbox div[data-baseweb="select"] *,
    .stSelectbox div[data-baseweb="select"] {{
        cursor: pointer !important;
    }}

    input:focus, textarea:focus {{
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    div[data-baseweb="select"] > div {{
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    div[data-baseweb="select"] > div:focus-within {{
        border: 2px solid white !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    div[data-baseweb="select"]:focus-within {{
        box-shadow: none !important;
    }}

    div[data-baseweb="input"] {{
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border: 2px solid white !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    div[data-baseweb="select"] > div > div:first-child {{
        color: #999 !important;
        opacity: 0.6 !important;
        font-style: italic !important;
    }}
    .fade-in {{
    animation: fadeIn 0.5s ease-in-out;
    }}
        @keyframes fadeIn {{
            from { opacity: 0; }
            to { opacity: 1; }
        }}

        .intensity-row {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

        .help-icon {{
    background-color: #555;
    color: white;
    border-radius: 50%;
    padding: 3px 9px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-family: 'Montserrat', sans-serif;
    }}

    .help-icon:hover {{
    background-color: #777;
    }}

    </style>
    """,
    unsafe_allow_html=True
)




# === HEADER ===
st.markdown(
    f"""
    <div class="header-container">
        <img src="data:image/jpeg;base64,{logo_base64}" class="header-logo">
        <div class="header-title">ScriptForge AI – Generatore Script Narrativi</div>
    </div>
    """,
    unsafe_allow_html=True
)

# === PARAMETRI ===
st.markdown("<div class='section-title'>Imposta i parametri</div>", unsafe_allow_html=True)

nicchie = [
    "Scegli opzione", "Anime", "Podcast", "Educazione", "Brand", "Biografie",
    "Storia Personale", "Startup / Business", "Motivazionale",
    "Tecnologia", "Crime / Mistero", "Fantasy", "Sci-Fi",
    "Educazione Finanziaria", "Salute e Benessere"
]
stili = ["Scegli opzione", "Epico", "Lirico", "Psicologico", "Ironico", "Analitico"]
intensità = ["Scegli opzione", "Alta", "Media", "Bassa"]
tema = st.text_input("Inserisci Argomento")

nicchia = st.selectbox("Seleziona la nicchia", nicchie, index=0)
stile = st.selectbox("Seleziona lo stile narrativo", stili, index=0)
col1, col2 = st.columns([6, 1])
with col1:
    intensita = st.selectbox("Seleziona l’intensità emotiva", intensità, index=0)
with col2:
    if st.button("?", key="help", help="Clicca per aprire la guida sull'intensità", use_container_width=True):
        st.session_state["mostra_guida"] = True
        
        
# Mostra guida se attiva
if "mostra_guida" not in st.session_state:
    st.session_state["mostra_guida"] = False

if st.session_state["mostra_guida"]:
    st.markdown("---")
    st.markdown("<div class='section-title'>Guida ai parametri</div>", unsafe_allow_html=True)

    guide_titles = ["Intensità Emotiva", "Stile Narrativo", "Scelta della Nicchia"]
    guida_selezionata = st.radio("Seleziona la guida:", guide_titles, horizontal=True)

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    if guida_selezionata == "Intensità Emotiva":
        st.markdown("""
### Guida all’intensità emotiva:

L’intensità emotiva definisce la forza con cui lo script coinvolge lo spettatore a livello emotivo.

**Alta:**
- Lo script punta a suscitare emozioni forti: adrenalina, commozione, stupore.
- Adatto a finali epici, trasformazioni potenti o momenti chiave dell’anime.
- Tono: drammatico, ispirazionale, cinematografico.

**Media:**
- Bilancia emozione e riflessione.
- Ideale per spiegare un personaggio, una scelta narrativa o un evento significativo.
- Tono: empatico, profondo ma accessibile.

**Bassa:**
- Tono più distaccato, descrittivo o analitico.
- Perfetta per contenuti educativi, recensioni, o osservazioni oggettive.
- Tono: calmo, professionale, razionale.

*Scegli in base all’effetto che vuoi ottenere.*
""")
    elif guida_selezionata == "Stile Narrativo":
        st.markdown("""
### Guida allo stile narrativo:

**Epico:** narrazione eroica, ritmo serrato, finale potente.  
**Lirico:** tono poetico, descrizioni evocative.  
**Psicologico:** introspezione, conflitti interiori.  
**Ironico:** tono leggero, critico, sarcastico.  
**Analitico:** stile oggettivo, basato su logica e struttura.
""")
    elif guida_selezionata == "Scelta della Nicchia":
        st.markdown("""
### Guida alla scelta della nicchia:

**Anime:** per analisi narrative, personaggi e momenti iconici.  
**Podcast:** per contenuti ascoltabili, chiari e ritmici.  
**Educazione:** per spiegazioni, storytelling didattico.  
**Brand:** per raccontare visioni aziendali in modo creativo.  
**Biografie:** per narrare vite in modo coinvolgente.
""")

    st.markdown('</div>', unsafe_allow_html=True)

# === PROMPT ===
def genera_prompt_script_lungo(nicchia, stile, intensita, tema):
    return f"""Crea uno script lungo (1200–1500 parole) in stile narrativo riflessivo ed epico, basato su questo personaggio/anime/tema: “{tema}”

Lo script deve essere creato sulla base delle scelte dell’utente e sarà quindi:
– Scorrevole e coinvolgente, con uno stile da documentario emotivo o storytelling YouTube
– Strutturato in forma narrativa fluida (no scalette), con transizioni psicologiche forti (es. “ed è qui che tutto cambia”)
– Capace di evolversi nel tono (es. da riflessivo a epico)
– Perfettamente adatto alla registrazione audio

Includi obbligatoriamente:
– 1200/1500 parole di script e della durata di 10 minuti
– Voice-over integrato (tra parentesi: tono, ritmo, pause)
– Scene con timestamp verificati (episodio + minuto esatto, fonti affidabili)
– Approfondimenti culturali, psicologici o simbolici
– Montaggio suggerito: evidenzia i momenti visivi più forti o emotivi
– Call to action narrativa *inserita nell’ultima frase*, senza chiusura esplicita

Se possibile, aggiungi anche:
– Titolo YouTube ottimizzato per CTR e curiosità
– Descrizione SEO con parole chiave e hashtag

Una volta completato tutto, riscrivi lo script sotto forma di **testo esteso in stile parlato**, contenente tutto lo script in forma fluida e naturale, come se fosse già pronto per essere registrato dal voice-over, senza sintesi o riassunti.

Queste sono le preferenze dell’utente:
– Nicchia: {nicchia}
– Stile narrativo scelto: {stile}
– Intensità emotiva: {intensita}
"""


# === CONFIG GPT ASSISTANT ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = "asst_k8nUpECUsPnjCgPOfNdrs9el"

def genera_script_con_gpt(prompt):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

# === GENERA ===
if st.button("⚙️ Genera Prompt"):
    if tema and nicchia != "Scegli opzione" and stile != "Scegli opzione" and intensita != "Scegli opzione":
        prompt = genera_prompt_script_lungo(nicchia, stile, intensita, tema)
        script = genera_script_con_gpt(prompt)
        st.session_state["script"] = script

        if script:
            st.success("✅ Script generato con successo!")
            st.text_area("Risultato finale:", st.session_state["script"], height=600)
        else:
            st.error("❌ Nessuna risposta ricevuta da OpenAI.")
    else:
        st.warning("⚠️ Completa tutti i campi prima di generare lo script.")

# === SEZIONE DOWNLOAD FORMATO ===
if st.session_state["script"]:
    st.markdown("---")
    st.markdown("**Scarica lo script:**")

    formato = st.radio("Seleziona il formato di download", ["TXT", "DOCX"], horizontal=True)

    if formato == "TXT":
        st.download_button(
            label="⬇️ Scarica .txt",
            data=st.session_state["script"],
            file_name="script.txt",
            mime="text/plain"
        )
    else:
        from docx import Document
        doc = Document()
        for line in st.session_state["script"].split("\n"):
            doc.add_paragraph(line)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="⬇️ Scarica .docx",
            data=buffer,
            file_name="script.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
