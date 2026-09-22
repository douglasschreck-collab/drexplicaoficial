import streamlit as st
import google.generativeai as genai

# 1. ORCHESTRATION & META
st.set_page_config(
    page_title="RadAI // Premium Reporting Suite", 
    page_icon="🩻", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. PREMIUM ENTERPRISE UI (CSS INJECTION)
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        /* Fundo Geral Off-white para conforto visual do radiologista */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #F8FAFC !important; 
            color: #0F172A !important;
        }
        
        /* Ocultar elementos nativos e sem graça do Streamlit */
        [data-testid="stHeader"], footer, #MainMenu { display: none !important; }
        
        /* Top Bar Executiva Personalizada */
        .clinic-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background-color: #0F172A; /* Azul Marinho Profundo */
            border-bottom: 3px solid #06B6D4; /* Linha de destaque em Ciano */
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .clinic-brand {
            color: #22D3EE !important; /* Ciano */
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

        /* Título do Workspace */
        .main-title-suite {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.04em;
            margin-bottom: 2rem;
        }
        .main-title-suite span {
            color: #0284C7; /* Azul Corporativo */
            font-weight: 300;
        }

        /* Blocos de Trabalho Avançados (Azure Acinzentado Macio) */
        .workspace-block {
            background: #F1F5F9 !important; 
            border: 1px solid #CBD5E1 !important;
            border-radius: 14px !important;
            padding: 2.2rem !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02), 0 4px 6px -2px rgba(0, 0, 0, 0.02) !important;
            margin-bottom: 1.5rem;
        }
        
        /* Inputs de Texto Clínico */
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important;
            border-radius: 8px !important;
            color: #0F172A !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        .stTextArea textarea:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15) !important;
        }
        
        /* Caixas de Seleção Estilizadas */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
        }
        
        /* Botão Balístico Executivo */
        .stButton>button {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            letter-spacing: 0.02em;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.25) !important;
            color: #22D3EE !important; /* Brilha em Ciano no hover */
        }

        /* Prancheta Médica de Saída (Contraste Máximo) */
        .medical-sheet-output {
            background-color: #FFFFFF !important; 
            color: #1E293B !important; /* Texto chumbo escuro, perfeito para leitura prolongada */
            padding: 2.5rem !important;
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            border-top: 5px solid #0F172A !important; /* Topo Marinho */
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05) !important;
            font-size: 1.05rem !important;
            line-height: 1.7 !important;
        }
        
        /* Alertas de Scores Faltantes */
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

        /* Ajuste fino nas labels */
        label p {
            color: #334155 !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            letter-spacing: -0.01em !important;
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

# 5. UI VIEWPORT (Estrutura de tela sem tags órfãs)
st.markdown("""
    <div class="clinic-top-bar">
        <div class="clinic-brand">Desenvolvido por @DrExplicaOficial</div>
        <div class="clinic-badge">RADAI SUITE v2.5</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title-suite">🩻 RadAI <span>// Engine de Laudos Estruturados</span></div>', unsafe_allow_html=True)

# Divisão limpa em duas colunas simétricas
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
        placeholder="Digite ou cole observações rápidas... Ex: 'Nódulo hepático segmento VII, hiperecoico, 2cm, sem fluxo ao Doppler...'"
    )
    
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    processar = st.button("Executar Engenharia de Laudo")
    st.markdown("</div>")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="workspace-block">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A; margin-top:0; margin-bottom:1.5rem; font-weight:700;'>Visualização do Documento Técnico</h4>", unsafe_allow_html=True)
    
    if processar and notas_medicas:
        with st.spinner("Compilando dados estruturados sob diretrizes internacionais..."):
            try:
                # Inicialização correta e limpa do modelo
                model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
                
                prompt_final = notas_medicas if idioma == "Mesmo do texto de entrada" else f"Gere o laudo em {idioma}. Notas: {notas_medicas}"
                
                # Correção: O conteúdo e as diretrizes entram unificados no parâmetro 'contents'
                response = model.generate_content(
                    contents=[{"role": "user", "parts": [SYSTEM_INSTRUCTION, prompt_final]}],
                    generation_config={"temperature": 0.0}
                )
                
                # Container limpo e isolado para renderização do laudo técnico
                st.markdown('<div class="medical-sheet-output">', unsafe_allow_html=True)
                st.markdown(response.text, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Falha de barramento com o motor de IA: {e}")
    else:
        st.markdown(
            "<div style='color: #64748B; text-align: center; margin-top: 160px; font-family: \"JetBrains Mono\"; font-size: 0.95rem; font-style: italic;'>"
            "[SISTEMA PRONTO]<br>Aguardando submissão de dados clínicos para renderização..."
            "</div>", 
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
