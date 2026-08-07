import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(
    page_title="Black Guys League - Cartola FC",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização Cyberpunk Neon + Banner do Mercado Embutido
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
        display: inline-block;
    }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.4);
        font-weight: 700;
    }

    /* CONTÊINER ALINHADO PARA O TÍTULO + TEMPORIZADOR */
    .header-title-container {
        display: flex;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap;
    }

    /* ESTILO DO BANNER CONTADOR AO LADO DO TÍTULO */
    .market-timer-inline-open {
        background: #ccff00;
        color: #0a0813;
        font-family: 'Teko', sans-serif;
        font-size: 22px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 4px 14px;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(204, 255, 0, 0.6);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .market-timer-inline-closed {
        background: #ef4444;
        color: #ffffff;
        font-family: 'Teko', sans-serif;
        font-size: 22px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 4px 14px;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.5);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Estilo do Link Oficial da Liga */
    .link-liga {
        display: inline-block;
        color: #00f2ff !important;
        font-weight: 700;
        font-size: 15px;
        text-decoration: none;
        letter-spacing: 1px;
        margin-top: 4px;
        padding: 4px 12px;
        background: rgba(0, 242, 255, 0.08);
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    .link-liga:hover {
        background: rgba(0, 242, 255, 0.25);
        border-color: #00f2ff;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.6);
        color: #ffffff !important;
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

    /* CARD ESTILO PAINEL DE TIME */
    .box-m1 {
        background: rgba(10, 8, 19, 0.85);
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #00f2ff;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }

    .box-m2 {
        background: rgba(10, 8, 19, 0.85);
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #22c55e;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.2);
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
        font-size: 46px;
        font-weight: bold;
        color: #ffffff;
        line-height: 1;
        margin-right: 10px;
    }

    .txt-up {
        color: #22c55e !important;
        font-size: 24px;
        font-weight: bold;
    }

    .txt-down {
        color: #ef4444 !important;
        font-size: 24px;
        font-weight: bold;
    }

    /* Cartões de Métricas (KPIs) Neons */
    div[data-testid="stMetric"] {
        background: rgba(18, 12, 38, 0.75);
        border: 2px solid #a855f7;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.35), inset 0 0 10px rgba(0, 242, 255, 0.1);
        padding: 16px;
        border-radius: 14px;
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

    .card-vencedor {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid #eab308;
        box-shadow: 0 0 15px rgba(234, 179, 8, 0.25);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        text-align: center;
    }

    .card-dica {
        background: rgba(18, 12, 38, 0.7);
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
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

# 3. Função de Carregamento Ultra-Rápido
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
    except:
        pass

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
        return pd.DataFrame(), rodada_cartola, status_mercado, info_fechamento

    atletas_ao_vivo = {}
    if status_mercado == 2:
        try:
            res_av = session.get("https://api.cartola.globo.com/atleta/pontuados", timeout=4)
            if res_av.status_code == 200:
                atletas_ao_vivo = res_av.json().get("atletas", {})
        except:
            pass

    lista_times = []
    rodada_penultima = rodada_cartola - 1 if status_mercado == 2 else rodada_cartola - 2
    rodada_ultima_consolidada = rodada_cartola - 1 if status_mercado == 1 else rodada_cartola
    
    for _, row in df_base.iterrows():
        nome_time = str(row["Time"]).strip()
        cartoleiro = str(row["Cartoleiro"]).strip()
        pontos_base_historico = float(row["Total"])
        
        time_id = row.get("ID", None)
        try:
            time_id = int(time_id) if pd.notna(time_id) else None
        except:
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
                        p_raw = dados.get("pontos", 0)
                        if isinstance(p_raw, dict):
                            pt_rodada = float(p_raw.get("rodada", 0))
                        elif isinstance(p_raw, (int, float)):
                            pt_rodada = float(p_raw)
                        
                        val_api = dados.get("valorizacao", 0.0)
                        if val_api is not None and float(val_api) != 0.0:
                            valorizacao_rodada = float(val_api)

                if valorizacao_rodada == 0.0 and rodada_ultima_consolidada >= 1:
                    res_at = session.get(f"https://api.cartola.globo.com/time/id/{time_id}/{rodada_ultima_consolidada}", timeout=3)
                    if res_at.status_code == 200:
                        dados_at = res_at.json()
                        atletas = dados_at.get("atletas", [])
                        if atletas:
                            valorizacao_rodada = sum([float(a.get("variacao_num", 0.0)) for a in atletas])

                if rodada_penultima >= 1:
                    res_ant = session.get(f"https://api.cartola.globo.com/time/id/{time_id}/{rodada_penultima}", timeout=3)
                    if res_ant.status_code == 200:
                        pt_rodada_anterior = float(res_ant.json().get("pontos", 0.0))
            except:
                pass
        
        if status_mercado == 2:
            total_acumulado = pontos_base_historico + pt_rodada
        else:
            total_acumulado = pontos_base_historico
        
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
    df = df.sort_values(by="Total Acumulado", ascending=False).reset_index(drop=True)
    df["Posição Geral"] = df.index + 1
    
    top_score = df.iloc[0]["Total Acumulado"]
    df["Dif. p/ Rival"] = (df["Total Acumulado"].shift(1) - df["Total Acumulado"]).round(2).fillna(0)
    df["Dif. p/ Líder"] = (top_score - df["Total Acumulado"]).round(2)
    
    return df, rodada_cartola, status_mercado, info_fechamento

# 4. Função para calcular a tag embutida do tempo do mercado (Apenas Horas e Minutos)
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
    except:
        return '<span class="market-timer-inline-open">⏱️ MERCADO ABERTO</span>'

# 5. Função para carregar os jogos reais do Campeonato Brasileiro
@st.cache_data(ttl=120)
def carregar_partidas_br(num_rodada):
    try:
        res = requests.get(f"https://api.cartola.globo.com/partidas/{num_rodada}", headers=HEADERS, timeout=4)
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

# 6. Função para carregar a base de vencedores do mês
@st.cache_data(ttl=120)
def carregar_base_vencedores():
    if os.path.exists("base_vencedores.csv"):
        try:
            df_v = pd.read_csv("base_vencedores.csv", sep=None, engine='python', encoding='utf-8-sig')
            df_v.columns = df_v.columns.str.strip()
            return df_v
        except:
            return None
    return None

# Carregamento dos dados
df, rodada_atual, status_mercado, info_fechamento = carregar_dados_liga()
df_vencedores = carregar_base_vencedores()
jogos_brasileirao = carregar_partidas_br(rodada_atual)

# --- 7. LETREIRO NEON (Ícone alterado para Bola de Futebol ⚽) ---
status_tag = "🔴 AO VIVO" if status_mercado == 2 else "🟢 MERCADO ABERTO"
texto_ticker = f"⚽ BRASILEIRÃO {rodada_atual}ª RODADA [{status_tag}]: {jogos_brasileirao} • ⚽ BLACK GUYS LEAGUE"

st.markdown(f'<div class="ticker-container"><div class="ticker-text">{texto_ticker}</div></div>', unsafe_allow_html=True)

# --- 8. CABEÇALHO, LOGO, TÍTULO + TEMPORIZADOR NA FRENTE ---
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
        st.title("⚽")

with col_title:
    badge_timer = gerar_badge_mercado(info_fechamento, status_mercado)
    
    st.markdown(f"""
        <div class="header-title-container">
            <h1>BLACK GUYS LEAGUE</h1>
            {badge_timer}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #c084fc; margin-top: -10px; margin-bottom: 2px;'>TEMPORADA 2026 • PORTAL OFICIAL DE PERFORMANCE</h4>", unsafe_allow_html=True)
    st.markdown('<a href="https://cartola.globo.com/#!/competicoes/classica/blackguys-league" target="_blank" rel="noopener noreferrer" class="link-liga">🔗 Acessar Liga Oficial no Cartola FC</a>', unsafe_allow_html=True)

st.divider()

# Botão de Atualização Manual
col_status, col_btn = st.columns([4, 1])
with col_status:
    if status_mercado == 2:
        st.markdown("<h5 style='color: #ef4444; margin: 0;'>🔴 Jogos em andamento! Dados sincronizados em tempo real.</h5>", unsafe_allow_html=True)

with col_btn:
    if st.button("🔄 Atualizar Ao Vivo"):
        st.cache_data.clear()
        st.rerun()

# --- 9. CARD DETALHADO INSTANTÂNEO ---
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
            f'<div style="margin-top:10px; font-size:14px; color:#94a3b8;">'
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
            f'<div style="margin-top:10px; font-size:14px; color:#94a3b8;">'
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
