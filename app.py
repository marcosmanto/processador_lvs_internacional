import base64
import time
import warnings
from datetime import datetime
from io import BytesIO

import requests
import streamlit as st


# ==============================================================================
# SISTEMA DE SEGURANÇA (KILL SWITCH)
# ==============================================================================
def verificar_licenca_remota():
    # LINK DA SUA PLANILHA (Substitua pelo link que você copiou no passo 1)
    url_controle = "https://pastebin.com/raw/eTsMCxet"

    try:
        # Adiciona numero aleatorio para evitar cache local
        fresh_url = f"{url_controle}?v={int(time.time())}"

        # Usamos requests que é mais leve que pandas para texto puro
        response = requests.get(fresh_url, timeout=5)

        # Pega o texto e limpa espaços
        texto_chave = response.text.strip().upper()

        if texto_chave != "LIBERADO":
            raise ValueError("Licença revogada")

    except Exception:
        svg_letter = """
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path fill="#FFF" stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
        </svg>
        """

        # Codifica o SVG para Base64 (Isso evita erro de renderização de HTML)
        b64_letter = base64.b64encode(svg_letter.encode("utf-8")).decode("utf-8")

        # --- ANIMAÇÃO DE FALHA ---

        # 1. Cria um espaço vazio para a barra
        placeholder_barra = st.empty()

        # 2. Desenha a barra dentro desse espaço
        barra = placeholder_barra.progress(
            0, text="Estabelecendo conexão segura com servidor ANTT..."
        )

        # 3. Anima a barra (Simula tentativa de conexão)
        for percent_complete in range(100):
            time.sleep(0.02)  # Ajuste a velocidade aqui (0.04 é um bom drama)
            barra.progress(percent_complete + 1, text="Verificando tokens de acesso...")

        # 4. A BARRA SOME (Limpa o espaço reservado)
        placeholder_barra.empty()

        # 5. SÓ AGORA EXIBE OS TEXTOS
        st.error("⛔ ERRO CRÍTICO 503: Falha de validação de segurança.")

        st.warning("Não foi possível autenticar a licença de uso deste software.")

        # Box personalizado com o E-mail e Link
        st.markdown(
            f"""
        <div style='background-color: #262730; padding: 15px; border-radius: 5px; border: 1px solid #444;'>
            <p style='margin-bottom: 5px;'>Entre em contato imediatamente com o administrador para solicitar nova chave:</p>
            <div style='display: flex; align-items: flex-start; gap: 0 5px; align-items: center'>
                <img src="data:image/svg+xml;base64,{b64_letter}" width="24" height="24" />
                <p style='font-size: 1.1em;margin: 0;'>
                    <a href='mailto:marcos.filho@antt.gov.br' style='color: #59acf8; text-decoration: none; font-weight: bold;'>
                        marcos.filho@antt.gov.br
                    </a>
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.stop()  # Trava tudo


# ==============================================================================
# 0. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================

st.set_option("client.showErrorDetails", "none")
st.set_option("client.showSidebarNavigation", False)
st.set_option("client.toolbarMode", "viewer")

st.set_page_config(
    page_title="Processador LVs Internacionais",
    layout="wide",
    page_icon="favicon.ico",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        /* --- BLOCO 1: REMOÇÃO DE ELEMENTOS VISUAIS --- */

        /* Remove cabeçalho, decoração, status e rodapé */
        header[data-testid="stHeader"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        footer {
            display: none !important;
        }

        /* Ajuste do topo */
        .main .block-container {
            padding-top: 2rem !important;
        }

        /* --- BLOCO 2: ANTI-FADE E ANTI-PISCA (A CORREÇÃO) --- */

        /* 9. FORÇA A OPACIDADE TOTAL SEMPRE */
        /* Impede que o Streamlit esmaeça a tela quando está 'running' */
        .stApp,
        .stApp[data-test-script-state="running"],
        [data-testid="stAppViewContainer"],
        .stMain {
            opacity: 1 !important;
            filter: none !important; /* Remove filtros de cinza/blur */
            transition: none !important; /* Mata qualquer animação de fade */
        }

        /* 10. PROTEGE OS ELEMENTOS INTERNOS DE HERDAR FADE */
        /* Garante que o conteúdo (botões, textos) fique 100% visível */
        .stApp > *,
        [data-testid="stVerticalBlock"] > * {
            opacity: 1 !important;
            transform: none !important;
        }

        /* 11. TRAVA O CURSOR E INTERAÇÃO */
        /* Impede o cursor de 'aguarde' ou 'stop' */
        .stApp[data-test-script-state="running"] {
            cursor: default !important;
        }

        /* 12. SUAVIZAÇÃO APENAS DO UPLOAD (Para ficar bonito) */
        div[data-testid="stFileUploaderDropzone"] {
            transition: background-color 0.1s;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# CHAMADA DA VERIFICAÇÃO IMEDIATAMENTE APÓS CONFIG DA PÁGINA
verificar_licenca_remota()

# Silenciar avisos
warnings.simplefilter(action="ignore", category=FutureWarning)

# ==============================================================================
# 1. CABEÇALHO E UI
# ==============================================================================

# --- CORREÇÃO DO SPLASH SCREEN ---
# Verificamos ANTES de criar qualquer elemento visual (placeholder)
if "splash_loading" not in st.session_state:
    st.session_state["splash_loading"] = True

    # O placeholder só é criado NA PRIMEIRA VEZ
    splash_placeholder = st.empty()

    with splash_placeholder.container():
        col_a, col_b, col_c = st.columns([1, 6, 1])
        with col_b:
            try:
                # Já com a correção do width que você fez
                st.image("splash.png", width="stretch")
                st.markdown(
                    "<h3 style='text-align: center; color: #aaa;'>Carregando...</h3>",
                    unsafe_allow_html=True,
                )
            except:
                pass

    time.sleep(2.5)  # Tempo do splash

    # Limpa e marca como pronto
    splash_placeholder.empty()
    st.session_state["splash_loading"] = False

    # TRUQUE DE MESTRE: Recarrega a página para limpar o HTML do splash da memória
    st.rerun()

# --- FIM DO BLOCO SPLASH ---

# Definição do Logo SVG (Copiado e limpo)
svg_antt = """
<svg version="1.1" id="Camada_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 76 76" style="enable-background:new 0 0 76 76;" xml:space="preserve">
  <g fill="#fff">
    <path d="M0,66.5c0.4,0,0.4-0.3,0.6-0.6c1.8-3.1,3.6-6.1,5.3-9.2c4.2-7.2,8.4-14.5,12.7-21.7c0.1-0.1,0.2-0.3,0.2-0.4 c0,0,0.1,0,0.1,0c0,0,0.1,0,0.1,0c6.1,10.5,12.2,21,18.2,31.5c0.1,0.1,0.1,0.2,0.2,0.4c-0.4,0-0.7,0-1,0c-8.4,0-16.9,0-25.3,0 c-3.4,0-6.7,0-10.1,0c-0.4,0-0.7,0-1.1-0.1L0,66.5z" />
    <path d="M20.8,36l40.9-4.9l0.1,0.2l-24.6,33C36.7,63.9,21.1,36.9,20.8,36z" />
    <path d="M37.5,2c5.6,9.8,11.2,19.4,16.8,29.2c-1.1,0.1-2.1,0.3-3,0.4c-2.8,0.3-5.7,0.7-8.5,1c-2.7,0.3-5.5,0.7-8.2,1 c-2.7,0.3-5.5,0.7-8.2,1c-1.8,0.2-3.7,0.4-5.5,0.7c-0.4,0.1-0.9,0-1.2-0.3c-0.5-0.5-0.5-0.7-0.2-1.3c5.9-10.3,11.8-20.7,17.7-31 C37.2,2.4,37.3,2.3,37.5,2z" />
    <path d="M74.9,66.7h-0.9c-11.7,0-23.4,0-35.2,0c-0.5,0-0.9,0-1.2-0.6c-0.2-0.5-0.2-0.9,0.1-1.3 c0.6-0.8,1.1-1.5,1.7-2.3c6-8.1,12.1-16.2,18.1-24.3c0.2-0.2,0.3-0.4,0.6-0.7L74.9,66.7z" />
  </g>
</svg>
"""

# Codifica o SVG para Base64 (Isso evita erro de renderização de HTML)
b64_logo = base64.b64encode(svg_antt.encode("utf-8")).decode("utf-8")

# Renderiza usando tag IMG padrão, que é mais segura
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="data:image/svg+xml;base64,{b64_logo}" width="70" />
        <div>
            <h1 style="margin: 0; padding: 0;">Processador LVs Internacionais</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("##### Filtro e Consolidação de Viagens Ocasionais por Países Visitados")
st.divider()

# --- Box de Instruções / Disclaimer ---
st.info("""
**ℹ️ Como obter os dados para este sistema:**

Os arquivos devem ser baixados diretamente do **Portal de Dados Abertos da ANTT**.
1.  Acesse o conjunto de dados: **[Licenças de Viagens do Fretamento Eventual e Turístico](https://dados.antt.gov.br/dataset/sisaut-nacional-internacional)**.
2.  Na lista de Recursos, procure pelos arquivos mensais nomeados como **"Licenças de Viagem - [Mês/Ano]"** (Ex: *Licenças de Viagem - Jan2026*).
3.  Clique em **Explorar** e depois em **Baixar** (certifique-se de baixar o arquivo **.CSV**).
4.  Após o download, arraste os arquivos para a área pontilhada abaixo.
""")

# Se você quiser exibir o print que mencionou, salve a imagem na pasta e descomente a linha abaixo:
st.image(
    "instrucoes_antt.png",
    caption="👆  Baixe arquivos do tipo CSV na página Licenças de Viagens do Fretamento Eventual e Turístico nos Portal de Dados Abertos ANTT",
    width=824,
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info("📂 **Passo 1: Seleção de Arquivos**")
    uploaded_files = st.file_uploader(
        "Arraste os arquivos CSV aqui (sisaut*.csv)",
        type="csv",
        accept_multiple_files=True,
        help="Você pode selecionar múltiplos arquivos de meses diferentes.",
    )

with col2:
    st.info("⚙️ **Passo 2: Configurações do Filtro**")

    lista_paises_sugestao = [
        "ARGENTINA",
        "PARAGUAI",
        "URUGUAI",
        "CHILE",
        "BOLÍVIA",
        "PERU",
    ]
    paises_alvo = st.multiselect(
        "Filtrar viagens que passaram por:",
        options=lista_paises_sugestao,
        default=["ARGENTINA", "PARAGUAI"],
    )

    timestamp_default = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo_input = st.text_input(
        "Nome do arquivo de saída:",
        value=f"Relatorio_Viagens_{timestamp_default}",
        placeholder="Digite o nome do arquivo...",
    )

st.divider()

# Centralizando o botão de ação
col_esq, col_centro, col_dir = st.columns([1, 2, 1])
with col_centro:
    botao_processar = st.button(
        "🚀 Processar e Gerar Relatório", type="primary", width="stretch"
    )

# ==============================================================================
# 2. LÓGICA DE PROCESSAMENTO
# ==============================================================================

if botao_processar and uploaded_files:
    with st.status("Processando dados...", expanded=True) as status:
        # Leitura
        status.write("📖 Lendo arquivos CSV...")
        dfs = []
        import pandas as pd

        for uploaded_file in uploaded_files:
            try:
                df_temp = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
                dfs.append(df_temp)
            except Exception as e:
                st.error(f"Erro ao ler {uploaded_file.name}: {e}")

        if not dfs:
            status.update(label="Erro no carregamento!", state="error")
            st.stop()

        # Consolidação
        df = pd.concat(dfs, ignore_index=True)
        status.write(f"✅ {len(df)} trechos carregados. Iniciando análise...")

        # Função Core (Master)
        def processar_viagem(grupo):
            grupo = grupo.sort_values("sequencia_trecho")
            primeiro_trecho = grupo.iloc[0]
            ultimo_trecho = grupo.iloc[-1]

            todos_paises = set(grupo["pais_inicio_trecho"].unique()) | set(
                grupo["pais_final_trecho"].unique()
            )
            paises_alvo_upper = [p.upper() for p in paises_alvo]
            alvos_encontrados = todos_paises.intersection(set(paises_alvo_upper))

            if not alvos_encontrados:
                return None

            passou_por_str = ", ".join(sorted(list(alvos_encontrados)))

            return pd.Series(
                {
                    "numero_licenca_viagem": primeiro_trecho["numero_licenca_viagem"],
                    "razao_social": primeiro_trecho["razao_social"],
                    "cnpj": primeiro_trecho["cnpj"],
                    "data_inicio_viagem": primeiro_trecho["data_inicio_viagem"],
                    "data_fim_viagem": primeiro_trecho["data_fim_viagem"],
                    "origem_viagem": f"{primeiro_trecho['municipio_inicio_trecho']}/{primeiro_trecho['UF_inicio_trecho']}",
                    "destino_retorno": f"{ultimo_trecho['municipio_final_trecho']}/{ultimo_trecho['UF_final_trecho']}",
                    "passou_por": passou_por_str,
                    "total_trechos": len(grupo),
                    "circuito_fechado_valido": (
                        primeiro_trecho["municipio_inicio_trecho"]
                        == ultimo_trecho["municipio_final_trecho"]
                    ),
                }
            )

        # Aplicação
        df_condensado = df.groupby("numero_licenca_viagem").apply(processar_viagem)
        df_final = df_condensado.dropna().sort_index()

        status.update(
            label="Processamento Concluído!", state="complete", expanded=False
        )

    # ==============================================================================
    # 3. RESULTADOS E DOWNLOAD
    # ==============================================================================

    st.success(f"Viagens encontradas: **{len(df_final)}**")

    # Exibe tabela
    st.dataframe(df_final.head(10), width="stretch")

    # Prepara Download
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_final.to_excel(writer, index=False)

    nome_final = (
        nome_arquivo_input
        if nome_arquivo_input.endswith(".xlsx")
        else f"{nome_arquivo_input}.xlsx"
    )

    col_dl_1, col_dl_2, col_dl_3 = st.columns([1, 2, 1])
    with col_dl_2:
        st.download_button(
            label="📥 Baixar Arquivo Excel",
            data=buffer,
            file_name=nome_final,
            mime="application/vnd.ms-excel",
            type="primary",
            width="stretch",
        )

elif botao_processar and not uploaded_files:
    st.warning("⚠️ Selecione os arquivos CSV primeiro.")
