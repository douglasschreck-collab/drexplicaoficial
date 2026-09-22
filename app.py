import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURAÇÕES INTERNACIONAIS DA PLATAFORMA
st.set_page_config(
    page_title="RadAI // Premium Reporting Suite", 
    page_icon="🩻", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. DESIGN PREMIUM INTERACTIVE (CSS INJECTION)
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        html, body, [data-testid="stAppViewContainer"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #F8FAFC !important; 
            color: #0F172A !important;
        }
        
        [data-testid="stHeader"], footer, #MainMenu { display: none !important; }
        
        .clinic-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background-color: #0F172A; 
            border-bottom: 3px solid #06B6D4; 
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .clinic-brand {
            color: #22D3EE !important; 
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.05em;
        }
        .clinic-badge {
            background-color: #1E293B;
            color: #FFFFFF; 
            padding: 0.35rem 0.85rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid #334155;
        }

        .main-title-suite {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.04em;
            margin-bottom: 2rem;
        }
        .main-title-suite span {
            color: #0284C7; 
            font-weight: 300;
        }

        .workspace-block {
            background: #F1F5F9 !important; 
            border: 1px solid #CBD5E1 !important;
            border-radius: 14px !important;
            padding: 2.2rem !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02) !important;
            margin-bottom: 1.5rem;
        }
        
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important;
            border-radius: 8px !important;
            color: #0F172A !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
        }
        .stButton>button:hover {
            color: #22D3EE !important; 
        }

        .medical-sheet-output {
            background-color: #FFFFFF !important; 
            color: #1E293B !important; 
            padding: 2.5rem !important;
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            border-top: 5px solid #0F172A !important; 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05) !important;
            font-size: 1.05rem !important;
            line-height: 1.7 !important;
        }
        
        .missing-data-alert {
            background-color: #FEF2F2 !important;
            border: 1px solid #FCA5A5 !important;
            border-left: 5px solid #EF4444 !important;
            padding: 1.2rem !important;
            border-radius: 8px !important;
            color: #991B1B !important;
            margin-bottom: 1.5rem !important;
            font-weight: 600 !important;
        }

        label p {
            color: #334155 !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. VERIFICAÇÃO DE CREDENCIAIS
api_key_configured = "GEMINI_API_KEY" in st.secrets

if not api_key_configured:
    st.error("Chave de API 'GEMINI_API_KEY' ausente nos Secrets do Streamlit.")

# 4. DIRETRIZES DO MOTOR CLÍNICO (SYSTEM PROMPT)
SYSTEM_INSTRUCTION = """
Você é o motor inteligente do RadAI Suite. Seu papel é atuar como um radiologista sênior estruturando relatórios médicos de alta precisão.
Diretrizes:
1. IDIOMA: Siga a escolha de idioma do usuário.
2. NORMAS: Aplique estritamente as diretrizes vigentes (ACR, ESR, BI-RADS, LI-RADS, PI-RADS, TI-RADS, Lung-RADS).
3. ZERO ALUCINAÇÃO: Se faltar critérios decisivos para um score, monte obrigatoriamente um alerta estruturado em formato HTML: <div class="missing-data-alert">⚠️ INFORMAÇÕES NECESSÁRIAS PARA CLASSIFICAÇÃO...</div> antes de qualquer outro texto do laudo, listando o que falta.
4. FORMATAÇÃO: Escreva diretamente em Markdown limpo para renderização na folha clínica.
"""

# 5. UI VIEWPORT
st.markdown("""
    <div class="clinic-top-bar">
        <div class="clinic-brand">Desenvolvido por @DrExplicaOficial</div>
        <div class="clinic-badge">RADAI SUITE v3.3 // LINEAR PRODUCTION</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title-suite">🩻 RadAI <span>// Engine de Laudos Estruturados</span></div>', unsafe_allow_html=True)

# Geração de colunas simétricas
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="workspace-block">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A; margin-top:0; margin-bottom:1.5rem; font-weight:700;'>Configuração e Captura</h4>", unsafe_allow_html=True)
    
    idioma = st.selectbox(
        "Idioma de Destino do Documento", 
        ["Mesmo do texto de entrada", "Português", "English", "Español"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    notas_medicas = st.text_area(
        "Inserção de Dados Clínicos (Ditado Corrente ou Notas Rápidas)", 
        height=340, 
        placeholder="Digite ou cole observações rápidas..."
    )
    
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    processar = st.button("Executar Engenharia de Laudo")
    st.markdown("</div>")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="workspace-block">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A; margin-top:0; margin-bottom:1.5rem; font-weight:700;'>Visualização do Documento Técnico</h4>", unsafe_allow_html=True)
    
    if processar and notas_medicas and api_key_configured:
        with st.spinner("Compilando dados estruturados sob diretrizes internacionais..."):
            try:
                # Inicialização utilizando o motor de nova geração homologado de alta disponibilidade (gemini-3.6-flash)
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                prompt_final = notas_medicas if idioma == "Mesmo do texto de entrada" else f"Gere o laudo em {idioma}. Notas: {notas_medicas}"
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt_final,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.0
                    )
                )
                
                st.markdown('<div class="medical-sheet-output">', unsafe_allow_html=True)
                st.markdown(response.text, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Falha de barramento: {e}")
    else:
        st.markdown("""
            <div style="color: #64748B; text-align: center; margin-top: 160px; font-family: 'JetBrains Mono'; font-size: 0.95rem; font-style: italic;">
                [SISTEMA PRONTO]<br>Aguardando submissão de dados clínicos para renderização...
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
