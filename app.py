import streamlit as st
import google.generativeai as genai

# 1. ORCHESTRATION & META
st.set_page_config(
    page_title="RadAI // Advanced Reporting Suite", 
    page_icon="🩻", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HIGH-END MEDICAL ENTERPRISE UI (CSS INJECTION)
# Paleta: Azure Acinzentado, Azul Marinho, Cinza Chumbo, Branco, Ciano, Off-white
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* Reset estrutural para forçar o Dark Mode Clínico no canvas do Streamlit */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #0F172A !important; /* Cinza Chumbo / Azul Escuro Profundo */
            color: #E2E8F0 !important;
        }
        
        /* Remover decorações nativas vazias do Streamlit */
        [data-testid="stHeader"], footer, #MainMenu { display: none !important; }
        
        /* Barra de Status Superior (Micro-Painel) */
        .clinic-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1.5rem;
            background-color: #1E293B; /* Azure acinzentado escuro */
            border-bottom: 1px solid #334155;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        .clinic-badge {
            background-color: #1E3A8A;
            color: #38BDF8; /* Ciano suave */
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            border: 1px solid #0284C7;
        }

        /* Título Principal */
        .main-title-suite {
            font-size: 1.75rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.04em;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .main-title-suite span {
            color: #22D3EE; /* Ciano de Destaque */
            font-weight: 300;
        }

        /* Módulos Operacionais (Cards Dinâmicos) */
        .workspace-block {
            background: #1E293B !important; /* Azul Marinho Corporativo */
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2) !important;
            transition: border-color 0.3s ease;
        }
        .workspace-block:focus-within {
            border-color: #06B6D4 !important;
        }
        
        /* Inputs de Texto Avançados */
        .stTextArea textarea {
            background-color: #0F172A !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        .stTextArea textarea:focus {
            border-color: #22D3EE !important;
            box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
        }
        
        /* Selectbox e componentes de escolha */
        div[data-baseweb="select"] > div {
            background-color: #0F172A !important;
            border: 1px solid #475569 !important;
            color: white !important;
        }
        
        /* Botão de Disparo Balístico (Ação Principal) */
        .stButton>button {
            background: linear-gradient(90deg, #06B6D4 0%, #0369A1 100%) !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            border: 1px solid #22D3EE !important;
            padding: 0.85rem 2rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 4px 14px 0 rgba(6, 182, 212, 0.4) !important;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #22D3EE 0%, #0284C7 100%) !important;
            box-shadow: 0 6px 20px 0 rgba(6, 182, 212, 0.6) !important;
            color: #FFFFFF !important;
        }

        /* Folha de Laudo Médico Digital (O Prontuário) */
        .medical-sheet-output {
            background-color: #FFFFFF !important; /* Off-white puro para contraste cirúrgico de leitura */
            color: #0F172A !important; /* Letras chumbo escuras para leitura sem fadiga */
            padding: 2.5rem !important;
            border-radius: 8px !important;
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06), 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
            border-left: 5px solid #0F172A !important;
            font-size: 1rem !important;
            line-height: 1.7 !important;
        }
        .medical-sheet-output h1, .medical-sheet-output h2, .medical-sheet-output h3 {
            color: #1E3A8A !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important;
            border-bottom: 1px solid #E2E8F0 !important;
            padding-bottom: 0.3rem !important;
        }
        
        /* Alertas Críticos de Classificações Faltantes */
        .missing-data-alert {
            background-color: #FEF2F2 !important;
            border: 1px solid #FCA5A5 !important;
            border-left: 4px solid #EF4444 !important;
            padding: 1rem !important;
            border-radius: 6px !important;
            color: #991B1B !important;
            margin-bottom: 1.5rem !important;
            font-weight: 500 !important;
        }

        /* Estilização das Labels nativas */
        label p {
            color: #94A3B8 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. SEGURANÇA E AMBIENTE API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API do Gemini ausente nos Secrets.")

# 4. MOTOR CLÍNICO (SYSTEM PROMPT)
SYSTEM_INSTRUCTION = """
Você é o motor inteligente do RadAI Suite. Seu papel é atuar como um radiologista sênior estruturando relatórios médicos de alta precisão.
Diretrizes:
1. IDIOMA: Siga a escolha exata do usuário.
2. NORMAS: Aplique estritamente as diretrizes vigentes (ACR, ESR, BI-RADS, LI-RADS, PI-RADS, TI-RADS, Lung-RADS).
3. ZERO ALUCINAÇÃO: Se faltar critérios decisivos para um score, monte o alerta estruturado em formato HTML: <div class="missing-data-alert">⚠️ INFORMAÇÕES NECESSÁRIAS PARA CLASSIFICAÇÃO...</div> antes de qualquer outro texto.
4. FORMATAÇÃO: Escreva diretamente em Markdown limpo para renderização na folha clínica.
"""

# 5. UI VIEWPORT
st.markdown("""
    <div class="clinic-top-bar">
        <div style="color: #94A3B8; font-size: 0.8rem; font-family: 'JetBrains Mono'; font-weight:500;">INSTITUTIONAL // CLINICAL USE ONLY</div>
        <div class="clinic-badge">ENGINE VERSION: GEMINI 1.5 PRO v2</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title-suite">🩻 RadAI <span>// Engine de Laudos Estruturados</span></div>', unsafe_allow_html=True)

# Grid estrutural balanceado
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="workspace-block">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;margin-top:0;margin-bottom:1.5rem;'>Configuração e Captura</h4>", unsafe_allow_html=True)
    
    idioma = st.selectbox(
        "Idioma de Destino do Documento", 
        ["Mesmo do texto de entrada", "Português", "English", "Español"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    notas_medicas = st.text_area(
        "Inserção de Dados Clínicos (Ditado Corrente ou Notas Rápidas)", 
        height=340, 
        placeholder="Digite ou cole observações rápidas... Ex: 'Nódulo hepático segmento VII, hiperecoico, 2cm, sem fluxo ao Doppler...'"
    )
    
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    processar = st.button("Executar Engenharia de Laudo")
    st.markdown("</div>")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="workspace-block">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;margin-top:0;margin-bottom:1.5rem;'>Visualização do Documento Técnico</h4>", unsafe_allow_html=True)
    
    if processar and notas_medicas:
        with st.spinner("Compilando dados estruturados sob diretrizes internacionais..."):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    system_instruction=SYSTEM_INSTRUCTION,
                    generation_config={"temperature": 0.0}
                )
                
                prompt_final = notas_medicas if idioma == "Mesmo do texto de entrada" else f"Gere o laudo em {idioma}. Notas: {notas_medicas}"
                response = model.generate_content(prompt_final)
                
                # Renderizador da prancheta médica contrastante de alta definição
                st.markdown(f'<div class="medical-sheet-output">', unsafe_allow_html=True)
                st.markdown(response.text, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Falha de barramento com o motor de IA: {e}")
    else:
        st.markdown(
