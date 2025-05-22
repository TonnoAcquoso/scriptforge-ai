# ---------------------------------------------------------
# PER AVVIARE QUESTA APP, USA SEMPRE QUESTO COMANDO:
#    cd ~/Desktop
#    cd scriptforge_app
#    python -m streamlit run app.py
# ---------------------------------------------------------

import time # type: ignore
import requests # type: ignore
import streamlit as st # type: ignore
import openai  # type: ignore
from openai import OpenAI  # type: ignore
from PIL import Image # type: ignore
import base64
from io import BytesIO
import os
import shutil

# Sposta il file nella posizione che Streamlit si aspetta
if os.path.exists("secrets.toml"):
    os.makedirs(".streamlit", exist_ok=True)
    shutil.copy("secrets.toml", ".streamlit/secrets.toml")

def rileva_tema():
    # Controllo hack basato sul colore di sfondo attuale
    bg = st.get_option("theme.backgroundColor")
    if bg is None or bg.lower() in ["#0e1117", "#000000", "#1e1e1e"]:
        return "dark"
    else:
        return "light"

# === CONFIG ===
st.set_page_config(page_title="ScriptForge AI", layout="centered")

st.markdown("""
<style>
/* Tema variabili */
html[data-theme='dark'] {
    --bg-color: #0e0e11;
    --text-color: #ffffff;
}
html[data-theme='light'] {
    --bg-color: #ffffff;
    --text-color: #111111;
}

/* Applica i colori dinamici */
body {
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Pulsante toggle */
.theme-toggle {
    position: absolute;
    top: 16px;
    right: 65px;
    width: 36px;
    height: 36px;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 9999;
}

.theme-toggle svg {
    width: 26px;
    height: 26px;
    fill: var(--text-color);
}
</style>

<button class="theme-toggle" onclick="toggleTheme()">
    <svg viewBox="0 0 24 24">
        <g id="theme-icon">
            <!-- Default: luna -->
            <path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 1 0 9.79 9.79z"/>
        </g>
    </svg>
</button>

<script>
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    html.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    updateIcon(next);
}

function updateIcon(theme) {
    const icon = document.getElementById("theme-icon");
    if (theme === "light") {
        icon.innerHTML = `<path d="M12 4.5V3m6.364 2.136l1.06-1.06M19.5 12h1.5M18.364 18.364l1.06 1.06M12 19.5V21m-6.364-2.136-1.06 1.06M4.5 12H3m1.636-6.364-1.06-1.06M12 6a6 6 0 1 0 0 12a6 6 0 0 0 0-12z"/>`;
    } else {
        icon.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 1 0 9.79 9.79z"/>`;
    }
}

// Applica il tema salvato all’avvio
window.onload = () => {
    const saved = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", saved);
    updateIcon(saved);
}
</script>
""", unsafe_allow_html=True)


# === SWITCH TEMA ===
st.markdown("<h6 style='text-align: center;'>Tema interfaccia</h6>", unsafe_allow_html=True)
theme = st.selectbox("Scegli il tema", ["Dark", "Light"], index=0)

if theme == "Dark":
    st.markdown(
        '''
        <style>
        :root {
            --bg-color: #0e0e11;
            --text-color: #ffffff;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '''
        <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #111111;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )


# === SESSION STATE INIT ===
if "script" not in st.session_state:
    st.session_state["script"] = ""
if "mostra_guida" not in st.session_state:
    st.session_state["mostra_guida"] = False

# === SFONDO ===
#try:
#    response = requests.get(bg_url)
#    bg_image = Image.open(BytesIO(response.content))
#except Exception:
#    from PIL import ImageDraw # type: ignore
#    st.warning("⚠️ Impossibile caricare l’immagine di sfondo online. Verrà utilizzato uno sfondo nero di default.")
#    bg_image = Image.new("RGB", (1920, 1080), color="black") 
    
# bg_image = Image.open("bg.jpg") Se vuoi lanciarlo in locale #
#buffered_bg = BytesIO()
#bg_image.save(buffered_bg, format="jpeg")
#bg_base64 = base64.b64encode(buffered_bg.getvalue()).decode() 

# === LOGO ===
#logo_base64 = ""

# === CSS DEFINITIVO ===
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">

    <style>
    :root {{
        --bg-color: #0e0e11;
        --text-color: #ffffff;
    }}
    
    html[data-theme='dark'] {{
        --bg-color: #0e0e11;
        --text-color: #ffffff;
    }}
    html[data-theme='light'] {{
        --bg-color: #ffffff;
        --text-color: #111111;
    }}
    
    body, html, .main {{
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }}
    
    /* Container principale */
    .block-container {{
        background: linear-gradient(135deg, #0e0e11, #1c1c1c);
        background-color: var(--bg-color);
        padding: 2rem;
        border-radius: 12px;
        max-width: 700px;
        margin: auto;
    }}
    
    /* Titoli */
    .header-title, .section-title {{
        color: var(--text-color);
        font-family: 'Montserrat', sans-serif;
    }}
    
    .header-title {{
        font-size: clamp(20px, 5vw, 28px);
        font-weight: bold;
        line-height: 1.2;
        text-align: left;
        transition: color 0.3s ease;
    }}
    
    .section-title {{
        font-weight: bold;
        font-size: clamp(16px, 4vw, 20px);
        margin-top: 1.5rem;
        text-align: center;
    }}
    
    /* Etichette input */
    label, .stSelectbox label, .stTextInput label {{
        color: var(--text-color);
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(14px, 3.5vw, 16px);
        font-weight: 600;
    }}
    
    /* Input e Selectbox */
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.05);
        border: 1px solid #555;
        border-radius: 8px;
        color: var(--text-color);
        transition: background-color 0.3s ease;
    }}
    
    /* Pulsanti */
    .stButton button {{
        background-color: #333;
        color: var(--text-color);
        border-radius: 8px;
        border: 1px solid #666;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s ease, color 0.3s ease;
        cursor: pointer;
    }}
    .stButton button:hover {{
        background-color: #555;
    }}
    
    /* Pulsante Tema (già incluso sopra) */
    .theme-toggle {{
        position: absolute;
        top: 16px;
        right: 65px;
        width: 36px;
        height: 36px;
        background: transparent;
        border: none;
        cursor: pointer;
        z-index: 9999;
    }}
    .theme-toggle svg {{
        width: 26px;
        height: 26px;
        fill: var(--text-color);
    }}
    
    
    .header-logo {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0;
        margin-right: 10px;
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

    /* Effetto fade-in */
    .fade-in {{
        animation: fadeIn 0.5s ease-in-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    /* Riga con icona guida */
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
    
    button[title="Clicca per aprire la guida sull'intensità"] {{
                display: block;
                margin: 0 auto;
            }}
    
    </style>
    """,
    unsafe_allow_html=True
)

tema_corrente = rileva_tema()
colore_titolo = "white" if tema_corrente == "dark" else "black"

# === TITOLO ===
col1, col2 = st.columns([1, 8])

with col1:
    st.image("https://i.imgur.com/GouOmJ6.png", width=50)

with col2:
    st.markdown(
        """
        <div style='display: flex; align-items: center; height: 100%;'>
            <h2 style='margin: 0; font-family: Montserrat, sans-serif;'>ScriptForge AI – Generatore Script Narrativi</h2>
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
intensita = st.selectbox("Seleziona l’intensità emotiva", intensità, index=0)

 # Pulsante ? centrato sotto il campo
if st.button("?", key="help", help="Clicca per aprire la guida sull'intensità"):
    st.session_state["mostra_guida"] = not st.session_state.get("mostra_guida", False)
        
        
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

        import time
        with st.spinner("Generazione in corso..."):
            progress_bar = st.progress(0)
            for i in range(5):
                time.sleep(0.2)
                progress_bar.progress((i + 1) * 20)

            script = genera_script_con_gpt(prompt)
            progress_bar.empty()

        st.session_state["script"] = script

        if script:
            st.success("✅ Script generato con successo!")
            st.text_area("Risultato finale:", script, height=600)
        else:
            st.error("❌ Nessuna risposta ricevuta da OpenAI.")
    else:
        st.warning("⚠️ Completa tutti i campi prima di generare lo script.")

                
# Bottone custom "?" intercettato
import streamlit.components.v1 as components # type: ignore
components.html("""
<script>
    const handler = () => {
        const streamlitEvent = new CustomEvent("streamlit:buttonClicked", { detail: { key: "help" } });
        window.dispatchEvent(streamlitEvent);
    };
    window.addEventListener("streamlit:buttonClicked_help", handler);
</script>
""", height=0)

# === SEZIONE DOWNLOAD FORMATO ===

if st.session_state["script"]:
    st.markdown("---")
    st.markdown("**Scarica lo script:**")
    file_name = st.text_input("Nome file da salvare (senza estensione)", "script")
    formato = st.radio("Seleziona il formato di download", ["TXT", "DOCX"], horizontal=True)

    if formato == "TXT":
        st.download_button(
            label="⬇️ Scarica .txt",
            data=st.session_state["script"],
            file_name=f"{file_name}.txt",
            mime="text/plain"
        )
    else:
        from docx import Document # type: ignore
        doc = Document()
        for line in st.session_state["script"].split("\n"):
            doc.add_paragraph(line)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="⬇️ Scarica .docx",
            data=buffer,
            file_name=f"{file_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
