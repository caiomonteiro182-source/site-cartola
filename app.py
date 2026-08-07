import streamlit as st
import pandas as pd
import requests

# 1. Configuração da Página
st.set_page_config(
    page_title="Campeonato Brasileiro - Série A",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização Cyberpunk Neon
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Rajdhani:wght@600;700&display=swap');

    /* Fundo Geral Escuro / Cyberpunk */
    .stApp {
        background: radial-gradient(circle at top center, #1e0b36 0%, #0a0813 60%, #030206 100%);
        color: #f1f5f9;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Cabeçalhos Neon */
    h1 {
        font-family: 'Teko', sans-serif !important;
        font-size: 52px !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2ff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0px !important;
    }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.4);
        font-weight: 700;
    }

    /* LETREIRO (MARQUEE) NEON */
    .ticker-container {
        width: 100%;
        background: rgba(10, 8, 19, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        overflow: hidden;
        white-space: nowrap;
        padding: 10px 0;
        margin-bottom: 20px;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 28s linear infinite;
        font-family: 'Rajdhani', sans-serif;
        font-size: 19px;
        font-weight: 700;
        color: #00f2ff;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* Card de Partida Neon */
    .match-card {
        background: rgba(18, 12, 38, 0.8);
        border: 1px solid #a855f7;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.25);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .match-card:hover {
        transform: translateY(-2px);
        border-color: #00f2ff;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
    }

    .score-badge {
        font-family: 'Teko', sans-serif;
        font-size: 32px;
        color: #00f2ff;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
        padding: 0 10px;
    }

    .team-name {
        font-size: 18px;
        font-weight: 700;
        color: #f1f5f9;
    }

    .match-info {
        font-size: 13px;
        color: #c084fc;
        margin-top: 6px;
    }

    hr {
        border-color: rgba(0, 242, 255, 0.3) !important;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# 3. Funções para Busca de Dados Reais do Brasileirão
@st.cache_data(ttl=120)
def obter_rodada_atual():
    try:
        res = requests.get("https://api.cartola.globo.com/mercado/status", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            dados = res.json()
            return dados.get("rodada_atual", 1), dados.get("status_mercado", 1)
    except:
        pass
    return 1, 1

@st.cache_data(ttl=120)
def carregar_partidas_rodada(num_rodada):
    url = f"https://api.cartola.globo.com/partidas/{num_rodada}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            data = res.json()
            partidas = data.get("partidas", [])
            clubes = data.get("clubes", {})
            return partidas, clubes
    except:
        pass
    return [], {}

# --- 4. CARREGAMENTO DOS DADOS ---
rodada_real, status_m = obter_rodada_atual()

# Seletor de Rodada no Cabeçalho
col_tit, col_sel, col_btn = st.columns([3, 1, 1])
with col_tit:
    st.title("BRASILEIRÃO SÉRLE A")
    st.markdown("<h4 style='color: #c084fc; margin-top: -10px;'>ACOMPANHAMENTO DE JOGOS E PLACARES EM TEMPO REAL</h4>", unsafe_allow_html=True)

with col_sel:
    rodada_selecionada = st.selectbox("Escolha a Rodada:", list(range(1, 39)), index=max(0, rodada_real - 1))

with col_btn:
    st.write("")
    if st.button("🔄 Atualizar Jogos"):
        st.cache_data.clear()
        st.rerun()

partidas, clubes = carregar_partidas_rodada(rodada_selecionada)

# --- 5. MONTAR TEXTO DO LETREIRO (TICKER) ---
itens_letreiro = []
if partidas and clubes:
    for p in partidas:
        id_m = str(p.get("clube_casa_id"))
        id_v = str(p.get("clube_visitante_id"))
        
        nome_m = clubes.get(id_m, {}).get("nome", "Casa").upper()
        nome_v = clubes.get(id_v, {}).get("nome", "Visitante").upper()
        
        placar_m = p.get("placar_oficial_mandante")
        placar_v = p.get("placar_oficial_visitante")
        
        if placar_m is not None and placar_v is not None:
            itens_letreiro.append(f"{nome_m} {placar_m} x {placar_v} {nome_v}")
        else:
            itens_letreiro.append(f"{nome_m} x {nome_v} (A JOGAR)")

    texto_ticker = f"⚽ BRASILEIRÃO SÉRLE A • RODADA {rodada_selecionada} • " + " • ".join(itens_letreiro) + " • ⚽"
else:
    texto_ticker = f"⚽ BRASILEIRÃO SÉRLE A • RODADA {rodada_selecionada} • Carregando jogos e placares..."

# Exibição do Letreiro Neon
st.markdown(f"""
    <div class="ticker-container">
        <div class="ticker-text">{texto_ticker}</div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- 6. EXIBIÇÃO DAS PARTIDAS REALIZADAS NA RODADA ---
st.subheader(f"⚔️ Confrontos da {rodada_selecionada}ª Rodada")

if partidas and clubes:
    cols = st.columns(2)
    for i, p in enumerate(partidas):
        id_m = str(p.get("clube_casa_id"))
        id_v = str(p.get("clube_visitante_id"))
        
        clube_m = clubes.get(id_m, {})
        clube_v = clubes.get(id_v, {})
        
        nome_m = clube_m.get("nome", "Mandante")
        nome_v = clube_v.get("nome", "Visitante")
        
        escudo_m = clube_m.get("escudos", {}).get("60x60", "")
        escudo_v = clube_v.get("escudos", {}).get("60x60", "")
        
        placar_m = p.get("placar_oficial_mandante")
        placar_v = p.get("placar_oficial_visitante")
        
        placar_txt = f"{placar_m if placar_m is not None else ''} X {placar_v if placar_v is not None else ''}" if (placar_m is not None or placar_v is not None) else "VS"
        
        local = p.get("local", "Estádio não informado")
        data_jogo = p.get("partida_data", "")
        
        with cols[i % 2]:
            st.markdown(f"""
                <div class="match-card">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="flex: 1; text-align: center;">
                            <img src="{escudo_m}" width="45" style="vertical-align: middle;"><br>
                            <span class="team-name">{nome_m}</span>
                        </div>
                        <div class="score-badge">
                            {placar_txt}
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <img src="{escudo_v}" width="45" style="vertical-align: middle;"><br>
                            <span class="team-name">{nome_v}</span>
                        </div>
                    </div>
                    <div class="match-info">
                        📍 {local} &nbsp;|&nbsp; 🗓️ {data_jogo}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("⚠️ Não foi possível carregar as partidas desta rodada no momento.")

st.divider()
st.caption(f"⚡ Dados Oficiais do Campeonato Brasileiro • Rodada {rodada_selecionada} • Sincronizado via API Cartola/Globo.")
