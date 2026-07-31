import streamlit as st
import pandas as pd
import requests
import urllib.parse

# 1. Configuração da página do site
st.set_page_config(page_title="Black Guys League", page_icon="🏆", layout="wide")

# 2. Função que baixa os dados (usamos "cache" para o site carregar rápido e não travar)
@st.cache_data(ttl=300) # Atualiza a cada 5 minutos
def puxar_dados_cartola():
    try:
        df_base = pd.read_csv("base_cartola.csv", sep=None, engine='python', encoding='utf-8-sig')
        df_base.columns = df_base.columns.str.strip()
    except:
        st.error("Arquivo base_cartola.csv não encontrado!")
        return pd.DataFrame(), 0

    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        res_mercado = requests.get("https://api.cartola.globo.com/mercado/status", headers=headers, timeout=5)
        rodada_atual = res_mercado.json().get("rodada_atual", 0) if res_mercado.status_code == 200 else 0
    except:
        rodada_atual = 0

    lista_final = []
    
    for index, row in df_base.iterrows():
        nome_time = str(row["Time"]).strip()
        cartoleiro = str(row["Cartoleiro"]).strip()
        pontuacao_base = float(row["Total"])
        
        nome_limpo = nome_time.replace(",", "").replace(" and ", " ").replace("  ", " ").strip()
        url_busca = "https://api.cartola.globo.com/times"
        
        try:
            res_busca = requests.get(url_busca, params={"q": nome_limpo}, headers=headers, timeout=5)
            time_id = None
            if res_busca.status_code == 200:
                resultados = res_busca.json()
                lista_resultados = resultados if isinstance(resultados, list) else resultados.get("times", [])
                for t in lista_resultados:
                    if t.get("nome_cartola", "").lower() == cartoleiro.lower() or t.get("nome", "").lower() == nome_time.lower():
                        time_id = t.get("time_id")
                        break
                if not time_id and len(lista_resultados) > 0:
                    time_id = lista_resultados[0].get("time_id")
            
            pt_rodada, pt_mes, pt_turno = 0.0, 0.0, 0.0
            if time_id:
                res_pontos = requests.get(f"https://api.cartola.globo.com/time/id/{time_id}", headers=headers, timeout=5)
                if res_pontos.status_code == 200:
                    pontos_raw = res_pontos.json().get("pontos", 0)
                    if isinstance(pontos_raw, dict):
                        pt_rodada = float(pontos_raw.get("rodada", 0))
                        pt_mes = float(pontos_raw.get("mes", 0))
                        pt_turno = float(pontos_raw.get("turno", 0))
            
            novo_total = pontuacao_base + pt_rodada
            lista_final.append({
                "Time": nome_time,
                "Cartoleiro": cartoleiro,
                "Total": round(novo_total, 2),
                "Últ. Rodada": round(pt_rodada, 2),
                "Mes": round(pt_mes, 2),
                "Turno": round(pt_turno, 2)
            })
        except:
            lista_final.append({"Time": nome_time, "Cartoleiro": cartoleiro, "Total": pontuacao_base, "Últ. Rodada": 0.0, "Mes": 0.0, "Turno": 0.0})

    df = pd.DataFrame(lista_final)
    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
    df["Posição"] = df.index + 1
    
    # Diferenças
    lider_geral = df.iloc[0]["Total"]
    df["Dif. Rival"] = (df["Total"].shift(1) - df["Total"]).round(2).fillna(0)
    df["Dif. Líder"] = (lider_geral - df["Total"]).round(2)
    
    return df, rodada_atual

# 3. Desenhando a Tela do Site
st.title("🏆 Black Guys League - Cartola FC")
st.markdown("Acompanhe a classificação em tempo real da nossa liga!")

with st.spinner("Conectando aos servidores da Globo e calculando pontos..."):
    df, rodada_atual = puxar_dados_cartola()

if not df.empty:
    st.caption(f"Status do Campeonato: Rodada {rodada_atual} | Dados calculados ao vivo")
    st.divider()
    
    # Cards de Destaque
    lider = df.iloc[0]
    mito = df.sort_values(by="Últ. Rodada", ascending=False).iloc[0]
    lider_mes = df.sort_values(by="Mes", ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🥇 Líder Geral", f"{lider['Time']}", f"{lider['Total']} pts")
    col2.metric("🚀 Mito da Rodada", f"{mito['Time']}", f"{mito['Últ. Rodada']} pts")
    col3.metric("📈 Líder do Mês", f"{lider_mes['Time']}", f"{lider_mes['Mes']} pts")
    
    st.divider()
    
    # Tabela Bonita
    st.subheader("📊 Classificação Completa")
    st.dataframe(
        df[["Posição", "Time", "Cartoleiro", "Total", "Últ. Rodada", "Dif. Rival", "Dif. Líder"]],
        use_container_width=True,
        hide_index=True
    )