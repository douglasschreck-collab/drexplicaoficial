import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO DE PÁGINA E META
st.set_page_config(
    page_title="RadAI // Premium Reporting", 
    page_icon="🩻", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ESTILIZAÇÃO CSS DE ALTO NÍVEL (Paleta da Marca: Azure, Marinho, Chumbo, Ciano, Off-white)
st.markdown("""
    <style>
        /* Importação de fonte moderna */
        @import url('https://googleapis.com');
        
        /* Reset de fontes global */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC !important; /* Off-white de fundo */
            color: #1E293B !important; /* Cinza chumbo para textos */
        }
        
        /* Header Premium */
        .premium-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); /* Azul Marinho profundo */
            padding: 2.5rem;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
            border-left: 6px solid #06B6D4; /* Detalhe em Ciano */
        }
        .premium-header h1 {
            color: #FFFFFF !important;
            font-weight: 700;
            letter-spacing: -0.05em;
            margin: 0;
            font-size: 2.2rem;
        }
        .premium-header p {
            color: #94A3B8;
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            font-weight: 300;
        }

        /* Cartões de Trabalho (Workspace) */
        .workspace-card {
            background-color: #FFFFFF;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #E2E8F0; /* Azure acinzentado */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            min-height: 520px;
        }
        
        /* Customização dos Inputs de Texto */
        .stTextArea textarea {
            background-color: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
            color: #0F172A !important;
            line-height: 1.6 !important;
            transition: all 0.2s ease;
        }
        .stTextArea textarea:focus {
            border-color: #06B6D4 !important; /* Foco em Ciano */
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15) !important;
        }

        /* Botão Principal Executivo */
        .stButton>button {
            background: linear-gradient(135deg, #06B6D4 0%, #0284C7 100%) !important; /* Ciano para Azul */
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.35) !important;
        }
        
        /* Caixa de Saída do Laudo (Estilo Prancheta Médica) */
        .report-output {
            background-color: #FFFFFF;
            padding: 2.5rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            border-top: 4px solid #0F172A; /* Topo Marinho */
            box-shadow: 0 4px 12px rgba(0,0,0,0.02);
            font-size: 1.05rem;
            line-height: 1.7;
        }
        
        /* Ajustes de labels e textos auxiliares */
        label {
            font-weight: 600 !important;
            color: #334155 !important;
            letter-spacing: -0.01em;
            margin-bottom: 0.5rem !important;
        }
        
        /* Ocultar elementos desnecessários do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. CONEXÃO SEGURA COM A API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API do Gemini não configurada nas configurações secretas.")

# 4. INSTÂNCIAS DE PROMPT DO SISTEMA
SYSTEM_INSTRUCTION = """
Você é um assistente de inteligência artificial especializado em Radiologia e Diagnóstico por Imagem, focado em alta produtividade clínica. Seu objetivo é transformar notas rápidas (ditadas ou escritas) em laudos formais, estruturados e revisados, conforme um radiologista sênior faria.

Diretrizes de Operação:
1. IDIOMA: Identifique o idioma de entrada, mas gere o laudo no idioma explicitamente solicitado pelo médico. Se não especificar, use o mesmo da entrada.
2. NORMAS MUNDIAIS: Estruture o laudo seguindo rigorosamente as recomendações do ACR, ESR e classificações internacionais validadas (BI-RADS, LI-RADS, PI-RADS, TI-RADS, Lung-RADS, etc.).
3. INTERROGAÇÃO DE DADOS FALTANTES: Se faltar critérios essenciais para fechar um score, NÃO invente dados. NUNCA INVENTE DADOS! No topo da sua resposta, antes do laudo, indique de forma proeminente: "⚠️ INFORMAÇÕES NECESSÁRIAS PARA CLASSIFICAÇÃO [NOME DA CLASSIFICAÇÃO]:" e liste as perguntas objetivas com opções de descritores.
4. ESTRUTURA DO LAUDO: Use cabeçalhos claros em Markdown (Markdown clássico sem caixas desnecessárias).
"""

# 5. ESTRUTURA VISUAL DA INTERFACE (UI)
st.markdown("""
    <div class="premium-header">
        <h1>RadAI // Intelligence Suite</h1>
        <p>Plataforma avançada para estruturação de laudos radiológicos e validação de scores internacionais.</p>
    </div>
""", unsafe_allow_html=True)

# Divisão de colunas simétricas e limpas
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Input Clínico")
    
    idioma = st.selectbox(
        "Selecione o idioma de saída do laudo:", 
        ["Mesmo do texto de entrada", "Português", "English", "Español"]
    )
    
    notas_medicas = st.text_area(
        "Notas do Exame / Achados rápidos (ditados ou transcritos):", 
        height=320, 
        placeholder="Ex: US de tireoide: nódulo sólido, hipoecoico no lobo direito, medindo 1.2cm, contornos mal definidos, sem calcificações. Resto normal..."
    )
    
    st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
    processar = st.button("✨ Estruturar e Validar Laudo")
    st.markdown("</div>")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Output Estruturado")
    
    if processar and notas_medicas:
        with st.spinner("Analisando achados médicos e aplicando consensos..."):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    system_instruction=SYSTEM_INSTRUCTION,
                    generation_config={"temperature": 0.0}
                )
                
                prompt_final = notas_medicas if idioma == "Mesmo do texto de entrada" else f"Gere o laudo em {idioma}. Notas: {notas_medicas}"
                response = model.generate_content(prompt_final)
                
                # Renderiza o laudo dentro de um container com visual de folha clínica impressa
                st.markdown(f'<div class="report-output">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erro na comunicação com o motor clínico: {e}")
    else:
        st.markdown(
            "<div style='color: #64748B; text-align: center; margin-top: 150px; font-weight: 300; font-style: italic;'>"
            "Aguardando a inserção de dados na coluna à esquerda para iniciar a estruturação do documento..."
            "</div>", 
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
