import streamlit as st
import pandas as pd
import requests
import os
import base64
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS HYPER-CYBERPUNK
# ==========================================
st.set_page_config(
    page_title="Black Guys League - Cartola FC",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def carregar_logo_base64():
    for ext in ["logo.png", "logo.jpg", "logo.jpeg"]:
        if os.path.exists(ext):
            with open(ext, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
    return ""

URL_BASE64_LOGO = carregar_logo_base64()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% -20%, #1a0933 0%, #080612 50%, #020105 100%);
        color: #f8fafc;
        font-family: 'Rajdhani', sans-serif;
    }

    .header-main-flex {
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 15px;
        background: rgba(15, 12, 29, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .header-logo-img {
        width: 140px;
        height: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.5));
    }

    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 48px !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2ff 0%, #7c3aed 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0px !important;
        line-height: 1.1 !important;
    }

    h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00f2ff !important;
        text-shadow: 0 0 12px rgba(0, 242, 255, 0.5);
        font-weight: 700;
        letter-spacing: 1px;
    }

    .header-title-container {
        display: flex;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap;
    }

    .market-timer-inline-open {
        background: linear-gradient(135deg, #a3e635 0%, #65a30d 100%);
        color: #020617;
        font-family: 'Orbitron', sans-serif;
        font-size: 15px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(163, 230, 53, 0.6);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .market-timer-inline-alert {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 15px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 30px;
        box-shadow: 0 0 18px rgba(249, 115, 22, 0.8);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .market-timer-inline-closed {
        background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%);
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 15px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.6);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .subtitle-header {
        color: #c084fc;
        font-weight: 700;
        margin-top: 6px;
        margin-bottom: 8px;
        font-size: 15px;
        letter-spacing: 1px;
    }

    .link-liga {
        display: inline-block;
        color: #00f2ff !important;
        font-weight: 700;
        font-size: 13px;
        text-decoration: none;
        letter-spacing: 1px;
        padding: 8px 16px;
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .link-liga:hover {
        background: rgba(0, 242, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }

    .matches-panel-container {
        width: 100%;
        background: rgba(10, 8, 22, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        padding: 14px 18px;
        margin-bottom: 22px;
    }

    .matches-panel-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: #00f2ff;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    .matches-grid {
        display: flex;
        gap: 12px;
        overflow-x: auto;
        padding-bottom: 10px;
    }

    .match-card {
        flex: 0 0 auto;
        background: rgba(21, 16, 43, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 12px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        min-width: 160px;
        transition: transform 0.2s ease;
    }
    .match-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 242, 255, 0.6);
    }

    .match-card img {
        width: 38px !important;
        height: 38px !important;
        object-fit: contain !important;
    }

    .match-score {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        font-weight: 900;
        color: #ffffff;
    }

    .box-m1 {
        background: rgba(13, 10, 28, 0.85);
        border-radius: 16px;
        padding: 18px;
        border-left: 6px solid #00f2ff;
        box-shadow: 0 4px 20px rgba(0, 242, 255, 0.15);
        margin-bottom: 12px;
    }

    .box-m2 {
        background: rgba(13, 10, 28, 0.85);
        border-radius: 16px;
        padding: 18px;
        border-left: 6px solid #10b981;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        margin-bottom: 12px;
    }

    .lbl-title {
        font-size: 13px;
        font-weight: bold;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .val-num {
        font-family: 'Orbitron', sans-serif;
        font-size: 44px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin-right: 10px;
    }

    .txt-up { color: #10b981 !important; font-size: 22px; font-weight: bold; }
    .txt-down { color: #f43f5e !important; font-size: 22px; font-weight: bold; }

    div[data-testid="stMetric"] {
        background: rgba(21, 16, 43, 0.7);
        border: 1px solid rgba(124, 58, 237, 0.4);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2);
        padding: 14px 18px;
        border-radius: 14px;
    }

    button[data-baseweb="tab"] {
        background-color: rgba(15, 12, 29, 0.5) !important;
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 18px !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(180deg, rgba(124, 58, 237, 0.3) 0%, rgba(0, 242, 255, 0.08) 100%) !important;
        color: #00f2ff !important;
        border-bottom: 3px solid #00f2ff !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(124, 58, 237, 0.4);
        border-radius: 14px;
        overflow: hidden;
    }

    .card-scout-player {
        background: rgba(13, 10, 28, 0.85);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    hr {
        border-color: rgba(0, 242, 255, 0.2) !important;
        margin: 18px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# ==========================================
# 2. SISTEMA DA BLACK GUYS LEAGUE
# ==========================================
def processar_dados_time(args):
    row, rodada_ultima_consolidada, rodada_penultima, status_mercado, atletas_ao_vivo = args
    session = requests.Session()
    session.headers.update(HEADERS)

    nome_time = str(row.get("Time", "")).strip()
    cartoleiro = str(row.get("Cartoleiro", "")).strip()
    time_id = row.get("ID", None)

    try:
        time_id = int(time_id) if pd.notna(time_id) else None
    except (ValueError, TypeError):
        time_id = None

    pt_rodada = 0.0
    pt_rodada_anterior = 0.0
    total_acumulado = 0.0
    patrimonio = 100.0
    valorizacao_rodada = 0.0

    if time_id:
        try:
            res_p = session.get(f"https://api.cartola.globo.com/time/id/{time_id}", timeout=3)
            if res_p.status_code == 200:
                patrimonio = float(res_p.json().get("patrimonio", 100.0))

            soma_historico_rodadas = 0.0
            for r in range(1, rodada_ultima_consolidada + 1):
                res_r = session.get(f"https://api.cartola.globo.com/time/id/{time_id}/{r}", timeout=3)
                if res_r.status_code == 200:
                    pts_r = float(res_r.json().get("pontos", 0.0))
                    soma_historico_rodadas += pts_r

                    if r == rodada_ultima_consolidada:
                        pt_rodada = pts_r
                        atletas_uc = res_r.json().get("atletas", [])
                        if atletas_uc and status_mercado == 1:
                            valorizacao_rodada = sum([float(a.get("variacao_num", 0.0)) for a in atletas_uc])

                    if r == rodada_penultima:
                        pt_rodada_anterior = pts_r

            total_acumulado = soma_historico_rodadas

            if status_mercado == 2 and atletas_ao_vivo and res_p.status_code == 200:
                dados = res_p.json()
                atletas_escalados = dados.get("atletas", [])
                capitao_id = dados.get("capitao_id", None)

                pontos_vivo = 0.0
                val_vivo = 0.0

                for atleta in atletas_escalados:
                    a_id = str(atleta.get("atleta_id"))
                    if a_id in atletas_ao_vivo:
                        info_v = atletas_ao_vivo[a_id]
                        p_atleta = float(info_v.get("pontuacao", 0.0))
                        v_atleta = float(info_v.get("variacao_num", 0.0))

                        if capitao_id and int(a_id) == int(capitao_id):
                            p_atleta *= 2

                        pontos_vivo += p_atleta
                        val_vivo += v_atleta

                pt_rodada = pontos_vivo
                valorizacao_rodada = val_vivo
                total_acumulado += pt_rodada

        except Exception:
            pass

    if total_acumulado == 0.0:
        try:
            total_acumulado = float(row.get("Total", 0.0))
        except Exception:
            total_acumulado = 0.0

    return {
        "Time": nome_time,
        "Cartoleiro": cartoleiro,
        "Pontos Ganhos (Última Rodada)": round(pt_rodada, 2),
        "Pontos Rodada Anterior": round(pt_rodada_anterior, 2),
        "Total Acumulado": round(total_acumulado, 2),
        "Patrimônio (C$)": round(patrimonio, 2),
        "Valorização (C$)": round(valorizacao_rodada, 2)
    }

@st.cache_data(ttl=120)
def carregar_dados_liga():
    session = requests.Session()
    session.headers.update(HEADERS)

    rodada_cartola = 20
    status_mercado = 1 
    info_fechamento = None

    try:
        res_m = session.get("https://api.cartola.globo.com/mercado/status", timeout=4)
        if res_m.status_code == 200:
            dados_m = res_m.json()
            rodada_cartola = dados_m.get("rodada_atual", 20)
            status_mercado = dados_m.get("status_mercado", 1)
            info_fechamento = dados_m.get("fechamento", {})
    except Exception:
        pass

    df_base = None
    for csv_file in ["base_cartola_oficial.csv", "base_cartola.csv"]:
        if os.path.exists(csv_file):
            try:
                df_base = pd.read_csv(csv_file, sep=None, engine='python', encoding='utf-8-sig')
                df_base.columns = df_base.columns.str.strip()
                break
            except Exception:
                pass

    if df_base is None:
        st.error("⚠️ O arquivo CSV de base ('base_cartola_oficial.csv') não foi encontrado!")
        return pd.DataFrame(), rodada_cartola, status_mercado, info_fechamento

    atletas_ao_vivo = {}
    if status_mercado == 2:
        try:
            res_av = session.get("https://api.cartola.globo.com/atleta/pontuados", timeout=4)
            if res_av.status_code == 200:
                atletas_ao_vivo = res_av.json().get("atletas", {})
        except Exception:
            pass

    rodada_ultima_consolidada = rodada_cartola - 1 if status_mercado == 1 else rodada_cartola
    rodada_penultima = rodada_ultima_consolidada - 1

    tasks = [(row, rodada_ultima_consolidada, rodada_penultima, status_mercado, atletas_ao_vivo) for _, row in df_base.iterrows()]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        lista_times = list(executor.map(processar_dados_time, tasks))

    df = pd.DataFrame(lista_times)
    
    if not df.empty:
        df = df.sort_values(by="Total Acumulado", ascending=False).reset_index(drop=True)
        df["Posição Geral"] = df.index + 1

        top_score = df.iloc[0]["Total Acumulado"]
        df["Dif. p/ Rival"] = (df["Total Acumulado"].shift(1) - df["Total Acumulado"]).round(2).fillna(0)
        df["Dif. p/ Líder"] = (top_score - df["Total Acumulado"]).round(2)

        max_mito = df["Pontos Ganhos (Última Rodada)"].max()
        max_patr = df["Patrimônio (C$)"].max()
        min_tot = df["Total Acumulado"].min()

        badges = []
        for _, r in df.iterrows():
            b_list = []
            if r["Posição Geral"] == 1:
                b_list.append("🥇 Líder")
            if r["Pontos Ganhos (Última Rodada)"] == max_mito and max_mito > 0:
                b_list.append("🚀 Mito")
            if r["Patrimônio (C$)"] == max_patr:
                b_list.append("💰 Rico")
            if r["Total Acumulado"] == min_tot and len(df) > 1:
                b_list.append("📉 Mala Cheia")
            badges.append(" ".join(b_list) if b_list else "—")
        
        df["Conquistas"] = badges

    return df, rodada_cartola, status_mercado, info_fechamento

def gerar_badge_mercado(info_fechamento, status_mercado):
    if status_mercado != 1 or not info_fechamento:
        return '<span class="market-timer-inline-closed">🔒 MERCADO FECHADO</span>'

    try:
        ano = info_fechamento.get("ano")
        mes = info_fechamento.get("mes")
        dia = info_fechamento.get("dia")
        hora = info_fechamento.get("hora")
        minuto = info_fechamento.get("minuto")

        data_fechamento = datetime(ano, mes, dia, hora, minuto)
        agora = datetime.now()

        diferenca = data_fechamento - agora
        total_segundos = int(diferenca.total_seconds())

        if total_segundos <= 0:
            return '<span class="market-timer-inline-closed">🔒 MERCADO FECHADO</span>'

        total_horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60

        if total_horas > 0:
            texto_tempo = f"MERCADO FECHA EM {total_horas}H {minutos:02d}MIN"
            return f'<span class="market-timer-inline-open">⏱️ {texto_tempo}</span>'
        else:
            texto_tempo = f"ATENÇÃO: MERCADO FECHA EM {minutos} MIN!"
            return f'<span class="market-timer-inline-alert">⚠️ {texto_tempo}</span>'
    except Exception:
        return '<span class="market-timer-inline-open">⏱️ MERCADO ABERTO</span>'

@st.cache_data(ttl=120)
def carregar_partidas_com_escudos(num_rodada):
    try:
        res = requests.get(f"https://api.cartola.globo.com/partidas/{num_rodada}", headers=HEADERS, timeout=4)
        if res.status_code == 200:
            dados = res.json()
            partidas = dados.get("partidas", [])
            clubes = dados.get("clubes", {})
            
            jogos = []
            for p in partidas:
                id_casa = str(p.get("clube_casa_id"))
                id_vis = str(p.get("clube_visitante_id"))
                clube_casa = clubes.get(id_casa, {})
                clube_vis = clubes.get(id_vis, {})
                
                nome_casa = clube_casa.get("nome", "").upper()
                nome_vis = clube_vis.get("nome", "").upper()
                escudos_casa = clube_casa.get("escudos", {})
                escudos_vis = clube_vis.get("escudos", {})
                
                escudo_casa = escudos_casa.get("60x60") or escudos_casa.get("30x30") or ""
                escudo_vis = escudos_vis.get("60x60") or escudos_vis.get("30x30") or ""
                
                jogos.append({
                    "escudo_casa": escudo_casa,
                    "escudo_vis": escudo_vis,
                    "nome_casa": nome_casa,
                    "nome_vis": nome_vis,
                    "placar_casa": p.get("placar_oficial_mandante"),
                    "placar_vis": p.get("placar_oficial_visitante")
                })
            return jogos
    except Exception:
        pass
    return []

@st.cache_data(ttl=120)
def carregar_base_vencedores():
    if os.path.exists("base_vencedores.csv"):
        try:
            df_v = pd.read_csv("base_vencedores.csv", sep=None, engine='python', encoding='utf-8-sig')
            df_v.columns = df_v.columns.str.strip()
            return df_v
        except Exception:
            return None
    return None

# ==========================================
# 3. SCOUT LAB COM MÍNIMO PARA VALORIZAR & DESFALQUES
# ==========================================
@st.cache_data(ttl=300)
def carregar_dados_completos_scout():
    try:
        res_m = requests.get("https://api.cartola.globo.com/atletas/mercado", headers=HEADERS, timeout=5)
        res_c = requests.get("https://api.cartola.globo.com/clubes", headers=HEADERS, timeout=5)
        res_s = requests.get("https://api.cartola.globo.com/mercado/status", timeout=5)
        
        status = res_s.json() if res_s.status_code == 200 else {}
        atletas = res_m.json().get("atletas", []) if res_m.status_code == 200 else []
        clubes = res_c.json() if res_c.status_code == 200 else {}
        
        posicoes = {1: "GOL", 2: "LAT", 3: "ZAG", 4: "MEI", 5: "ATA", 6: "TEC"}
        
        lista_final = []
        for a in atletas:
            cid = str(a.get("clube_id"))
            clube_info = clubes.get(cid, {}) if isinstance(clubes, dict) else {}
            clube_nome = clube_info.get("nome", "Time")
            
            media = float(a.get("media_num", 0.0))
            preco = float(a.get("preco_num", 0.0))
            status_id = a.get("status_id")

            mpv = round(preco * 0.45, 2)
            projecao = media * 1.15 if status_id == 7 else media * 0.85
            score = (projecao * 0.60) + ((projecao / max(0.1, preco)) * 4.0)

            status_str = "Confirmado" if status_id == 7 else ("Em dúvida" if status_id == 2 else ("Nulo/Outro" if status_id == 6 else "Fora"))

            lista_final.append({
                "atleta_id": a.get("atleta_id"),
                "jogador": a.get("apelido", "Atleta"),
                "time": clube_nome,
                "posicao": posicoes.get(a.get("posicao_id"), "MEI"),
                "preco": preco,
                "media": media,
                "min_valorizar": mpv,
                "projecao": round(projecao, 2),
                "score": round(score, 2),
                "status_id": status_id,
                "status": status_str
            })
            
        return pd.DataFrame(lista_final), status.get("rodada_atual", 1)
    except Exception:
        return pd.DataFrame(), 1

# ==========================================
# 4. CARREGAMENTO DAS VARIÁVEIS
# ==========================================
df, rodada_atual, status_mercado, info_fechamento = carregar_dados_liga()
df_vencedores = carregar_base_vencedores()
lista_partidas = carregar_partidas_com_escudos(rodada_atual)

# ==========================================
# 5. CABEÇALHO E JOGOS
# ==========================================
status_tag = "🔴 JOGOS AO VIVO" if status_mercado == 2 else "🟢 PRÓXIMA RODADA"

if lista_partidas:
    cards_html_list = []
    for j in lista_partidas:
        placar_str = f'<div class="match-score">{j["placar_casa"]} x {j["placar_vis"]}</div>' if j["placar_casa"] is not None else '<div class="match-score">VS</div>'
        card_item = (
            f'<div class="match-card">'
            f'<img src="{j["escudo_casa"]}" title="{j["nome_casa"]}">'
            f'{placar_str}'
            f'<img src="{j["escudo_vis"]}" title="{j["nome_vis"]}">'
            f'</div>'
        )
        cards_html_list.append(card_item)

    st.markdown(f"""
        <div class="matches-panel-container">
            <div class="matches-panel-header">⚽ BRASILEIRÃO {rodada_atual}ª RODADA [{status_tag}]</div>
            <div class="matches-grid">{"".join(cards_html_list)}</div>
        </div>
    """, unsafe_allow_html=True)

badge_timer = gerar_badge_mercado(info_fechamento, status_mercado)
img_logo_html = f'<img src="{URL_BASE64_LOGO}" class="header-logo-img" alt="Logo">' if URL_BASE64_LOGO else ''

st.markdown(f"""
    <div class="header-main-flex">
        {img_logo_html}
        <div class="header-col-wrapper">
            <div class="header-title-container">
                <h1>BLACK GUYS LEAGUE</h1>
                {badge_timer}
            </div>
            <div class="subtitle-header">TEMPORADA 2026 • PORTAL OFICIAL DE PERFORMANCE & SCOUT LAB</div>
            <a href="https://cartola.globo.com/#!/competicoes/classica/blackguys-league" target="_blank" rel="noopener noreferrer" class="link-liga">🔗 Acessar Liga Oficial no Cartola FC</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

col_status, col_btn = st.columns([3, 1])
with col_status:
    if status_mercado == 2:
        st.markdown("<h5 style='color: #ef4444; margin: 0;'>🔴 Jogos em andamento! Dados sincronizados em tempo real.</h5>", unsafe_allow_html=True)
    else:
        st.markdown("<h5 style='color: #22c55e; margin: 0;'>⚡ Dados sincronizados via ThreadPool com a API Oficial.</h5>", unsafe_allow_html=True)

with col_btn:
    if st.button("🔄 FORÇAR RECARGA / ATUALIZAR", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ==========================================
# 6. PAINEL INDIVIDUAL & METRICAS
# ==========================================
if not df.empty:
    st.subheader("🔍 Painel de Desempenho Individual do Time")
    time_selecionado = st.selectbox("Selecione um time para ver a análise completa:", df["Time"].tolist())
    
    dados_time = df[df["Time"] == time_selecionado].iloc[0]
    media_pontos_liga = df["Pontos Ganhos (Última Rodada)"].mean()
    media_patrimonio_liga = df["Patrimônio (C$)"].mean()
    
    pt_atual = dados_time["Pontos Ganhos (Última Rodada)"]
    pt_ant = dados_time["Pontos Rodada Anterior"]
    diff_pontos = pt_atual - pt_ant
    html_diff_pontos = f'<span class="txt-up">↑ {diff_pontos:.2f}</span>' if diff_pontos >= 0 else f'<span class="txt-down">↓ {abs(diff_pontos):.2f}</span>'
    
    val_cartoletas = dados_time["Valorização (C$)"]
    html_val_cartoletas = f'<span class="txt-up">↑ {val_cartoletas:.2f}</span>' if val_cartoletas >= 0 else f'<span class="txt-down">↓ {abs(val_cartoletas):.2f}</span>'

    st.markdown(f"<h3 style='margin-bottom:0; color:#00f2ff;'>⚽ {dados_time['Time']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#c084fc; font-weight:bold; margin-bottom:15px;'>Cartoleiro: {dados_time['Cartoleiro']} | Posição Geral: #{dados_time['Posição Geral']}</p>", unsafe_allow_html=True)

    c_box1, c_box2 = st.columns(2)
    with c_box1:
        st.markdown(f'<div class="box-m1"><div class="lbl-title">⚽ ÚLTIMA PONTUAÇÃO</div><div style="display:flex; align-items:baseline; margin-top:5px;"><span class="val-num">{pt_atual:.2f}</span>{html_diff_pontos}</div><div style="margin-top:8px; font-size:13px; color:#94a3b8;">MÉDIA DOS CARTOLEIROS: <strong style="color:#f1f5f9;">{media_pontos_liga:.2f} pts</strong></div></div>', unsafe_allow_html=True)

    with c_box2:
        st.markdown(f'<div class="box-m2"><div class="lbl-title">💰 PATRIMÔNIO</div><div style="display:flex; align-items:baseline; margin-top:5px;"><span class="val-num">C$ {dados_time["Patrimônio (C$)"]:.2f}</span>{html_val_cartoletas}</div><div style="margin-top:8px; font-size:13px; color:#94a3b8;">MÉDIA DOS CARTOLEIROS: <strong style="color:#f1f5f9;">C$ {media_patrimonio_liga:.2f}</strong></div></div>', unsafe_allow_html=True)

    st.divider()

    lider_geral = df.iloc[0]
    mito_rodada = df.sort_values(by="Pontos Ganhos (Última Rodada)", ascending=False).iloc[0]
    pior_rodada = df.sort_values(by="Pontos Ganhos (Última Rodada)", ascending=True).iloc[0]

    k1, k2, k3 = st.columns(3)
    k1.metric("🥇 LÍDER GERAL", f"{lider_geral['Time']}", f"{lider_geral['Total Acumulado']} pts")
    k2.metric("🚀 MITO DA RODADA", f"{mito_rodada['Time']}", f"+{mito_rodada['Pontos Ganhos (Última Rodada)']} pts")
    k3.metric("📉 MALA CHEIA DA RODADA", f"{pior_rodada['Time']}", f"{pior_rodada['Pontos Ganhos (Última Rodada)']} pts")

    st.write("")

    # ==========================================
    # 7. ABAS PRINCIPAIS + MODO X1 E ZUEIRA
    # ==========================================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏆 Classificação Geral", 
        "⚔️ Confronto Direto (X1)", 
        "📱 Resumo WhatsApp",
        "🥇 Campeões do Mês", 
        "💰 Guia de Valorização", 
        "🤖 Cartola Scout Lab"
    ])

    # --- TAB 1: CLASSIFICAÇÃO & GRÁFICOS ---
    with tab1:
        st.subheader("⚡ Tabela de Posições e Desempenho da Liga")
        visao = st.radio("Selecione a ordem de visualização:", ["Classificação Geral (Total Acumulado)", "Ranking da Última Rodada (Pontos Ganhos)"], horizontal=True)
        st.write("")
        
        if visao == "Classificação Geral (Total Acumulado)":
            st.dataframe(
                df[["Posição Geral", "Conquistas", "Time", "Cartoleiro", "Pontos Ganhos (Última Rodada)", "Total Acumulado", "Dif. p/ Rival", "Dif. p/ Líder"]],
                column_config={
                    "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn("Ganho na Rodada (pts)", format="%.2f"), 
                    "Total Acumulado": st.column_config.NumberColumn("Total Geral (pts)", format="%.2f")
                },
                use_container_width=True, hide_index=True
            )
        else:
            df_rodada = df.sort_values(by="Pontos Ganhos (Última Rodada)", ascending=False).reset_index(drop=True)
            df_rodada["Pos. Rodada"] = df_rodada.index + 1
            st.dataframe(
                df_rodada[["Pos. Rodada", "Conquistas", "Time", "Cartoleiro", "Pontos Ganhos (Última Rodada)", "Total Acumulado"]],
                column_config={"Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn("Pontos Ganhos (Última Rodada)", format="+%.2f")},
                use_container_width=True, hide_index=True
            )

        st.divider()

        # NOVO MÓDULO VISUAL: HOT STREAK / SEQUÊNCIA DA LIGA
        st.markdown("### 🔥 Destaque de Sequência e Disparada")
        c_hot1, c_hot2 = st.columns(2)
        
        df_subida = df.sort_values(by="Pontos Rodada Anterior", ascending=False)
        maior_subida = df_subida.iloc[0] if not df_subida.empty else df.iloc[0]
        
        with c_hot1:
            st.markdown(f"""
                <div style="background: rgba(124, 58, 237, 0.15); border: 1px solid #7c3aed; border-radius: 12px; padding: 14px;">
                    <h5 style="color: #c084fc; margin:0;">🚀 MAIOR EVOLUÇÃO RECENTE</h5>
                    <h3 style="color: #ffffff; margin-top:5px;">{maior_subida['Time']}</h3>
                    <p style="margin:0; font-size:13px; color:#94a3b8;">Consistência mantida com <strong>{maior_subida['Pontos Rodada Anterior']} pts</strong> na rodada anterior.</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_hot2:
            st.markdown(f"""
                <div style="background: rgba(0, 242, 255, 0.15); border: 1px solid #00f2ff; border-radius: 12px; padding: 14px;">
                    <h5 style="color: #00f2ff; margin:0;">💰 MAIOR PATRIMÔNIO DA LIGA</h5>
                    <h3 style="color: #ffffff; margin-top:5px;">{df.sort_values(by="Patrimônio (C$)", ascending=False).iloc[0]['Time']}</h3>
                    <p style="margin:0; font-size:13px; color:#94a3b8;">Cofre cheio com <strong>C$ {df.sort_values(by="Patrimônio (C$)", ascending=False).iloc[0]['Patrimônio (C$)']}</strong> acumulados.</p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📊 Comparativo da Liga (Top Pontuadores)")
        fig_bar = px.bar(
            df.head(10), 
            x="Time", 
            y="Total Acumulado", 
            color="Total Acumulado",
            text="Total Acumulado",
            color_continuous_scale="Purples",
            template="plotly_dark"
        )
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: CONFRONTO DIRETO (X1) ---
    with tab2:
        st.subheader("⚔️ Desafio X1: Confronto Direto Entre Cartoleiros")
        col_x1, col_x2 = st.columns(2)
        
        times_lista = df["Time"].tolist()
        with col_x1:
            t1 = st.selectbox("Selecione o Time 1:", times_lista, index=0)
        with col_x2:
            t2 = st.selectbox("Selecione o Time 2:", times_lista, index=min(1, len(times_lista)-1))

        if t1 == t2:
            st.warning("Escolha dois times diferentes para realizar o confronto X1!")
        else:
            d1 = df[df["Time"] == t1].iloc[0]
            d2 = df[df["Time"] == t2].iloc[0]

            st.write("")
            c_res1, c_vs, c_res2 = st.columns([2, 1, 2])
            
            with c_res1:
                st.markdown(f"<h3 style='text-align:center;'>{d1['Time']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center; color:#c084fc;'>{d1['Cartoleiro']}</p>", unsafe_allow_html=True)
                st.metric("Total Acumulado", f"{d1['Total Acumulado']} pts")
                st.metric("Pontos na Rodada", f"{d1['Pontos Ganhos (Última Rodada)']} pts")
                st.metric("Patrimônio", f"C$ {d1['Patrimônio (C$)']}")

            with c_vs:
                st.markdown("<h1 style='text-align:center; margin-top:50px;'>VS</h1>", unsafe_allow_html=True)
                diff_x1 = d1["Total Acumulado"] - d2["Total Acumulado"]
                if diff_x1 > 0:
                    st.success(f"**{d1['Time']}** lidera por +{diff_x1:.2f} pts!")
                elif diff_x1 < 0:
                    st.success(f"**{d2['Time']}** lidera por +{abs(diff_x1):.2f} pts!")
                else:
                    st.info("Empate absoluto no total!")

            with c_res2:
                st.markdown(f"<h3 style='text-align:center;'>{d2['Time']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center; color:#c084fc;'>{d2['Cartoleiro']}</p>", unsafe_allow_html=True)
                st.metric("Total Acumulado", f"{d2['Total Acumulado']} pts")
                st.metric("Pontos na Rodada", f"{d2['Pontos Ganhos (Última Rodada)']} pts")
                st.metric("Patrimônio", f"C$ {d2['Patrimônio (C$)']}")

    # --- TAB 3: RESUMO WHATSAPP ---
    with tab3:
        st.subheader("📱 Gerador de Resumo para WhatsApp")
        st.caption("Copie o texto formatado abaixo para enviar no grupo da liga ao final da rodada!")
        
        texto_wa = f"""*🚨 RESUMO BLACK GUYS LEAGUE - RODADA {rodada_atual} 🚨*

🥇 *LÍDER GERAL:* {lider_geral['Time']} ({lider_geral['Total Acumulado']} pts)
🚀 *MITO DA RODADA:* {mito_rodada['Time']} (+{mito_rodada['Pontos Ganhos (Última Rodada)']} pts)
📉 *MALA CHEIA:* {pior_rodada['Time']} ({pior_rodada['Pontos Ganhos (Última Rodada)']} pts)

*TOP 5 DA LIGA:*
"""
        for i, row in df.head(5).iterrows():
            texto_wa += f"{row['Posição Geral']}º {row['Time']} - {row['Total Acumulado']} pts\n"

        texto_wa += f"\n👉 Acesse o painel completo para ver mais estatísticas!"
        
        st.code(texto_wa, language="markdown")

    # --- TAB 4: CAMPEÕES DO MÊS ---
    with tab4:
        st.subheader("👑 Galeria de Campeões Mensais")
        if df_vencedores is not None and not df_vencedores.empty:
            st.dataframe(df_vencedores, use_container_width=True, hide_index=True)
        else:
            st.info("📌 Envie o arquivo `base_vencedores.csv` para o GitHub para exibir a galeria de campeões.")

    # --- TAB 5: GUIA DE VALORIZAÇÃO ---
    with tab5:
        st.subheader("💰 Painel de Patrimônio & Valorização Ao Vivo")
        df_val = df.sort_values(by="Valorização (C$)", ascending=False).reset_index(drop=True)
        df_val["Rank Valorização"] = df_val.index + 1
        st.dataframe(
            df_val[["Rank Valorização", "Time", "Cartoleiro", "Valorização (C$)", "Patrimônio (C$)", "Pontos Ganhos (Última Rodada)"]],
            column_config={
                "Valorização (C$)": st.column_config.NumberColumn("Valorização na Rodada (C$)", format="C$ %.2f"),
                "Patrimônio (C$)": st.column_config.NumberColumn("Patrimônio Total (C$)", format="C$ %.2f")
            },
            use_container_width=True, hide_index=True
        )

    # --- TAB 6: SCOUT LAB (COM BUSCA DE JOGADOR E AUTOCOMPLETE) ---
    with tab6:
        st.subheader("🤖 Cartola Scout Lab (Laboratório de Inteligência)")
        st.caption("Monte seu esquadrão ideal, consulte métricas e pesquise por qualquer jogador para checar o status.")
        
        df_scout_full, r_num = carregar_dados_completos_scout()

        if not df_scout_full.empty:
            st.markdown("### 🔍 Consulta Rápida de Status de Jogadores")
            
            df_scout_full["nome_busca"] = df_scout_full["jogador"] + " (" + df_scout_full["time"] + " - " + df_scout_full["posicao"] + ")"
            lista_jogadores_busca = sorted(df_scout_full["nome_busca"].tolist())
            
            jogador_pesquisado_str = st.selectbox(
                "Digite o nome do jogador para consultar o status atual no Cartola:",
                options=[""] + lista_jogadores_busca,
                index=0,
                placeholder="Ex: Arrascaeta, Pedro, Garro..."
            )

            if jogador_pesquisado_str:
                atleta_info = df_scout_full[df_scout_full["nome_busca"] == jogador_pesquisado_str].iloc[0]
                
                status_atleta = atleta_info["status"]
                
                if atleta_info["status_id"] == 7:
                    cor_status = "#22c55e"
                    icone_status = "✅"
                elif atleta_info["status_id"] == 2:
                    cor_status = "#f97316"
                    icone_status = "⚠️"
                else:
                    cor_status = "#ef4444"
                    icone_status = "❌"

                st.markdown(f"""
                    <div style="background: rgba(18, 12, 38, 0.9); border: 2px solid {cor_status}; border-radius: 12px; padding: 16px; margin-bottom: 15px; backdrop-filter: blur(8px);">
                        <h4 style="margin: 0; color: #ffffff;">{icone_status} {atleta_info['jogador']} <span style="font-size:14px; color:#c084fc;">({atleta_info['time']} - {atleta_info['posicao']})</span></h4>
                        <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
                            <div>Status: <strong style="color: {cor_status};">{status_atleta}</strong></div>
                            <div>Preço: <strong>C$ {atleta_info['preco']:.2f}</strong></div>
                            <div>Média: <strong>{atleta_info['media']:.2f} pts</strong></div>
                            <div>Mínimo p/ Valorizar: <strong>{atleta_info['min_valorizar']:.2f} pts</strong></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.divider()

            df_duvidas = df_scout_full[df_scout_full["status_id"].isin([2, 6, 5])]
            if not df_duvidas.empty:
                st.warning(f"⚠️ **Radar Geral:** Existem **{len(df_duvidas)}** atletas registrados como 'Em Dúvida', 'Nulo' ou 'Contundido' nesta rodada!")
                with st.expander("🔍 Ver Tabela Completa de Desfalques e Dúvidas"):
                    st.dataframe(df_duvidas[["jogador", "time", "posicao", "preco", "status"]], use_container_width=True, hide_index=True)

            col_scout_left, col_scout_right = st.columns([1, 2])

            with col_scout_left:
                st.markdown("### ⚙️ Parâmetros do Esquadrão")
                
                patrimonio_sugerido = float(dados_time["Patrimônio (C$)"]) if "dados_time" in locals() else 100.0
                
                orcamento = st.number_input(
                    "Patrimônio Disponível (C$):", 
                    min_value=30.0, 
                    max_value=300.0, 
                    value=patrimonio_sugerido, 
                    step=0.5
                )
                esquema_tatico = st.selectbox("Formação Tática:", ["4-3-3", "4-4-2", "3-5-2", "3-4-3", "5-3-2", "5-4-1"])
                filtro_posicao = st.selectbox("Filtrar Posição Tabela:", ["TODAS", "GOL", "LAT", "ZAG", "MEI", "ATA", "TEC"])
                
                btn_montar = st.button("🚀 Montar Escalação Ideal", use_container_width=True)

            with col_scout_right:
                st.markdown("### 📊 Estatísticas do Mercado")
                s1, s2 = st.columns(2)
                s1.metric("Atletas Analisados", len(df_scout_full))
                s2.metric("Média de Preço do Mercado", f"C$ {df_scout_full['preco'].mean():.2f}")

            st.divider()

            esquemas_dict = {
                "4-3-3": {"GOL": 1, "LAT": 2, "ZAG": 2, "MEI": 3, "ATA": 3, "TEC": 1},
                "4-4-2": {"GOL": 1, "LAT": 2, "ZAG": 2, "MEI": 4, "ATA": 2, "TEC": 1},
                "3-5-2": {"GOL": 1, "LAT": 0, "ZAG": 3, "MEI": 5, "ATA": 2, "TEC": 1},
                "3-4-3": {"GOL": 1, "LAT": 0, "ZAG": 3, "MEI": 4, "ATA": 3, "TEC": 1},
                "5-3-2": {"GOL": 1, "LAT": 2, "ZAG": 3, "MEI": 3, "ATA": 2, "TEC": 1},
                "5-4-1": {"GOL": 1, "LAT": 2, "ZAG": 3, "MEI": 4, "ATA": 1, "TEC": 1},
            }

            if btn_montar or "squad_gerado" not in st.session_state:
                necessidade = esquemas_dict[esquema_tatico]
                df_filtrado_status = df_scout_full[df_scout_full["status_id"] == 7].sort_values(by="score", ascending=False)

                titulares = []
                custo_atual = 0.0

                for pos, qtd in necessidade.items():
                    if qtd > 0:
                        opcoes_pos = df_filtrado_status[df_filtrado_status["posicao"] == pos]
                        for _, atleta in opcoes_pos.iterrows():
                            if len([x for x in titulares if x["posicao"] == pos]) < qtd:
                                if custo_atual + atleta["preco"] <= orcamento:
                                    titulares.append(atleta)
                                    custo_atual += atleta["preco"]

                st.session_state["squad_gerado"] = pd.DataFrame(titulares)
                st.session_state["custo_squad"] = custo_atual

            df_titulares = st.session_state.get("squad_gerado", pd.DataFrame())
            custo_time = st.session_state.get("custo_squad", 0.0)

            c_tit, c_cap = st.columns([2, 1])

            with c_tit:
                st.markdown(f"### 🛡️ Esquadrão Sugerido ({esquema_tatico}) — Custo: C$ {custo_time:.2f} / C$ {orcamento:.2f}")
                if not df_titulares.empty:
                    st.dataframe(
                        df_titulares[["posicao", "jogador", "time", "preco", "min_valorizar", "projecao", "status"]],
                        column_config={
                            "posicao": "Posição",
                            "jogador": "Atleta",
                            "time": "Clube",
                            "preco": st.column_config.NumberColumn("Custo", format="C$ %.2f"),
                            "min_valorizar": st.column_config.NumberColumn("Mín. p/ Valorizar", format="%.2f pts"),
                            "projecao": st.column_config.NumberColumn("Projeção", format="%.2f pts")
                        },
                        use_container_width=True, hide_index=True
                    )
                else:
                    st.warning("Não foi possível montar um time completo com esse orçamento. Tente aumentar o valor disponível.")

            with c_cap:
                st.markdown("### ⭐ Sugestão de Capitães")
                if not df_titulares.empty:
                    capitaes = df_titulares[df_titulares["posicao"] != "TEC"].sort_values(by="projecao", ascending=False).head(3)
                    for i, (_, cap) in enumerate(capitaes.iterrows()):
                        st.markdown(f"""
                            <div class="card-scout-player">
                                <strong>{i+1}º Capitão: {cap['jogador']}</strong> ({cap['time']})<br>
                                Posição: {cap['posicao']} | Projeção: <span style="color:#00f2ff; font-weight:bold;">{cap['projecao']} pts</span>
                            </div>
                        """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 🏆 Ranking de Oportunidades do Mercado")
            df_scout_view = df_scout_full if filtro_posicao == "TODAS" else df_scout_full[df_scout_full["posicao"] == filtro_posicao]
            st.dataframe(
                df_scout_view[["jogador", "time", "posicao", "preco", "min_valorizar", "media", "projecao", "score", "status"]],
                column_config={
                    "preco": st.column_config.NumberColumn("Preço", format="C$ %.2f"),
                    "min_valorizar": st.column_config.NumberColumn("Mínimo p/ Valorizar", format="%.2f pts"),
                    "projecao": st.column_config.NumberColumn("Projeção", format="%.2f pts"),
                    "score": st.column_config.NumberColumn("Score de Compra", format="%.2f")
                },
                use_container_width=True, hide_index=True
            )

    st.divider()
    st.caption(f"⚡ Black Guys League | Rodada {rodada_atual} | Sistema otimizado com ThreadPoolExecutor.")
