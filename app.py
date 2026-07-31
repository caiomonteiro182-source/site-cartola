import streamlit as st
import pandas as pd
import requests
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
    }

    /* Estilização das Abas */
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

    hr {
        border-color: rgba(0, 242, 255, 0.3) !important;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Função de Carregamento de Dados (100% Precisa)
@st.cache_data(ttl=60)
def carregar_dados_liga():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # Busca status do mercado no Cartola FC
    # status_mercado = 1 (Mercado Aberto)
    # status_mercado = 2 (Mercado Fechado / Rodada ao vivo)
    rodada_cartola = 20
    status_mercado = 1 
    try:
        res_m = requests.get("https://api.cartola.globo.com/mercado/status", headers=headers, timeout=5)
        if res_m.status_code == 200:
            dados_m = res_m.json()
            rodada_cartola = dados_m.get("rodada_atual", 20)
            status_mercado = dados_m.get("status_mercado", 1)
    except:
        pass

    # Carrega o CSV base
    df_base = None
    for csv_file in ["base_cartola_oficial.csv", "base_cartola.csv"]:
        if os.path.exists(csv_file):
            try:
                df_base = pd.read_csv(csv_file, sep=None, engine='python', encoding='utf-8-sig')
                df_base.columns = df_base.columns.str.strip()
                break
            except:
                pass

    if df_base is None:
        st.error("⚠️ O arquivo CSV de base ('base_cartola_oficial.csv') não foi encontrado no GitHub!")
        return pd.DataFrame(), rodada_cartola

    lista_times = []
    
    for _, row in df_base.iterrows():
        nome_time = str(row["Time"]).strip()
        cartoleiro = str(row["Cartoleiro"]).strip()
        
        # O valor do CSV 'Total' é a base soberana consolidada
        pontos_base_historico = float(row["Total"])
        
        # Leitura da coluna ID
        time_id = row.get("ID", None)
        if pd.notna(time_id):
            try:
                time_id = int(time_id)
            except:
                time_id = None
        else:
            time_id = None

        pt_rodada = 0.0
        
        # Consulta ao vivo via ID na API do Cartola
        if time_id:
            try:
                res_p = requests.get(f"https://api.cartola.globo.com/time/id/{time_id}", headers=headers, timeout=5)
                if res_p.status_code == 200:
                    dados = res_p.json()
                    p_raw = dados.get("pontos", 0)
                    if isinstance(p_raw, dict):
                        pt_rodada = float(p_raw.get("rodada", 0))
                    elif isinstance(p_raw, (int, float)):
                        pt_rodada = float(p_raw)
            except:
                pass
        
        # O Total do CSV reflete exatamente o estado atual.
        # Só soma a pontuação temporária se a rodada estiver acontecendo AO VIVO (status_mercado == 2)
        if status_mercado == 2:
            total_acumulado = pontos_base_historico + pt_rodada
        else:
            total_acumulado = pontos_base_historico
        
        lista_times.append({
            "Time": nome_time,
            "Cartoleiro": cartoleiro,
            "Total": round(total_acumulado, 2),
            "Última Rodada": round(pt_rodada, 2)
        })

    df = pd.DataFrame(lista_times)
    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
    df["Posição"] = df.index + 1
    
    top_score = df.iloc[0]["Total"]
    df["Dif. p/ Rival"] = (df["Total"].shift(1) - df["Total"]).round(2).fillna(0)
    df["Dif. p/ Líder"] = (top_score - df["Total"]).round(2)
    
    return df, rodada_cartola

# --- 4. CABEÇALHO & LOGO ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
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

# Botão de Atualização Manual
col_status, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("🔄 Atualizar Ao Vivo"):
        st.cache_data.clear()
        st.rerun()

with st.spinner("⚡ Conectando ao Cartola FC e sincronizando pontos ao vivo..."):
    df, rodada_atual = carregar_dados_liga()

# --- 5. VISUALIZAÇÃO E TABELAS ---
if not df.empty:
    # KPI METRIC CARDS
    lider_geral = df.iloc[0]
    mito_rodada = df.sort_values(by="Última Rodada", ascending=False).iloc[0]

    k1, k2 = st.columns(2)
    k1.metric("🥇 LÍDER GERAL", f"{lider_geral['Time']}", f"{lider_geral['Total']} pts")
    k2.metric("🚀 MITO DA RODADA", f"{mito_rodada['Time']}", f"{mito_rodada['Última Rodada']} pts")

    st.write("")

    # ABAS
    tab1, tab2 = st.tabs(["🏆 Classificação Geral", "📊 Gráficos & Estatísticas"])

    with tab1:
        st.subheader("⚡ Tabela de Posições da Liga")
        
        # Seleção entre Geral x Última Rodada
        visao = st.radio(
            "Selecione a visualização:",
            ["Classificação Geral (Total Acumulado)", "Pontuação da Última Rodada"],
            horizontal=True
        )
        
        st.write("")
        
        if visao == "Classificação Geral (Total Acumulado)":
            st.dataframe(
                df[["Posição", "Time", "Cartoleiro", "Total", "Última Rodada", "Dif. p/ Rival", "Dif. p/ Líder"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            df_rodada = df.sort_values(by="Última Rodada", ascending=False).reset_index(drop=True)
            df_rodada["Pos. Rodada"] = df_rodada.index + 1
            st.dataframe(
                df_rodada[["Pos. Rodada", "Time", "Cartoleiro", "Última Rodada", "Total"]],
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
        st.caption("Visão geral do volume total de pontos acumulados no campeonato.")
        
        st.bar_chart(
            df.sort_values(by="Total", ascending=True),
            x="Time",
            y="Total",
            use_container_width=True
        )

    st.divider()
    st.caption(f"⚡ Black Guys League | Rodada {rodada_atual} | Sincronizado automaticamente via API Cartola FC.")
