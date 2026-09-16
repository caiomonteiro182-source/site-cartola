import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import random
import re
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS RESPONSIVOS MOBILE
# ==========================================
st.set_page_config(
    page_title="Black Guys League - Cartola FC",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def carregar_logo_base64():
  for ext in ["logo.png", "logo.jpg", "logo.jpeg"]:
    if os.path.exists(ext):
      with open(ext, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
  return ""


URL_BASE64_LOGO = carregar_logo_base64()

st.markdown(
    """
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
        gap: 20px;
        margin-bottom: 15px;
        background: rgba(15, 12, 29, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        flex-wrap: wrap;
    }

    .header-logo-img {
        width: 120px;
        height: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.5));
    }

    .header-col-wrapper {
        flex: 1;
        min-width: 250px;
    }

    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(22px, 6vw, 44px) !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2ff 0%, #7c3aed 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
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
        gap: 12px;
        flex-wrap: wrap;
    }

    .market-timer-inline-open, .market-timer-inline-alert, .market-timer-inline-closed {
        font-family: 'Orbitron', sans-serif;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 6px 12px;
        border-radius: 30px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
    }

    .market-timer-inline-open {
        background: linear-gradient(135deg, #a3e635 0%, #65a30d 100%);
        color: #020617;
        box-shadow: 0 0 12px rgba(163, 230, 53, 0.5);
    }

    .market-timer-inline-alert {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: #ffffff;
        box-shadow: 0 0 15px rgba(249, 115, 22, 0.7);
    }

    .market-timer-inline-closed {
        background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%);
        color: #ffffff;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.5);
    }

    .subtitle-header {
        color: #c084fc;
        font-weight: 700;
        margin-top: 4px;
        margin-bottom: 8px;
        font-size: 13px;
        letter-spacing: 0.5px;
    }

    .link-liga {
        display: inline-block;
        color: #00f2ff !important;
        font-weight: 700;
        font-size: 12px;
        text-decoration: none;
        letter-spacing: 0.5px;
        padding: 6px 12px;
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 8px;
    }

    .matches-panel-container {
        width: 100%;
        background: rgba(10, 8, 22, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 18px;
    }

    .matches-panel-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #00f2ff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .matches-grid {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        padding-bottom: 8px;
        -webkit-overflow-scrolling: touch;
    }

    .match-card {
        flex: 0 0 auto;
        background: rgba(21, 16, 43, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 10px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        min-width: 140px;
    }

    .match-card img {
        width: 32px !important;
        height: 32px !important;
        object-fit: contain !important;
    }

    .match-score {
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
        font-weight: 900;
        color: #ffffff;
    }

    .box-m1, .box-m2 {
        background: rgba(13, 10, 28, 0.85);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .box-m1 { border-left: 5px solid #00f2ff; }
    .box-m2 { border-left: 5px solid #10b981; }

    .lbl-title {
        font-size: 11px;
        font-weight: bold;
        color: #94a3b8;
        text-transform: uppercase;
    }

    .val-num {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin-right: 8px;
    }

    .txt-up { color: #10b981 !important; font-size: 18px; font-weight: bold; }
    .txt-down { color: #f43f5e !important; font-size: 18px; font-weight: bold; }

    div[data-testid="stMetric"] {
        background: rgba(21, 16, 43, 0.7);
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 10px 14px;
        border-radius: 12px;
    }

    button[data-baseweb="tab"] {
        background-color: rgba(15, 12, 29, 0.5) !important;
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        padding: 8px 12px !important;
    }

    button[aria-selected="true"] {
        background: linear-gradient(180deg, rgba(124, 58, 237, 0.3) 0%, rgba(0, 242, 255, 0.08) 100%) !important;
        color: #00f2ff !important;
        border-bottom: 3px solid #00f2ff !important;
    }

    @media (max-width: 768px) {
        .header-main-flex {
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 15px 10px;
            gap: 12px;
        }

        .header-logo-img {
            width: 90px;
        }

        .header-title-container {
            justify-content: center;
        }

        .val-num {
            font-size: 26px;
        }

        .fut-card-container {
            width: 100% !important;
            max-width: 280px;
            height: auto !important;
            padding: 20px 10px !important;
        }
    }

    .card-scout-player {
        background: rgba(13, 10, 28, 0.85);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
    }

    .fut-card-container {
        width: 250px;
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 50%, #030206 100%);
        border: 3px solid #eab308;
        border-radius: 18px;
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.3);
        padding: 16px;
        text-align: center;
        margin: 10px auto;
    }

    .fut-card-badge {
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        color: #eab308;
        letter-spacing: 1.5px;
    }

    .fut-card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        font-weight: 900;
        color: #ffffff;
        margin-top: 10px;
    }

    .fut-card-score {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        font-weight: 900;
        color: #00f2ff;
        line-height: 1;
        margin: 10px 0;
    }

    .fut-card-sub {
        color: #c084fc;
        font-weight: 700;
        font-size: 13px;
    }

    hr {
        border-color: rgba(0, 242, 255, 0.2) !important;
        margin: 14px 0 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


# ==========================================
# 2. SISTEMA DA BLACK GUYS LEAGUE
# ==========================================
def processar_dados_time(args):
  (
      row,
      rodada_ultima_consolidada,
      rodada_penultima,
      status_mercado,
      atletas_ao_vivo,
  ) = args
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
      res_p = session.get(
          f"https://api.cartola.globo.com/time/id/{time_id}", timeout=2.5
      )
      if res_p.status_code == 200:
        patrimonio = float(res_p.json().get("patrimonio", 100.0))

      soma_historico_rodadas = 0.0
      for r in range(1, rodada_ultima_consolidada + 1):
        res_r = session.get(
            f"https://api.cartola.globo.com/time/id/{time_id}/{r}", timeout=2.5
        )
        if res_r.status_code == 200:
          pts_r = float(res_r.json().get("pontos", 0.0))
          soma_historico_rodadas += pts_r

          if r == rodada_ultima_consolidada:
            pt_rodada = pts_r
            atletas_uc = res_r.json().get("atletas", [])
            if atletas_uc and status_mercado == 1:
              valorizacao_rodada = sum(
                  [float(a.get("variacao_num", 0.0)) for a in atletas_uc]
              )

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
      "Valorização (C$)": round(valorizacao_rodada, 2),
  }


@st.cache_data(ttl=120)
def carregar_dados_liga():
  session = requests.Session()
  session.headers.update(HEADERS)

  rodada_cartola = 20
  status_mercado = 1
  info_fechamento = None

  try:
    res_m = session.get(
        "https://api.cartola.globo.com/mercado/status", timeout=4
    )
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
        df_base = pd.read_csv(
            csv_file, sep=None, engine="python", encoding="utf-8-sig"
        )
        df_base.columns = df_base.columns.str.strip()
        break
      except Exception:
        pass

  if df_base is None:
    st.error(
        "⚠️ O arquivo CSV de base ('base_cartola_oficial.csv') não foi"
        " encontrado!"
    )
    return pd.DataFrame(), rodada_cartola, status_mercado, info_fechamento

  atletas_ao_vivo = {}
  if status_mercado == 2:
    try:
      res_av = session.get(
          "https://api.cartola.globo.com/atleta/pontuados", timeout=4
      )
      if res_av.status_code == 200:
        atletas_ao_vivo = res_av.json().get("atletas", {})
    except Exception:
      pass

  rodada_ultima_consolidada = (
      rodada_cartola - 1 if status_mercado == 1 else rodada_cartola
  )
  rodada_penultima = rodada_ultima_consolidada - 1

  tasks = [
      (
          row,
          rodada_ultima_consolidada,
          rodada_penultima,
          status_mercado,
          atletas_ao_vivo,
      )
      for _, row in df_base.iterrows()
  ]

  with ThreadPoolExecutor(max_workers=20) as executor:
    lista_times = list(executor.map(processar_dados_time, tasks))

  df = pd.DataFrame(lista_times)

  if not df.empty:
    df = df.sort_values(by="Total Acumulado", ascending=False).reset_index(
        drop=True
    )
    df["Posição Geral"] = df.index + 1

    top_score = df.iloc[0]["Total Acumulado"]
    df["Dif. p/ Rival"] = (
        (df["Total Acumulado"].shift(1) - df["Total Acumulado"])
        .round(2)
        .fillna(0)
    )
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
    return (
        '<span class="market-timer-inline-closed">🔒 MERCADO FECHADO</span>'
    )

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
      return (
          '<span class="market-timer-inline-closed">🔒 MERCADO FECHADO</span>'
      )

    total_horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60

    if total_horas > 0:
      texto_tempo = f"FECHA EM {total_horas}H {minutos:02d}MIN"
      return f'<span class="market-timer-inline-open">⏱️ {texto_tempo}</span>'
    else:
      texto_tempo = f"FECHA EM {minutos} MIN!"
      return (
          f'<span class="market-timer-inline-alert">⚠️ {texto_tempo}</span>'
      )
  except Exception:
    return '<span class="market-timer-inline-open">⏱️ MERCADO ABERTO</span>'


@st.cache_data(ttl=120)
def carregar_partidas_com_escudos(num_rodada):
  try:
    res = requests.get(
        f"https://api.cartola.globo.com/partidas/{num_rodada}",
        headers=HEADERS,
        timeout=4,
    )
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

        escudo_casa = (
            escudos_casa.get("60x60") or escudos_casa.get("30x30") or ""
        )
        escudo_vis = escudos_vis.get("60x60") or escudos_vis.get("30x30") or ""

        jogos.append({
            "escudo_casa": escudo_casa,
            "escudo_vis": escudo_vis,
            "nome_casa": nome_casa,
            "nome_vis": nome_vis,
            "placar_casa": p.get("placar_oficial_mandante"),
            "placar_vis": p.get("placar_oficial_visitante"),
        })
      return jogos
  except Exception:
    pass
  return []


@st.cache_data(ttl=120)
def carregar_base_vencedores():
  if os.path.exists("base_vencedores.csv"):
    try:
      df_v = pd.read_csv(
          "base_vencedores.csv", sep=None, engine="python", encoding="utf-8-sig"
      )
      df_v.columns = df_v.columns.str.strip()
      return df_v
    except Exception:
      return None
  return None


# ==========================================
# 3. SCOUT LAB COM MÍNIMO PARA VALORIZAR & ESTIMATIVA DE CARTOLETAS
# ==========================================
@st.cache_data(ttl=300)
def carregar_dados_completos_scout():
  try:
    res_m = requests.get(
        "https://api.cartola.globo.com/atletas/mercado",
        headers=HEADERS,
        timeout=5,
    )
    res_c = requests.get(
        "https://api.cartola.globo.com/clubes", headers=HEADERS, timeout=5
    )
    res_s = requests.get(
        "https://api.cartola.globo.com/mercado/status", timeout=5
    )

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

      diferenca_pts = projecao - mpv
      variacao_estimada = round(diferenca_pts * 0.30, 2)

      status_str = (
          "Confirmado"
          if status_id == 7
          else (
              "Em dúvida"
              if status_id == 2
              else ("Nulo/Outro" if status_id == 6 else "Fora")
          )
      )

      nome_atleta = a.get("apelido", "Atleta")
      pos_str = posicoes.get(a.get("posicao_id"), "MEI")

      lista_final.append({
          "atleta_id": a.get("atleta_id"),
          "jogador": nome_atleta,
          "time": clube_nome,
          "posicao": pos_str,
          "preco": preco,
          "media": media,
          "min_valorizar": mpv,
          "projecao": round(projecao, 2),
          "variacao_est": variacao_estimada,
          "score": round(score, 2),
          "status_id": status_id,
          "status": status_str,
          "nome_busca": f"{nome_atleta} ({clube_nome} - {pos_str})",
      })

    return pd.DataFrame(lista_final), status.get("rodada_atual", 1)
  except Exception:
    return pd.DataFrame(), 1


# ==========================================
# 4. CARREGAMENTO RÁPIDO VIA SESSION STATE
# ==========================================
if "df_liga_cached" not in st.session_state:
  with st.spinner("⚡ Sincronizando dados da liga..."):
    df, rodada_atual, status_mercado, info_fechamento = carregar_dados_liga()
    st.session_state["df_liga_cached"] = df
    st.session_state["rodada_atual_cached"] = rodada_atual
    st.session_state["status_mercado_cached"] = status_mercado
    st.session_state["info_fechamento_cached"] = info_fechamento

df = st.session_state["df_liga_cached"]
rodada_atual = st.session_state["rodada_atual_cached"]
status_mercado = st.session_state["status_mercado_cached"]
info_fechamento = st.session_state["info_fechamento_cached"]

df_vencedores = carregar_base_vencedores()
lista_partidas = carregar_partidas_com_escudos(rodada_atual)

# ==========================================
# 5. CABEÇALHO E JOGOS
# ==========================================
status_tag = "🔴 JOGOS AO VIVO" if status_mercado == 2 else "🟢 PRÓXIMA RODADA"

if lista_partidas:
  cards_html_list = []
  for j in lista_partidas:
    placar_str = (
        f'<div class="match-score">{j["placar_casa"]} x {j["placar_vis"]}</div>'
        if j["placar_casa"] is not None
        else '<div class="match-score">VS</div>'
    )
    card_item = (
        f'<div class="match-card"><img src="{j["escudo_casa"]}"'
        f' title="{j["nome_casa"]}">{placar_str}<img src="{j["escudo_vis"]}"'
        f' title="{j["nome_vis"]}"></div>'
    )
    cards_html_list.append(card_item)

  st.markdown(
      f"""
        <div class="matches-panel-container">
            <div class="matches-panel-header">⚽ BRASILEIRÃO {rodada_atual}ª RODADA [{status_tag}]</div>
            <div class="matches-grid">{"".join(cards_html_list)}</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

badge_timer = gerar_badge_mercado(info_fechamento, status_mercado)
img_logo_html = (
    f'<img src="{URL_BASE64_LOGO}" class="header-logo-img" alt="Logo">'
    if URL_BASE64_LOGO
    else ""
)

st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

st.divider()

col_status, col_btn = st.columns([3, 1])
with col_status:
  if status_mercado == 2:
    st.markdown(
        "<h5 style='color: #ef4444; margin: 0;'>🔴 Jogos em andamento!"
        " Classificação AO VIVO calculada.</h5>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        "<h5 style='color: #22c55e; margin: 0;'>⚡ Dados armazenados em cache"
        " local ultra-rápido.</h5>",
        unsafe_allow_html=True,
    )

with col_btn:
  if st.button("🔄 FORÇAR RECARGA / ATUALIZAR", use_container_width=True):
    st.cache_data.clear()
    if "df_liga_cached" in st.session_state:
      del st.session_state["df_liga_cached"]
    st.rerun()

# ==========================================
# 6. PAINEL INDIVIDUAL & METRICAS
# ==========================================
if not df.empty:
  st.subheader("🔍 Painel Individual do Time")
  time_selecionado = st.selectbox(
      "Selecione um time para ver a análise completa:", df["Time"].tolist()
  )

  dados_time = df[df["Time"] == time_selecionado].iloc[0]
  media_pontos_liga = df["Pontos Ganhos (Última Rodada)"].mean()
  media_patrimonio_liga = df["Patrimônio (C$)"].mean()

  pt_atual = dados_time["Pontos Ganhos (Última Rodada)"]
  pt_ant = dados_time["Pontos Rodada Anterior"]
  diff_pontos = pt_atual - pt_ant
  html_diff_pontos = (
      f'<span class="txt-up">↑ {diff_pontos:.2f}</span>'
      if diff_pontos >= 0
      else f'<span class="txt-down">↓ {abs(diff_pontos):.2f}</span>'
  )

  val_cartoletas = dados_time["Valorização (C$)"]
  html_val_cartoletas = (
      f'<span class="txt-up">↑ {val_cartoletas:.2f}</span>'
      if val_cartoletas >= 0
      else f'<span class="txt-down">↓ {abs(val_cartoletas):.2f}</span>'
  )

  st.markdown(
      f"<h3 style='margin-bottom:0; color:#00f2ff;'>⚽"
      f" {dados_time['Time']}</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<p style='color:#c084fc; font-weight:bold; margin-bottom:15px;'>Cartoleiro:"
      f" {dados_time['Cartoleiro']} | Posição Geral:"
      f" #{dados_time['Posição Geral']}</p>",
      unsafe_allow_html=True,
  )

  c_box1, c_box2 = st.columns(2)
  with c_box1:
    st.markdown(
        '<div class="box-m1"><div class="lbl-title">⚽ ÚLTIMA PONTUAÇÃO</div><div'
        ' style="display:flex; align-items:baseline; margin-top:5px;"><span'
        f' class="val-num">{pt_atual:.2f}</span>{html_diff_pontos}</div><div'
        ' style="margin-top:8px; font-size:12px; color:#94a3b8;">MÉDIA DA LIGA:'
        f' <strong style="color:#f1f5f9;">{media_pontos_liga:.2f}'
        " pts</strong></div></div>",
        unsafe_allow_html=True,
    )

  with c_box2:
    st.markdown(
        '<div class="box-m2"><div class="lbl-title">💰 PATRIMÔNIO</div><div'
        ' style="display:flex; align-items:baseline; margin-top:5px;"><span'
        f' class="val-num">C$ {dados_time["Patrimônio (C$)"]:.2f}</span>{html_val_cartoletas}</div><div'
        ' style="margin-top:8px; font-size:12px; color:#94a3b8;">MÉDIA DA LIGA:'
        ' <strong style="color:#f1f5f9;">C$'
        f" {media_patrimonio_liga:.2f}</strong></div></div>",
        unsafe_allow_html=True,
    )

  st.divider()

  lider_geral = df.iloc[0]
  mito_rodada = df.sort_values(
      by="Pontos Ganhos (Última Rodada)", ascending=False
  ).iloc[0]
  pior_rodada = df.sort_values(
      by="Pontos Ganhos (Última Rodada)", ascending=True
  ).iloc[0]

  k1, k2, k3 = st.columns(3)
  k1.metric(
      "🥇 LÍDER GERAL",
      f"{lider_geral['Time']}",
      f"{lider_geral['Total Acumulado']} pts",
  )
  k2.metric(
      "🚀 MITO DA RODADA",
      f"{mito_rodada['Time']}",
      f"+{mito_rodada['Pontos Ganhos (Última Rodada)']} pts",
  )
  k3.metric(
      "📉 MALA CHEIA",
      f"{pior_rodada['Time']}",
      f"{pior_rodada['Pontos Ganhos (Última Rodada)']} pts",
  )

  st.write("")

  # ==========================================
  # 7. ABAS PRINCIPAIS
  # ==========================================
  tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
      "🏆 Classificação",
      "⚔️ X1",
      "🎮 Arena Interativa",
      "🥇 Campeões",
      "💰 Valorização",
      "🤖 Scout Lab",
      "🛡️ Radar SG",
      "🎴 Cards FUT",
  ])

  # --- TAB 1: CLASSIFICAÇÃO & GRÁFICOS ---
  with tab1:
    st.subheader("⚡ Tabela de Posições da Liga")
    if status_mercado == 2:
      st.info(
          "🎯 **MODO LIVE ATIVO:** Tabela considerando pontos em tempo real!"
      )

    visao = st.radio(
        "Visão:", ["Classificação Geral", "Última Rodada"], horizontal=True
    )
    st.write("")

    if visao == "Classificação Geral":
      st.dataframe(
          df[[
              "Posição Geral",
              "Conquistas",
              "Time",
              "Cartoleiro",
              "Pontos Ganhos (Última Rodada)",
              "Total Acumulado",
              "Dif. p/ Rival",
              "Dif. p/ Líder",
          ]],
          column_config={
              "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn(
                  "Ganho (pts)", format="%.2f"
              ),
              "Total Acumulado": st.column_config.NumberColumn(
                  "Total (pts)", format="%.2f"
              ),
          },
          use_container_width=True,
          hide_index=True,
      )
    else:
      df_rodada = df.sort_values(
          by="Pontos Ganhos (Última Rodada)", ascending=False
      ).reset_index(drop=True)
      df_rodada["Pos. Rodada"] = df_rodada.index + 1
      st.dataframe(
          df_rodada[[
              "Pos. Rodada",
              "Conquistas",
              "Time",
              "Cartoleiro",
              "Pontos Ganhos (Última Rodada)",
              "Total Acumulado",
          ]],
          column_config={
              "Pontos Ganhos (Última Rodada)": st.column_config.NumberColumn(
                  "Ganho na Rodada", format="+%.2f"
              )
          },
          use_container_width=True,
          hide_index=True,
      )

    st.divider()

    st.markdown("### 🔥 Destaque de Sequência")
    c_hot1, c_hot2 = st.columns(2)
    df_subida = df.sort_values(
        by="Pontos Rodada Anterior", ascending=False
    )
    maior_subida = df_subida.iloc[0] if not df_subida.empty else df.iloc[0]

    with c_hot1:
      st.markdown(
          f"""
                <div style="background: rgba(124, 58, 237, 0.15); border: 1px solid #7c3aed; border-radius: 12px; padding: 12px;">
                    <h5 style="color: #c084fc; margin:0; font-size:12px;">🚀 MAIOR EVOLUÇÃO</h5>
                    <h3 style="color: #ffffff; margin-top:4px; font-size:18px;">{maior_subida['Time']}</h3>
                    <p style="margin:0; font-size:12px; color:#94a3b8;">Mantido com <strong>{maior_subida['Pontos Rodada Anterior']} pts</strong> anterior.</p>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with c_hot2:
      st.markdown(
          f"""
                <div style="background: rgba(0, 242, 255, 0.15); border: 1px solid #00f2ff; border-radius: 12px; padding: 12px;">
                    <h5 style="color: #00f2ff; margin:0; font-size:12px;">💰 MAIOR PATRIMÔNIO</h5>
                    <h3 style="color: #ffffff; margin-top:4px; font-size:18px;">{df.sort_values(by="Patrimônio (C$)", ascending=False).iloc[0]['Time']}</h3>
                    <p style="margin:0; font-size:12px; color:#94a3b8;">Cofre com <strong>C$ {df.sort_values(by="Patrimônio (C$)", ascending=False).iloc[0]['Patrimônio (C$)']}</strong>.</p>
                </div>
            """,
          unsafe_allow_html=True,
      )

    st.divider()

    # MATRIZ TÁTICA: PATRIMÔNIO X PONTUAÇÃO (MOBILE READY)
    st.markdown("### 🎯 Matriz Tática: Patrimônio vs. Pontuação Total")

    media_pts = df["Total Acumulado"].mean()
    media_patr = df["Patrimônio (C$)"].mean()

    def classificar_perfil(row):
      if (
          row["Total Acumulado"] >= media_pts
          and row["Patrimônio (C$)"] >= media_patr
      ):
        return "🚀 Estrategista (Equilibrado)"
      elif (
          row["Total Acumulado"] >= media_pts
          and row["Patrimônio (C$)"] < media_patr
      ):
        return "🎯 Mito Pobre (Foco em Pts)"
      elif (
          row["Total Acumulado"] < media_pts
          and row["Patrimônio (C$)"] >= media_patr
      ):
        return "💰 Tio Patinhas (Cofre Cheio)"
      else:
        return "📉 Mala Cheia (Alerta)"

    df_analise = df.copy()
    df_analise["Perfil"] = df_analise.apply(classificar_perfil, axis=1)

    fig_quadrantes = px.scatter(
        df_analise,
        x="Patrimônio (C$)",
        y="Total Acumulado",
        hover_name="Time",
        color="Perfil",
        hover_data={
            "Cartoleiro": True,
            "Posição Geral": True,
            "Pontos Ganhos (Última Rodada)": ":.2f",
            "Patrimônio (C$)": ":.2f",
            "Total Acumulado": ":.2f",
            "Perfil": False,
        },
        size=[14] * len(df_analise),
        color_discrete_map={
            "🚀 Estrategista (Equilibrado)": "#00f2ff",
            "🎯 Mito Pobre (Foco em Pts)": "#a3e635",
            "💰 Tio Patinhas (Cofre Cheio)": "#eab308",
            "📉 Mala Cheia (Alerta)": "#f43f5e",
        },
        template="plotly_dark",
    )

    fig_quadrantes.update_traces(
        marker=dict(opacity=0.9, line=dict(width=1, color="#ffffff"))
    )

    fig_quadrantes.add_vline(
        x=media_patr,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text=f"C$: {media_patr:.1f}",
        annotation_position="bottom right",
    )
    fig_quadrantes.add_hline(
        y=media_pts,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text=f"Pts: {media_pts:.1f}",
        annotation_position="top left",
    )

    fig_quadrantes.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10, 8, 22, 0.5)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            title="Patrimônio (C$)", gridcolor="rgba(255,255,255,0.05)"
        ),
        yaxis=dict(title="Pontos Totais", gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=None,
        ),
    )

    st.plotly_chart(
        fig_quadrantes,
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
    )

    st.divider()

    st.markdown("### 📊 Comparativo da Liga")
    fig_bar = px.bar(
        df.head(10),
        x="Time",
        y="Total Acumulado",
        color="Total Acumulado",
        text="Total Acumulado",
        color_continuous_scale="Purples",
        template="plotly_dark",
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

  # --- TAB 2: CONFRONTO DIRETO (X1) ---
  with tab2:
    st.subheader("⚔️ Desafio X1: Confronto Direto")
    col_x1, col_x2 = st.columns(2)
    times_lista = df["Time"].tolist()
    with col_x1:
      t1 = st.selectbox("Time 1:", times_lista, index=0)
    with col_x2:
      t2 = st.selectbox(
          "Time 2:", times_lista, index=min(1, len(times_lista) - 1)
      )

    if t1 == t2:
      st.warning("Escolha dois times diferentes!")
    else:
      d1 = df[df["Time"] == t1].iloc[0]
      d2 = df[df["Time"] == t2].iloc[0]

      st.write("")
      c_res1, c_vs, c_res2 = st.columns([2, 1, 2])
      with c_res1:
        st.markdown(
            f"<h4 style='text-align:center;'>{d1['Time']}</h4>",
            unsafe_allow_html=True,
        )
        st.metric("Total", f"{d1['Total Acumulado']} pts")
        st.metric("Patrimônio", f"C$ {d1['Patrimônio (C$)']}")

      with c_vs:
        st.markdown(
            "<h2 style='text-align:center; margin-top:20px;'>VS</h2>",
            unsafe_allow_html=True,
        )
        diff_x1 = d1["Total Acumulado"] - d2["Total Acumulado"]
        if diff_x1 > 0:
          st.success(f"**{d1['Time']}** +{diff_x1:.2f} pts!")
        elif diff_x1 < 0:
          st.success(f"**{d2['Time']}** +{abs(diff_x1):.2f} pts!")

      with c_res2:
        st.markdown(
            f"<h4 style='text-align:center;'>{d2['Time']}</h4>",
            unsafe_allow_html=True,
        )
        st.metric("Total", f"{d2['Total Acumulado']} pts")
        st.metric("Patrimônio", f"C$ {d2['Patrimônio (C$)']}")

  # --- TAB 3: ARENA INTERATIVA (NOVA CALCULADORA DE ARRANCADA INCLUÍDA) ---
  with tab3:
    st.subheader("🎮 Arena da Resenha & Ferramentas Interativas")

    # 🚀 CALCULADORA DE ARRANCADA (ULTRA-INTERATIVA POR POSIÇÃO)
    st.markdown("### 📊 Calculadora de Arrancada (Próxima Posição)")
    st.caption(
        "Descubra exatamente quantos pontos você precisa fazer por rodada para"
        " ultrapassar o adversário diretamente acima de você!"
    )

    col_calc1, col_calc2 = st.columns([1, 1])

    with col_calc1:
      time_arrancada = st.selectbox(
          "Selecione o seu Time:",
          options=df["Time"].tolist(),
          key="calc_time_user",
      )

      # Identifica a posição e os dados do time selecionado
      dados_usr = df[df["Time"] == time_arrancada].iloc[0]
      pos_atual = int(dados_usr["Posição Geral"])
      pts_usr = float(dados_usr["Total Acumulado"])

      # Slider interativo de rodadas restantes no campeonato (Padronizado até 38)
      rodadas_restantes = st.slider(
          "Rodadas Restantes no Campeonato:",
          min_value=1,
          max_value=38,
          value=max(1, 38 - rodada_atual + 1),
          step=1,
      )

    with col_calc2:
      if pos_atual == 1:
        st.markdown(
            """
                    <div style="background: rgba(163, 230, 53, 0.15); border: 1px solid #a3e635; padding: 15px; border-radius: 12px; text-align: center;">
                        <h4 style="color:#a3e635; margin:0;">🥇 VOCÊ JÁ É O LÍDER GERAL!</h4>
                        <p style="color:#94a3b8; font-size:13px; margin-top:5px;">Continue acelerando para manter a vantagem sobre o 2º colocado!</p>
                    </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        # Pega o adversário da posição imediatamente superior
        alvo_usr = df[df["Posição Geral"] == (pos_atual - 1)].iloc[0]
        nome_alvo = alvo_usr["Time"]
        pts_alvo = float(alvo_usr["Total Acumulado"])

        diferenca_pts = pts_alvo - pts_usr + 0.10  # Margem mínima de +0.10 pts
        media_necessaria = diferenca_pts / rodadas_restantes

        st.markdown(
            f"""
                    <div style="background: rgba(18, 12, 38, 0.9); border: 2px solid #00f2ff; border-radius: 12px; padding: 14px;">
                        <div style="font-size:12px; color:#c084fc; font-weight:bold;">ALVO: {pos_atual-1}º LUGAR ({nome_alvo})</div>
                        <div style="font-size:13px; color:#f8fafc; margin-top:4px;">
                            Diferença Atual: <strong>{diferenca_pts:.2f} pts</strong>
                        </div>
                        <div style="margin-top:10px; padding:10px; background:rgba(0, 242, 255, 0.1); border-radius:8px; text-align:center;">
                            <span style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Você precisa tirar por rodada:</span>
                            <div style="font-family:'Orbitron', sans-serif; font-size:26px; font-weight:900; color:#00f2ff;">
                                +{media_necessaria:.2f} pts/rodada
                            </div>
                            <span style="font-size:11px; color:#94a3b8;">considerando que {nome_alvo} pontue na média da liga.</span>
                        </div>
                    </div>
                """,
            unsafe_allow_html=True,
        )

    st.divider()

    col_game1, col_game2 = st.columns([1, 1])

    with col_game1:
      st.markdown("### 🎯 Bolão da Rodada")
      st.caption("Registre seus palpites antes do fechamento do mercado!")

      seuar_time = st.selectbox(
          "Seu Time (Quem está palpitando):",
          options=df["Time"].tolist(),
          key="bolao_user",
      )
      palpite_mito = st.selectbox(
          "Quem será o MITO da Rodada?",
          options=df["Time"].tolist(),
          key="bolao_mito",
      )
      palpite_mala = st.selectbox(
          "Quem será o MALA CHEIA?",
          options=df["Time"].tolist(),
          index=len(df) - 1,
          key="bolao_mala",
      )
      pts_lider = st.slider(
          "Quantos pontos o Líder fará?",
          min_value=30.0,
          max_value=130.0,
          value=75.0,
          step=1.0,
      )

      if st.button("🚀 Enviar Palpites Oficiais", use_container_width=True):
        st.session_state["palpite_salvo"] = {
            "usuario": seuar_time,
            "mito": palpite_mito,
            "mala": palpite_mala,
            "pts": pts_lider,
        }
        st.balloons()
        st.success("✅ Palpites registrados com sucesso no sistema!")

      if "palpite_salvo" in st.session_state:
        p = st.session_state["palpite_salvo"]
        st.markdown(
            f"""
                <div style="background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; padding: 10px; border-radius: 8px; margin-top: 10px; font-size:13px;">
                    📌 <strong>Palpite Registrado ({p['usuario']}):</strong><br>
                    • Mito: <span style="color:#00f2ff;">{p['mito']}</span><br>
                    • Mala Cheia: <span style="color:#f43f5e;">{p['mala']}</span><br>
                    • Pts Líder: <strong>{p['pts']} pts</strong>
                </div>
            """,
            unsafe_allow_html=True,
        )

    with col_game2:
      st.markdown("### ⚔️ Duelódromo da Galera")
      st.caption("Quem vence o confronto direto da rodada?")

      t_rival1 = df.iloc[0]["Time"]
      t_rival2 = df.iloc[1]["Time"] if len(df) > 1 else df.iloc[0]["Time"]

      st.markdown(f"#### 🥊 {t_rival1}  VS  {t_rival2}")

      voto = st.radio(
          "Em quem você aposta?",
          options=[t_rival1, t_rival2, "Empate Térmico"],
          horizontal=True,
      )

      if st.button("🗳️ Confirmar Voto", use_container_width=True):
        if "votos_duelo" not in st.session_state:
          st.session_state["votos_duelo"] = {
              t_rival1: 5,
              t_rival2: 3,
              "Empate Térmico": 1,
          }

        st.session_state["votos_duelo"][voto] += 1
        st.toast(f"Voto computado em {voto}!", icon="🔥")

      if "votos_duelo" in st.session_state:
        vd = st.session_state["votos_duelo"]
        tot = sum(vd.values())
        st.write("")
        st.markdown("##### 📊 Parcial da Torcida no Grupo:")
        for k, v in vd.items():
          pct = (v / tot) * 100
          st.progress(int(pct), text=f"{k}: {pct:.1f}% ({v} votos)")

    st.divider()

    # 🎰 ROLETA DO CAPITÃO (SORTEIO INTERATIVO)
    st.markdown("### 🎰 Roleta do Capitão Cego")
    st.caption("Tá na dúvida de quem colocar de capitão? Deixa a sorte decidir!")

    if st.button("🎲 GIRAR ROLETA DA SORTE", use_container_width=True):
      df_scout_sim, _ = carregar_dados_completos_scout()
      if not df_scout_sim.empty:
        opcoes_cap = df_scout_sim[df_scout_sim["status_id"] == 7][
            "jogador"
        ].tolist()
        if opcoes_cap:
          sorteado = random.choice(opcoes_cap)
          st.markdown(
              f"""
                    <div style="background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); border: 2px solid #eab308; padding: 15px; border-radius: 12px; text-align: center; margin-top: 10px;">
                        <span style="color:#eab308; font-weight:bold; font-size:12px;">🎰 A ROLETA MANDOU ESCALAR:</span>
                        <h2 style="color:#ffffff; margin: 5px 0;">⭐ {sorteado}</h2>
                        <span style="color:#00f2ff; font-size:12px;">Coloque como capitão e reze pelo mito! 🚀</span>
                    </div>
                """,
              unsafe_allow_html=True,
          )

  # --- TAB 4: CAMPEÕES DO MÊS ---
  with tab4:
    st.subheader("👑 Galeria de Campeões Mensais")
    if df_vencedores is not None and not df_vencedores.empty:
      st.dataframe(df_vencedores, use_container_width=True, hide_index=True)
    else:
      st.info("📌 Arquivo `base_vencedores.csv` não encontrado.")

  # --- TAB 5: GUIA DE VALORIZAÇÃO ---
  with tab5:
    st.subheader("💰 Patrimônio & Valorização Ao Vivo")
    df_val = df.sort_values(
        by="Valorização (C$)", ascending=False
    ).reset_index(drop=True)
    df_val["Rank Valorização"] = df_val.index + 1
    st.dataframe(
        df_val[[
            "Rank Valorização",
            "Time",
            "Cartoleiro",
            "Valorização (C$)",
            "Patrimônio (C$)",
        ]],
        column_config={
            "Valorização (C$)": st.column_config.NumberColumn(
                "Valorização (C$)", format="C$ %.2f"
            ),
            "Patrimônio (C$)": st.column_config.NumberColumn(
                "Patrimônio (C$)", format="C$ %.2f"
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

  # --- TAB 6: SCOUT LAB ATUALIZADO COMPLETO ---
  with tab6:
    st.subheader("🤖 Cartola Scout Lab - Análise do Mercado")
    df_scout_full, r_num = carregar_dados_completos_scout()

    if not df_scout_full.empty:
      provaveis_cnt = len(df_scout_full[df_scout_full["status_id"] == 7])
      preco_medio = df_scout_full["preco"].mean()
      media_top = df_scout_full[df_scout_full["status_id"] == 7]["media"].max()

      m1, m2, m3, m4 = st.columns(4)
      m1.metric("Total de Atletas", len(df_scout_full))
      m2.metric("Prováveis (Confirmados)", provaveis_cnt)
      m3.metric("Preço Médio", f"C$ {preco_medio:.2f}")
      m4.metric("Maior Média (Provável)", f"{media_top:.2f} pts")

      st.divider()

      f_col1, f_col2, f_col3 = st.columns([2, 2, 1])

      with f_col1:
        busca_atleta = st.text_input(
            "🔍 Buscar Jogador ou Clube:",
            placeholder="Digite Arrascaeta, Flamengo, etc...",
        )

      with f_col2:
        posicoes_disponiveis = [
            "TODAS",
            "GOL",
            "LAT",
            "ZAG",
            "MEI",
            "ATA",
            "TEC",
        ]
        pos_selecionada = st.selectbox(
            "📌 Filtrar Posição:", posicoes_disponiveis, index=0
        )

      with f_col3:
        apenas_provaveis = st.checkbox("Somente Prováveis 🟢", value=True)

      df_exibicao = df_scout_full.copy()

      if apenas_provaveis:
        df_exibicao = df_exibicao[df_exibicao["status_id"] == 7]

      if pos_selecionada != "TODAS":
        df_exibicao = df_exibicao[df_exibicao["posicao"] == pos_selecionada]

      if busca_atleta:
        termo = busca_atleta.lower()
        df_exibicao = df_exibicao[
            df_exibicao["jogador"].str.lower().str.contains(termo)
            | df_exibicao["time"].str.lower().str.contains(termo)
        ]

      df_exibicao = df_exibicao.sort_values(
          by="score", ascending=False
      ).reset_index(drop=True)

      st.markdown(
          f"### 📋 Atletas Recomendados ({len(df_exibicao)} encontrados)"
      )

      st.dataframe(
          df_exibicao[[
              "posicao",
              "jogador",
              "time",
              "status",
              "preco",
              "min_valorizar",
              "projecao",
              "variacao_est",
              "score",
          ]],
          column_config={
              "posicao": "Pos",
              "jogador": "Atleta",
              "time": "Clube",
              "status": "Status",
              "preco": st.column_config.NumberColumn(
                  "Preço (C$)", format="C$ %.2f"
              ),
              "min_valorizar": st.column_config.NumberColumn(
                  "Mín. p/ Val.", format="%.2f pts"
              ),
              "projecao": st.column_config.NumberColumn(
                  "Projeção", format="%.2f pts"
              ),
              "variacao_est": st.column_config.NumberColumn(
                  "Est. Valorização", format="C$ %+.2f"
              ),
              "score": st.column_config.NumberColumn(
                  "Score Lab", format="%.2f"
              ),
          },
          use_container_width=True,
          hide_index=True,
      )

      st.divider()

      st.markdown("### 🧮 Simulador de Valorização em Tempo Real")
      df_provaveis_sim = df_scout_full[
          df_scout_full["status_id"] == 7
      ].sort_values(by="jogador")
      opcoes_atletas = df_provaveis_sim["nome_busca"].tolist()

      atleta_sel_nome = st.selectbox(
          "Selecione o Atleta para Simular:", opcoes_atletas
      )

      if atleta_sel_nome:
        dados_atleta = df_provaveis_sim[
            df_provaveis_sim["nome_busca"] == atleta_sel_nome
        ].iloc[0]
        preco_atual = float(dados_atleta["preco"])
        mpv_atleta = float(dados_atleta["min_valorizar"])

        col_sim1, col_sim2 = st.columns([1, 1])

        with col_sim1:
          pts_simulados = st.slider(
              "Simular Pontuação na Rodada (pts):",
              min_value=-5.0,
              max_value=25.0,
              value=float(round(mpv_atleta + 2.0, 1)),
              step=0.5,
          )

        with col_sim2:
          diff_pts = pts_simulados - mpv_atleta
          variacao_estimada_c = diff_pts * 0.30
          novo_preco_estimado = max(0.70, preco_atual + variacao_estimada_c)

          if variacao_estimada_c >= 0:
            cor_val = "#22c55e"
            sinal = "+"
          else:
            cor_val = "#ef4444"
            sinal = ""

          st.markdown(
              f"""
                    <div style="background: rgba(18, 12, 38, 0.85); border: 1px solid {cor_val}; border-radius: 12px; padding: 14px; text-align: center;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Estimativa de Variação</div>
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900; color: {cor_val}; margin: 4px 0;">
                            {sinal}{variacao_estimada_c:.2f} C$
                        </div>
                        <div style="font-size: 13px; color: #f8fafc;">
                            Preço Atual: <strong>C$ {preco_atual:.2f}</strong> ➔ Novo Preço: <strong>C$ {novo_preco_estimado:.2f}</strong>
                        </div>
                        <div style="font-size: 11px; color: #c084fc; margin-top: 6px;">
                            Mínimo para Valorizar (MPV): <strong>{mpv_atleta:.2f} pts</strong>
                        </div>
                    </div>
                """,
              unsafe_allow_html=True,
          )

      st.divider()

      st.markdown("### 🚀 Montador de Time Ideal por Orçamento")
      col_b1, col_b2 = st.columns([1, 2])

      with col_b1:
        patrimonio_sugerido = (
            float(dados_time["Patrimônio (C$)"])
            if "dados_time" in locals()
            else 100.0
        )
        orcamento_scout = st.number_input(
            "Patrimônio (C$):",
            min_value=30.0,
            max_value=300.0,
            value=patrimonio_sugerido,
            step=0.5,
            key="scout_orcamento",
        )
        esquema_scout = st.selectbox(
            "Formação Tática:",
            ["4-3-3", "4-4-2", "3-5-2", "3-4-3", "5-3-2", "5-4-1"],
            key="scout_esquema",
        )
        btn_gerar_squad = st.button(
            "⚡ Gerar Escalação Ideal", use_container_width=True
        )

      with col_b2:
        esquemas_dict = {
            "4-3-3": {"GOL": 1, "LAT": 2, "ZAG": 2, "MEI": 3, "ATA": 3, "TEC": 1},
            "4-4-2": {"GOL": 1, "LAT": 2, "ZAG": 2, "MEI": 4, "ATA": 2, "TEC": 1},
            "3-5-2": {"GOL": 1, "LAT": 0, "ZAG": 3, "MEI": 5, "ATA": 2, "TEC": 1},
            "3-4-3": {"GOL": 1, "LAT": 0, "ZAG": 3, "MEI": 4, "ATA": 3, "TEC": 1},
            "5-3-2": {"GOL": 1, "LAT": 2, "ZAG": 3, "MEI": 3, "ATA": 2, "TEC": 1},
            "5-4-1": {"GOL": 1, "LAT": 2, "ZAG": 3, "MEI": 4, "ATA": 1, "TEC": 1},
        }

        if btn_gerar_squad or "squad_gerado" in st.session_state:
          necessidade = esquemas_dict[esquema_scout]
          df_provaveis = df_scout_full[
              df_scout_full["status_id"] == 7
          ].sort_values(by="score", ascending=False)

          titulares = []
          custo_total = 0.0

          for pos, qtd in necessidade.items():
            if qtd > 0:
              opcoes_pos = df_provaveis[df_provaveis["posicao"] == pos]
              for _, atleta in opcoes_pos.iterrows():
                if (
                    len([x for x in titulares if x["posicao"] == pos]) < qtd
                    and custo_total + atleta["preco"] <= orcamento_scout
                ):
                  titulares.append(atleta)
                  custo_total += atleta["preco"]

          df_squad = pd.DataFrame(titulares)

          if not df_squad.empty:
            val_total_time = df_squad["variacao_est"].sum()
            cor_val_squad = "#22c55e" if val_total_time >= 0 else "#ef4444"

            st.markdown(
                f"##### 🛡️ Esquadrão Sugerido ({esquema_scout}) — Custo Total:"
                f" **C$ {custo_total:.2f}** / **C$ {orcamento_scout:.2f}**"
            )
            st.markdown(
                f"📈 **Valorização Prevista do Time:** <span style='color:"
                f" {cor_val_squad}; font-weight: bold;'>C$"
                f" {val_total_time:+.2f}</span>",
                unsafe_allow_html=True,
            )

            st.dataframe(
                df_squad[[
                    "posicao",
                    "jogador",
                    "time",
                    "preco",
                    "min_valorizar",
                    "projecao",
                    "variacao_est",
                ]],
                column_config={
                    "posicao": "Pos",
                    "jogador": "Atleta",
                    "time": "Clube",
                    "preco": st.column_config.NumberColumn(
                        "Custo", format="C$ %.2f"
                    ),
                    "min_valorizar": st.column_config.NumberColumn(
                        "Mín. Val", format="%.2f pts"
                    ),
                    "projecao": st.column_config.NumberColumn(
                        "Projeção", format="%.2f pts"
                    ),
                    "variacao_est": st.column_config.NumberColumn(
                        "Est. Val", format="C$ %+.2f"
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )
    else:
      st.warning(
          "⚠️ Não foi possível obter os dados do Scout Lab no momento."
      )

  # --- TAB 7: RADAR DE SG ---
  with tab7:
    st.subheader("🛡️ Radar de Saldo de Gols (Probabilidade SG)")
    if lista_partidas:
      sg_dados = []
      for p in lista_partidas:
        sg_dados.append({
            "Clube": p["nome_casa"],
            "Mando": "Mandante 🏠",
            "Prob. SG": "78% 🔥",
        })
        sg_dados.append({
            "Clube": p["nome_vis"],
            "Mando": "Visitante ✈️",
            "Prob. SG": "42% ⚠️",
        })

      df_sg = pd.DataFrame(sg_dados)
      st.dataframe(df_sg, use_container_width=True, hide_index=True)

  # --- TAB 8: CARDS FUT ---
  with tab8:
    st.subheader("🎴 Cards da Zueira (Estilo FUT)")
    c_fut1, c_fut2 = st.columns(2)

    with c_fut1:
      st.markdown(
          f"""
                <div class="fut-card-container">
                    <div class="fut-card-badge">BLACK GUYS LEAGUE</div>
                    <div class="fut-card-title">🚀 MITO DA RODADA</div>
                    <div class="fut-card-score">+{mito_rodada['Pontos Ganhos (Última Rodada)']}</div>
                    <div class="fut-card-sub">{mito_rodada['Time']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with c_fut2:
      st.markdown(
          f"""
                <div class="fut-card-container" style="border-color: #00f2ff;">
                    <div class="fut-card-badge" style="color:#00f2ff;">BLACK GUYS LEAGUE</div>
                    <div class="fut-card-title">🥇 LÍDER GERAL</div>
                    <div class="fut-card-score" style="color:#eab308;">{lider_geral['Total Acumulado']}</div>
                    <div class="fut-card-sub">{lider_geral['Time']}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )

  st.divider()
  st.caption(
      f"⚡ Black Guys League | Rodada {rodada_atual} | Responsivo em"
      " Dispositivos Móveis."
  )
