import streamlit as st
import pandas as pd
import requests
import os
import base64
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(
    page_title="Black Guys League - Cartola FC",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Converte a logo em Base64
def carregar_logo_base64():
    for ext in ["logo.png", "logo.jpg", "logo.jpeg"]:
        if os.path.exists(ext):
            with open(ext, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
    return ""

URL_BASE64_LOGO = carregar_logo_base64()

# 3. Estilização Cyberpunk Neon + Layout Responsivo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Rajdhani:wght@600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top center, #1e0b36 0%, #0a0813 60%, #030206 100%);
        color: #f1f5f9;
        font-family: 'Rajdhani', sans-serif;
    }

    .header-main-flex {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 10px;
    }

    .header-logo-img {
        width: 130px;
        height: auto;
        object-fit: contain;
    }

    h1 {
        font-family: 'Teko', sans-serif !important;
        font-size: 52px !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2ff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0px !important;
        line-height: 1 !important;
    }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.4);
        font-weight: 700;
    }

    .header-title-container {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .market-timer-inline-open {
        background: #ccff00;
        color: #0a0813;
        font-family: 'Teko', sans-serif;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 4px 12px;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(204, 255, 0, 0.5);
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
    }

    .market-timer-inline-closed {
        background: #ef4444;
        color: #ffffff;
        font-family: 'Teko', sans-serif;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 4px 12px;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.5);
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
    }

    .subtitle-header {
        color: #c084fc;
        font-weight: 700;
        margin-top: 4px;
        margin-bottom: 6px;
        font-size: 15px;
    }

    .link-liga {
        display: inline-block;
        color: #00f2ff !important;
        font-weight: 700;
        font-size: 14px;
        text-decoration: none;
        letter-spacing: 1px;
        padding: 6px 14px;
        background: rgba(0, 242, 255, 0.08);
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    .matches-panel-container {
        width: 100%;
        background: rgba(10, 8, 19, 0.85);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.15);
        padding: 12px 16px;
        margin-bottom: 20px;
    }

    .matches-panel-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #00f2ff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .matches-grid {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        padding-bottom: 8px;
        -webkit-overflow-scrolling: touch;
    }

    .matches-grid::-webkit-scrollbar {
        height: 5px;
    }
    .matches-grid::-webkit-scrollbar-thumb {
        background: #a855f7;
        border-radius: 4px;
    }

    .match-card {
        flex: 0 0 auto;
        background: rgba(18, 12, 38, 0.8);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        min-width: 150px;
    }

    .match-card img {
        width: 36px !important;
        height: 36px !important;
        object-fit: contain !important;
        display: block !important;
    }

    .match-score {
        font-family: 'Teko', sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        letter-spacing: 1px;
        text-align: center;
    }

    .match-vs {
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        color: #94a3b8;
        font-weight: bold;
    }

    .box-m1 {
        background: rgba(10, 8, 19, 0.85);
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #00f2ff;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        margin-bottom: 10px;
    }

    .box-m2 {
        background: rgba(10, 8, 19, 0.85);
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #22c55e;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.2);
        margin-bottom: 10px;
    }

    .lbl-title {
        font-size: 13px;
        font-weight: bold;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .val-num {
        font-family: 'Teko', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #ffffff;
        line-height: 1;
        margin-right: 8px;
    }

    .txt-up {
        color: #22c55e !important;
        font-size: 22px;
        font-weight: bold;
    }

    .txt-down {
        color: #ef4444 !important;
        font-size: 22px;
        font-weight: bold;
    }

    div[data-testid="stMetric"] {
        background: rgba(18, 12, 38, 0.75);
        border: 2px solid #a855f7;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.35);
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
    }

    button[data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0px 0px;
        padding: 8px 14px !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(180deg, rgba(168, 85, 247, 0.3) 0%, rgba(0, 242, 255, 0.1) 100%) !important;
        color: #00f2ff !important;
        border-bottom: 3px solid #00f2ff !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #a855f7;
        border-radius: 12px;
        overflow: hidden;
    }

    .card-vencedor {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid #eab308;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
        text-align: center;
    }

    .card-dica {
        background: rgba(18, 12, 38, 0.7);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    hr {
        border-color: rgba(0, 242, 255, 0.3) !important;
        margin: 15px 0 !important;
    }

    @media (max-width: 768px) {
        .header-main-flex {
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            width: 100% !important;
        }

        .header-logo-img {
            display: block !important;
            margin: 0 auto 12px auto !important;
            width: 140px !important;
        }

        h1 {
            font-size: 38px !important;
            text-align: center !important;
            width: 100% !important;
        }

        .header-title-container {
            justify-content: center !important;
            flex-direction: column !important;
            gap: 8px !important;
            width: 100% !important;
        }

        .market-timer-inline-open, .market-timer-inline-closed {
            font-size: 18px !important;
            padding: 4px 10px !important;
            margin-top: 4px !important;
        }

        .subtitle-header {
            text-align: center !important;
            font-size: 13px !important;
            width: 100% !important;
        }

        .header-col-wrapper {
            text-align: center !important;
            width: 100% !important;
        }

        .link-liga {
            width: 100% !important;
            text-align: center !important;
            margin-top: 6px !important;
        }

        .val-num {
            font-size: 36px !important;
        }

        .matches-panel-container {
            padding: 10px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# 4. Lógica Corrigida: Soma Direta do CSV com a Pontuação da ÚLTIMA Rodada
@st.cache_data(ttl=30)
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

    lista_times = []
    rodada_ultima_consolidada = rodada_cartola - 1 if status_mercado == 1 else rodada_cartola
    rodada_penultima = rodada_ultima_consolidada - 1

    for _, row in df_base.iterrows():
        nome_time = str(row.get("Time", "")).strip()
        cartoleiro = str(row.get("Cartoleiro", "")).strip()
        
        # Lê a base histórica gravada no CSV
        try:
            pontos_base_historico = float(row.get("Total", 0.0))
            if pd.isna(pontos_base_historico):
                pontos_base_historico = 0.0
        except (ValueError, TypeError):
            pontos_base_historico = 0.0

        time_id = row.get("ID", None)
        try:
            time_id = int(time_id) if pd.notna(time_id) else None
        except (ValueError, TypeError):
            time_id = None

        pt_rodada = 0.0
        pt_rodada_anterior = 0.0
        patrimonio = 100.0
        valorizacao_rodada = 0.0

        if time_id:
            try:
                res_p = session.get(f"https://api.cartola.globo.com/time/id/{time_id}", timeout=3)
                if res_p.status_code == 200:
                    dados = res_p.json()
                    patrimonio = float(dados.get("patrimonio", 100.0))

                    # Se estiver em andamento (Ao Vivo)
                    if status_mercado == 2 and atletas_ao_vivo:
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
                    else:
                        # Pega os pontos da última rodada da API
                        p_raw = dados.get("pontos", 0)
                        if isinstance(p_raw, dict):
                            pt_rodada = float(p_raw.get("rodada", 0.0))
                        elif isinstance(p_raw, (int, float)):
                            pt_rodada = float(p_raw)

                        val_api = dados.get("valorizacao", 0.0)
                        if val_api is not None and float(val_api) != 0.0:
                            valorizacao_rodada = float(val_api)

                if rodada_penultima >= 1:
                    res_ant = session.get(f"https://api.cartola.globo.com/time/id/{time_id}/{rodada_penultima}", timeout=3)
                    if res_ant.status_code == 200:
                        pt_rodada_anterior = float(res_ant.json().get("pontos", 0.0))
            except Exception:
                pass

        # MATEMÁTICA CORRETA:
        # Total Acumulado = Pontuação anterior da base CSV + Pontos obtidos na última rodada
        total_acumulado = pontos_base_historico + pt_rodada

        lista_times.append({
            "Time": nome_time,
            "Cartoleiro": cartoleiro,
            "Pontos Ganhos (Última Rodada)": round(pt_rodada, 2),
            "Pontos Rodada Anterior": round(pt_rodada_anterior, 2),
            "Total Acumulado": round(total_acumulado, 2),
            "Patrimônio (C$)": round(patrimonio, 2),
            "Valorização (C$)": round(valorizacao_rodada, 2)
        })

    df = pd.DataFrame(lista_times)
    
    if not df.empty:
        # Ordena a tabela do maior para o menor Total Acumulado
        df = df.sort_values(by="Total Acumulado", ascending=False).reset_index(drop=True)
        df["Posição Geral"] = df.index + 1

        top_score = df.iloc[0]["Total Acumulado"]
        df["Dif. p/ Rival"] = (df["Total Acumulado"].shift(1) - df["Total Acumulado"]).round(2).fillna(0)
        df["Dif. p/ Líder"] = (top_score - df["Total Acumulado"]).round(2)

    return df, rodada_cartola, status_mercado, info_fechamento

# 5. Contador de Mercado
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
        else:
            texto_tempo = f"MERCADO FECHA EM {minutos} MIN!"

        return f'<span class="market-timer-inline-open">⏱️ {texto_tempo}</span>'
    except Exception:
        return '<span class="market-timer-inline-open">⏱️ MERCADO ABERTO</span>'

# 6. Busca de partidas e escudos da API do Cartola FC
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
                
                escudo_casa = escudos_casa.get("60x60") or escudos_casa.get("45x45") or escudos_casa.get("30x30") or ""
                escudo_vis = escudos_vis.get("60x60") or escudos_vis.get("45x45") or escudos_vis.get("30x30") or ""
                
                placar_casa = p.get("placar_oficial_mandante")
                placar_vis = p.get("placar_oficial_visitante")
                
                jogos.append({
                    "escudo_casa": escudo_casa,
                    "escudo_vis": escudo_vis,
                    "nome_casa": nome_casa,
                    "nome_vis": nome_vis,
                    "placar_casa": placar_casa,
                    "placar_vis": placar_vis
                })
            return jogos
    except Exception:
        pass
    return []

# 7. Carregar Vencedores do Mês
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

# Carregamento dos dados
df, rodada_atual, status_mercado, info_fechamento = carregar_dados_liga()
df_vencedores = carregar_base_vencedores()
lista_partidas = carregar_partidas_com_escudos(rodada_atual)

# --- 8. PAINEL FIXO COM ESCUDOS DA API CARTOLA ---
status_tag = "🔴 JOGOS AO VIVO" if status_mercado == 2 else "🟢 PRÓXIMA RODADA"

if lista_partidas:
    cards_html_list = []
    for j in lista_partidas:
        if j["placar_casa"] is not None and j["placar_vis"] is not None:
            placar_str = f'<div class="match-score">{j["placar_casa"]} x {j["placar_vis"]}</div>'
        else:
            placar_str = '<div class="match-vs">VS</div>'
            
        card_item = (
            f'<div class="match-card">'
            f'<img src="{j["escudo_casa"]}" title="{j["nome_casa"]}">'
            f'{placar_str}'
            f'<img src="{j["escudo_vis"]}" title="{j["nome_vis"]}">'
            f'</div>'
        )
        cards_html_list.append(card_item)

    cards_html = "".join(cards_html_list)

    st.markdown(f"""
        <div class="matches-panel-container">
            <div class="matches-panel-header">
                ⚽ BRASILEIRÃO {rodada_atual}ª RODADA [{status_tag}]
            </div>
            <div class="matches-grid">
                {cards_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 9. CABEÇALHO UNIFICADO ---
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
            <div class="subtitle-header">TEMPORADA 2026 • PORTAL OFICIAL DE PERFORMANCE</div>
            <a href="https://cartola.globo.com/#!/competicoes/classica/blackguys-league" target="_blank" rel="noopener noreferrer" class="link-liga">🔗 Acessar Liga Oficial no Cartola FC</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- BOTÃO DE ATUALIZAÇÃO FORÇADA ---
col_status, col_btn = st.columns([3, 1])
with col_status:
    if status_mercado == 2:
        st.markdown("<h5 style='color: #ef4444; margin: 0;'>🔴 Jogos em andamento! Dados sincronizados em tempo real.</h5>", unsafe_allow_html=True)
    else:
        st.markdown("<h5 style='color: #22c55e; margin: 0;'>⚡ Tabela atualizada com a soma da última rodada.</h5>", unsafe_allow_html=True)

with col_btn:
    if st.button("🔄 FORÇAR RECARGA / ATUALIZAR TABELA", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- 10. CARD DETALHADO INSTANTÂNEO ---
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
        st.markdown(
            f'<div class="box-m1">'
            f'<div class="lbl-title">⚽ ÚLTIMA PONTUAÇÃO</div>'
            f'<div style="display:flex; align-items:baseline; margin-top:5px;">'
            f'<span class="val-num">{pt_atual:.2f}</span>{html_diff_pontos}'
            f'</div>'
            f'<div style="margin-top:8px; font-size:13px; color:#94a3b8;">'
            f'MÉDIA DOS CARTOLEIROS: <strong style="color:#f1f5f9;">{media_pontos_liga:.2f} pts</strong>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with c_box2:
        st.markdown(
            f'<div class="box-m2">'
            f'<div class="lbl-title">💰 PATRIMÔNIO</div>'
            f'<div style="display:flex; align-items:baseline; margin-top:5px;">'
            f'<span class="val-num">C$ {dados_time["Patrimônio (C$)"]:.2f}</span>{html_val_cartoletas}'
            f'</div>'
            f'<div style="margin-top:8px; font-size:13px; color:#94a3b8;">'
            f'MÉDIA DOS CARTOLEIROS: <strong style="color:#f1f5f9;">C$ {media_patrimonio_liga:.2f}</strong>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # --- VISUALIZAÇÃO DAS ABAS ---
    lider_geral = df.iloc[0]
    mito_rodada = df.sort_values(by="Pontos Ganhos (Última Rodada)", ascending=False).iloc[0]

    k1, k2 = st.columns(2)
    k1.metric("🥇 LÍDER GERAL", f"{lider_geral['Time']}", f"{lider_geral['Total Acumulado']} pts")
    
    rotulo_mito = "🚀 MITO DA RODADA (AO VIVO)" if status_mercado == 2 else "🚀 MITO DA RODADA"
    k2.metric(rotulo_mito, f"{mito_rodada['Time']}", f"+{mito_rodada['Pontos Ganhos (Última Rodada)']} pts")

    st.write("")

    tab1, tab2, tab3 = st.tabs(["🏆 Classificação Geral", "🥇 Campeões do Mês", "💰 Guia de Valorização"])

    with tab1:
        st.subheader("⚡ Tabela de Posições e Desempenho da Liga")
        
        visao = st.radio(
            "Selecione a ordem de visualização:",
            ["Classificação Geral (Total Acumulado)", "Ranking da Última Rodada (Pontos Ganhos)"],
            horizontal=True
        )
        
        st.write("")
        
        if visao == "Classificação Geral (Total Acumulado)":
            st.dataframe(
                df[["Posição Geral", "Time", "Cartoleiro", "Pontos Ganhos (Última Rodada)", "Total Acumulado", "Dif. p/ Rival", "Dif. p/ Líder"]],
                column_config={
                    "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn(
                        "Ganho na Rodada (pts)",
                        format="%.2f"
                    ),
                    "Total Acumulado": st.column_config.NumberColumn(
                        "Total Geral (pts)",
                        format="%.2f"
                    )
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            df_rodada = df.sort_values(by="Pontos Ganhos (Última Rodada)", ascending=False).reset_index(drop=True)
            df_rodada["Pos. Rodada"] = df_rodada.index + 1
            st.dataframe(
                df_rodada[["Pos. Rodada", "Time", "Cartoleiro", "Pontos Ganhos (Última Rodada)", "Total Acumulado"]],
                column_config={
                    "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn(
                        "Pontos Ganhos (Última Rodada)",
                        format="+%.2f"
                    )
                },
                use_container_width=True,
                hide_index=True
            )

    with tab2:
        st.subheader("👑 Galeria de Campeões Mensais")
        st.caption("Premiações e mitações mês a mês na Black Guys League.")
        
        if df_vencedores is not None and not df_vencedores.empty:
            st.dataframe(df_vencedores, use_container_width=True, hide_index=True)
            st.write("")
            st.divider()
            
            cols_v = st.columns(3)
            idx_col = 0
            
            for _, row in df_vencedores.iterrows():
                mes = row.get("Mês", row.get("Mes", "Mês"))
                vencedor = row.get("Vencedor", row.get("Time", "-"))
                pontos = row.get("Pontos", row.get("Pontuação", "-"))
                cartoleiro = row.get("Cartoleiro", "")
                
                with cols_v[idx_col % 3]:
                    st.markdown(f"""
                        <div class="card-vencedor">
                            <h4 style="color: #eab308; margin: 0;">🥇 {mes}</h4>
                            <h3 style="color: #00f2ff; margin: 5px 0;">{vencedor}</h3>
                            <p style="color: #c084fc; margin: 0; font-weight: bold;">{cartoleiro}</p>
                            <p style="color: #e2e8f0; margin-top: 5px; font-size: 18px;"><strong>{pontos}</strong></p>
                        </div>
                    """, unsafe_allow_html=True)
                idx_col += 1
        else:
            st.info("📌 Envie o arquivo `base_vencedores.csv` para o GitHub para exibir a galeria de campeões.")

    with tab3:
        st.subheader("💰 Painel de Patrimônio & Valorização Ao Vivo")
        st.caption("Diferença de cartoletas (C$) ganhas/perdidas na rodada e patrimônio acumulado.")

        df_val = df.sort_values(by="Valorização (C$)", ascending=False).reset_index(drop=True)
        df_val["Rank Valorização"] = df_val.index + 1

        mais_rico = df.sort_values(by="Patrimônio (C$)", ascending=False).iloc[0]
        maior_val = df_val.iloc[0]

        v1, v2 = st.columns(2)
        v1.metric("💎 TIME MAIS RICO (PATRIMÔNIO)", f"{mais_rico['Time']}", f"C$ {mais_rico['Patrimônio (C$)']}")
        
        val_txt = f"+C$ {maior_val['Valorização (C$)']}" if maior_val['Valorização (C$)'] > 0 else f"C$ {maior_val['Valorização (C$)']}"
        rotulo_val = "📈 MAIOR VALORIZAÇÃO DA RODADA (AO VIVO)" if status_mercado == 2 else "📈 MAIOR VALORIZAÇÃO NA RODADA"
        v2.metric(rotulo_val, f"{maior_val['Time']}", val_txt)

        st.write("")
        st.markdown("### 📊 Variação de Cartoletas na Rodada")
        
        st.dataframe(
            df_val[["Rank Valorização", "Time", "Cartoleiro", "Valorização (C$)", "Patrimônio (C$)", "Pontos Ganhos (Última Rodada)"]],
            column_config={
                "Valorização (C$)": st.column_config.NumberColumn(
                    "Valorização na Rodada (C$)",
                    help="Cartoletas calculadas em tempo real durante a rodada",
                    format="C$ %.2f"
                ),
                "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn(
                    "Pontos Conquistados",
                    format="%.2f pts"
                ),
                "Patrimônio (C$)": st.column_config.NumberColumn(
                    "Patrimônio Total (C$)",
                    format="C$ %.2f"
                )
            },
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.markdown("### 📘 Guia Prático de Valorização")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="card-dica">
                <h4 style="color: #00f2ff; margin-top:0;">1ª Rodada (A Regra dos 45%)</h4>
                <p>Na 1ª rodada do campeonato, para um jogador valorizar ele precisa fazer aproximadamente <strong>45% do valor dele em pontos</strong>.</p>
                <ul>
                    <li>Jogador de C$ 10,00 precisa de ~ 4,5 pontos.</li>
                    <li>Escalar jogadores mais baratos (C$ 5 a C$ 8) facilita a valorização.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="card-dica">
                <h4 style="color: #00f2ff; margin-top:0;">2ª Rodada (A Regra da Média)</h4>
                <p>Na 2ª rodada o sistema calcula a <strong>média das duas rodadas</strong>. Jogadores que desvalorizaram na 1ª rodada mas pontuarem bem na 2ª tendem a valorizar bastante.</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="card-dica">
                <h4 style="color: #a855f7; margin-top:0;">3ª Rodada em diante (Mínimo para Valorizar)</h4>
                <p>A partir da 3ª rodada o algoritmo entra no formato padrão: a valorização depende do valor atual do atleta e do seu desempenho recente.</p>
                <ul>
                    <li>Jogadores que desvalorizaram na rodada anterior costumam ter um pontuação mínima menor para voltar a valorizar.</li>
                    <li>Evite escalar jogadores muito caros após uma grande pontuação se o seu foco for ganhar cartoletas.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.caption(f"⚡ Black Guys League | Rodada {rodada_atual} | Sincronizado automaticamente via API Cartola FC.")
