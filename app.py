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

# 2. Estilização Cyberpunk Neon (Baseada na Logo Oficial + Letreiro)
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

    /* ESTILO DO LETREIRO (MARQUEE) NEON */
    .ticker-container {
        width: 100%;
        background: rgba(10, 8, 19, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.3);
        overflow: hidden;
        white-space: nowrap;
        padding: 8px 0;
        margin-bottom: 20px;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 30s linear infinite;
        font-family: 'Rajdhani', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #00f2ff;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
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

    /* Card de Vencedor do Mês */
    .card-vencedor {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid #eab308;
        box-shadow: 0 0 15px rgba(234, 179, 8, 0.25);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        text-align: center;
    }

    hr {
        border-color: rgba(0, 242, 255, 0.3) !important;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Função de Carregamento de Dados da Liga
@st.cache_data(ttl=60)
def carregar_dados_liga():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
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

    # Carrega o CSV base principal
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
        return pd.DataFrame(), rodada_cartola, status_mercado

    lista_times = []
    
    for _, row in df_base.iterrows():
        nome_time = str(row["Time"]).strip()
        cartoleiro = str(row["Cartoleiro"]).strip()
        pontos_base_historico = float(row["Total"])
        
        time_id = row.get("ID", None)
        if pd.notna(time_id):
            try:
                time_id = int(time_id)
            except:
                time_id = None
        else:
            time_id = None

        pt_rodada = 0.0
        
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
    
    return df, rodada_cartola, status_mercado

# 4. Função para carregar os jogos reais do Campeonato Brasileiro
@st.cache_data(ttl=120)
def carregar_partidas_br(num_rodada):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        res = requests.get(f"https://api.cartola.globo.com/partidas/{num_rodada}", headers=headers, timeout=5)
        if res.status_code == 200:
            dados = res.json()
            partidas = dados.get("partidas", [])
            clubes = dados.get("clubes", {})
            
            jogos_formatados = []
            for p in partidas:
                id_casa = str(p.get("clube_casa_id"))
                id_vis = str(p.get("clube_visitante_id"))
                
                nome_casa = clubes.get(id_casa, {}).get("nome", "Mandante").upper()
                nome_vis = clubes.get(id_vis, {}).get("nome", "Visitante").upper()
                
                placar_casa = p.get("placar_oficial_mandante")
                placar_vis = p.get("placar_oficial_visitante")
                
                if placar_casa is not None and placar_vis is not None:
                    jogos_formatados.append(f"{nome_casa} {placar_casa} x {placar_vis} {nome_vis}")
                else:
                    jogos_formatados.append(f"{nome_casa} x {nome_vis} (A JOGAR)")
            
            return " • ".join(jogos_formatados)
    except:
        pass
    return "RESULTADOS DO BRASILEIRÃO EM ATUALIZAÇÃO"

# 5. Função para carregar a base de vencedores do mês
@st.cache_data(ttl=60)
def carregar_base_vencedores():
    if os.path.exists("base_vencedores.csv"):
        try:
            df_v = pd.read_csv("base_vencedores.csv", sep=None, engine='python', encoding='utf-8-sig')
            df_v.columns = df_v.columns.str.strip()
            return df_v
        except:
            return None
    return None

# Busca os dados
df, rodada_atual, status_mercado = carregar_dados_liga()
df_vencedores = carregar_base_vencedores()
jogos_brasileirao = carregar_partidas_br(rodada_atual)

# --- 6. LETREIRO DE NOTÍCIAS / RESULTADOS REAIS DO BRASILEIRÃO ---
texto_ticker = f"⚽ PLACARES DA {rodada_atual}ª RODADA DO BRASILEIRÃO: {jogos_brasileirao} • ⚔️ BLACK GUYS LEAGUE TEMPORADA 2026"

st.markdown(f"""
    <div class="ticker-container">
        <div class="ticker-text">{texto_ticker}</div>
    </div>
""", unsafe_allow_html=True)

# --- 7. CABEÇALHO & LOGO ---
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

# --- 8. VISUALIZAÇÃO E TABELAS ---
if not df.empty:
    # KPI METRIC CARDS
    lider_geral = df.iloc[0]
    mito_rodada = df.sort_values(by="Última Rodada", ascending=False).iloc[0]

    k1, k2 = st.columns(2)
    k1.metric("🥇 LÍDER GERAL", f"{lider_geral['Time']}", f"{lider_geral['Total']} pts")
    k2.metric("🚀 MITO DA RODADA", f"{mito_rodada['Time']}", f"{mito_rodada['Última Rodada']} pts")

    st.write("")

    # ABAS
    tab1, tab2, tab3 = st.tabs(["🏆 Classificação Geral", "🥇 Campeões do Mês", "📊 Gráficos & Estatísticas"])

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
        st.subheader("👑 Galeria de Campeões Mensais")
        st.caption("Premiações e mitações mês a mês na Black Guys League.")
        
        if df_vencedores is not None and not df_vencedores.empty:
            # Tabela resumida
            st.dataframe(df_vencedores, use_container_width=True, hide_index=True)
            
            st.write("")
            st.divider()
            
            # Cards em colunas para dar visual moderno
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
