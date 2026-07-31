import streamlit as st
import pandas as pd
import requests
import time
import os

# 1. Configuração da Página
st.set_page_config(
    page_title="Black Guys League - Cartola FC",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização Cyberpunk Neon (Baseada na Logo Oficial)
st.markdown("""
    <style>
    /* Importando fonte gamer / moderna */
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Rajdhani:wght@600;700&display=swap');

    /* Fundo Geral Escuro / Cyberpunk */
    .stApp {
        background: radial-gradient(circle at top center, #1e0b36 0%, #0a0813 60%, #030206 100%);
        color: #f1f5f9;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Cabeçalhos com efeito Neon */
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

    /* Cartões de Métricas (KPIs) Neons */
    div[data-testid="stMetric"] {
        background: rgba(18, 12, 38, 0.75);
        border: 2px solid #a855f7;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.35), inset 0 0 10px rgba(0, 242, 255, 0.1);
        padding: 16px;
        border-radius: 14px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6);
        border-color: #00f2ff;
    }

    div[data-testid="stMetricLabel"] {
        color: #c084fc !important;
        font-size: 16px !important;
        font-weight: bold;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: #00f2ff !important;
        font-family: 'Teko', sans-serif !important;
        font-size: 38px !important;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
    }

    /* Estilização das Abas (Tabs) */
    button[data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #94a3b8 !important;
        font-size: 18px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(180deg, rgba(168, 85, 247, 0.3) 0%, rgba(0, 242, 255, 0.1) 100%) !important;
        color: #00f2ff !important;
        border-bottom: 3px solid #00f2ff !important;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.5);
    }

    /* Tabelas */
    div[data-testid="stDataFrame"] {
        border: 1px solid #a855f7;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
        overflow: hidden;
    }

    /* Linha Divisória Neon */
    hr {
        border-color: rgba(0, 242, 255, 0.3) !important;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Lista Oficial dos Times da Liga
TIMES_LEAGUE = [
    ("Tupinambaranas Futebol Clube", "Vitor Geromini"),
    ("Lockdown United", "Caio Monteiro"),
    ("Budaibes FC", "Bruno Budaibes"),
    ("Open de Corote FC", "Hermes Augusto"),
    ("Burpee F.C.", "Helio Isayama"),
    ("Toon Squad FC", "Vinicius Monteiro"),
    ("Covrinthians FC", "Denis M. Covre"),
    ("Bom Dcopus SPFC", "Gutenberg"),
    ("CPR sport", "Cesar Postingel Ramo"),
    ("Bueno team EC", "Marcelo Bueno"),
    ("Red, Black and White", "Diego Covre"),
    ("Tgramos82", "Thiago Ramos"),
    ("promadalozofc", "madalozo"),
    ("Pedroo SPFC", "Pedro Lopes"),
    ("Mitador Campeão", "Barves")
]

@st.cache_data(ttl=300)
def carregar_dados_liga():
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        res_m = requests.get("https://api.cartola.globo.com/mercado/status", headers=headers, timeout=5)
        rodada_atual = res_m.json().get("rodada_atual", 0) if res_m.status_code == 200 else 20
    except:
        rodada_atual = 20
        
    turno_atual = 2 if rodada_atual > 19 else 1
    
    # Carrega base local como fallback inteligente
    df_base_dict = {}
    for csv_file in ["base_cartola_oficial.csv", "base_cartola.csv"]:
        if os.path.exists(csv_file):
            try:
                df_csv = pd.read_csv(csv_file, sep=None, engine='python', encoding='utf-8-sig')
                df_csv.columns = df_csv.columns.str.strip()
                for _, r in df_csv.iterrows():
                    df_base_dict[str(r["Time"]).strip().lower()] = float(r["Total"])
                break
            except:
                pass

    lista_times = []
    
    for nome_time, cartoleiro in TIMES_LEAGUE:
        nome_limpo = nome_time.replace(",", "").replace(" and ", " ").replace("  ", " ").strip()
        url_busca = "https://api.cartola.globo.com/times"
        time_id = None
        
        try:
            res_b = requests.get(url_busca, params={"q": nome_limpo}, headers=headers, timeout=5)
            if res_b.status_code == 200:
                resultados = res_b.json()
                lista_r = resultados if isinstance(resultados, list) else resultados.get("times", [])
                for t in lista_r:
                    if t.get("nome_cartola", "").lower() == cartoleiro.lower() or t.get("nome", "").lower() == nome_time.lower():
                        time_id = t.get("time_id")
                        break
                if not time_id and len(lista_r) > 0:
                    time_id = lista_r[0].get("time_id")
        except:
            pass

        pt_rodada, pt_mes, pt_turno, pt_total_api = 0.0, 0.0, 0.0, 0.0
        
        if time_id:
            try:
                res_p = requests.get(f"https://api.cartola.globo.com/time/id/{time_id}", headers=headers, timeout=5)
                if res_p.status_code == 200:
                    dados = res_p.json()
                    p_raw = dados.get("pontos", 0)
                    if isinstance(p_raw, dict):
                        pt_total_api = float(p_raw.get("campeonato", p_raw.get("total", 0)))
                        pt_rodada = float(p_raw.get("rodada", 0))
                        pt_mes = float(p_raw.get("mes", 0))
                        pt_turno = float(p_raw.get("turno", 0))
                    elif isinstance(p_raw, (int, float)):
                        pt_total_api = float(p_raw)
            except:
                pass
        
        total_historico = df_base_dict.get(nome_time.lower(), 0.0)
        total_final = pt_total_api if pt_total_api > 0 else (total_historico + pt_rodada)
        
        lista_times.append({
            "Time": nome_time,
            "Cartoleiro": cartoleiro,
            "Total": round(total_final, 2),
            "Última Rodada": round(pt_rodada, 2),
            "Mês": round(pt_mes, 2),
            "Turno": round(pt_turno, 2)
        })

    df = pd.DataFrame(lista_times)
    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
    df["Posição"] = df.index + 1
    
    top_score = df.iloc[0]["Total"]
    df["Dif. p/ Rival"] = (df["Total"].shift(1) - df["Total"]).round(2).fillna(0)
    df["Dif. p/ Líder"] = (top_score - df["Total"]).round(2)
    
    return df, rodada_atual, turno_atual

# --- CABEÇALHO DO SITE COM A LOGO ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    # Procura a logo em png ou jpg na pasta
    logo_path = None
    for ext in ["logo.jpg", "logo.png", "logo.jpeg"]:
        if os.path.exists(ext):
            logo_path = ext
            break
            
    if logo_path:
        st.image(logo_path, width=150)
    else:
        st.title("⚔️")

with col_title:
    st.title("BLACK GUYS LEAGUE")
    st.markdown("<h4 style='color: #c084fc; margin-top: -10px;'>TEMPORADA 2026 • PORTAL OFICIAL DE PERFORMANCE</h4>", unsafe_allow_html=True)

st.divider()

# Carregando Dados
with st.spinner("⚡ Conectando aos servidores do Cartola FC..."):
    df, rodada_atual, turno_atual = carregar_dados_liga()

if not df.empty:
    # METRIC CARDS
    lider_geral = df.iloc[0]
    mito_rodada = df.sort_values(by="Última Rodada", ascending=False).iloc[0]
    lider_mes = df.sort_values(by="Mês", ascending=False).iloc[0]
    lider_turno = df.sort_values(by="Turno", ascending=False).iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🥇 LÍDER GERAL", f"{lider_geral['Time']}", f"{lider_geral['Total']} pts")
    k2.metric("🚀 MITO DA RODADA", f"{mito_rodada['Time']}", f"{mito_rodada['Última Rodada']} pts")
    k3.metric("📈 LÍDER DO MÊS", f"{lider_mes['Time']}", f"{lider_mes['Mês']} pts")
    k4.metric(f"🔥 LÍDER DO {turno_atual}º TURNO", f"{lider_turno['Time']}", f"{lider_turno['Turno']} pts")

    st.write("")

    # ABAS PRINCIPAIS
    tab1, tab2 = st.tabs(["🏆 Classificação Geral", "📊 Gráficos & Estatísticas"])

    with tab1:
        st.subheader("⚡ Tabela de Posições da Liga")
        st.dataframe(
            df[["Posição", "Time", "Cartoleiro", "Total", "Última Rodada", "Mês", "Turno", "Dif. p/ Rival", "Dif. p/ Líder"]],
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.subheader("🎯 Desempenho da Última Rodada")
        st.caption("Rendimento isolado de cada cartoleiro na rodada mais recente.")
        
        df_rodada_sorted = df.sort_values(by="Última Rodada", ascending=True)
        st.bar_chart(
            df_rodada_sorted,
            x="Time",
            y="Última Rodada",
            color="Time",
            use_container_width=True
        )

        st.divider()

        st.subheader("🔥 Pontuação Total Acumulada")
        st.caption("Visão geral do volume total de pontos acumulados.")
        
        st.bar_chart(
            df.sort_values(by="Total", ascending=True),
            x="Time",
            y="Total",
            use_container_width=True
        )

    st.divider()
    st.caption(f"⚡ Black Guys League | Rodada {rodada_atual} • {turno_atual}º Turno | Conectado à API do Cartola FC.")