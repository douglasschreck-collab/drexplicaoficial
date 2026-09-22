import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO PREMIUM DE DESIGN (Cores da Marca)
st.set_page_config(page_title="RadAI - Laudos Inteligentes", page_icon="🩻", layout="wide")

st.markdown("""
    <style>
        /* Fundo e texto base (Off-white e Cinza Chumbo) */
        .stApp { background-color: #FAFAFA; color: #1E293B; }
        /* Barra lateral (Azure acinzentado e Azul Marinho) */
        section[data-testid="stSidebar"] { background-color: #E2E8F0; }
        /* Títulos e Destaques (Azul Marinho e Ciano) */
        h1, h2, h3 { color: #0F172A; font-family: 'Helvetica Neue', sans-serif; }
        .stButton>button { 
            background-color: #0284C7; color: white; border-radius: 6px; 
            border: none; font-weight: bold; width: 100%;
        }
        .stButton>button:hover { background-color: #0369A1; color: #E0F2FE; }
        /* Áreas de texto */
        textarea { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. AUTENTICAÇÃO DA API DO GEMINI
# A chave de API será configurada de forma segura na nuvem (Passo 2)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave de API do Gemini não configurada nas configurações secretas.")

# 3. PROMPT DO SISTEMA (Baseado no seu modelo validado)
SYSTEM_INSTRUCTION = """
Você é um assistente de inteligência artificial especializado em Radiologia e Diagnóstico por Imagem. Seu papel é atuar como um radiologista sênior, transformando notas rápidas em laudos formais, estruturados e revisados.

Diretrizes de Operação:
1. IDIOMA: Identifique o idioma de entrada. Gere o laudo no idioma explicitamente solicitado pelo médico. Caso não haja especificação, mantenha o idioma da entrada.
2. NORMAS MUNDIAIS: Estruture o laudo seguindo rigorosamente as diretrizes atualizadas do ACR e ESR (BI-RADS, LI-RADS, PI-RADS, TI-RADS, Lung-RADS, etc.).
3. ZERO ALUCINAÇÃO: Se os dados forem insuficientes para calcular um score, NUNCA invente dados. Interrompa a conclusão do laudo e insira o alerta "⚠️ INFORMAÇÕES NECESSÁRIAS PARA CLASSIFICAÇÃO [NOME]", listando as perguntas pendentes em tópicos com opções de escolha.
4. PADRÃO DE FORMATAÇÃO: Use Markdown para estruturar os cabeçalhos: Tipo de Exame, Técnica, Achados, Impressão Diagnóstica e Classificação.
"""

# 4. INTERFACE DO USUÁRIO (UI)
st.title("🩻 RadAI: Assistente de Laudos Estruturados")
st.caption("Produtividade clínica com inteligência artificial para radiologistas seniores")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Entrada de Dados")
    idioma = st.selectbox("Idioma do Laudo Final:", ["Mesmo do texto de entrada", "Português", "English", "Español"])
    
    # Suporta texto digitado ou ditado (copiado de um transcritor)
    notas_medicas = st.text_area("Digite ou cole as notas do exame (achados rápidos):", height=300, 
                                  placeholder="Ex: US de tireoide: nódulo sólido, hipoecoico no lobo direito, medindo 1.2cm...")
    
    gerar_laudo = st.button("Estruturar e Revisar Laudo")

with col2:
    st.subheader("Laudo Formal Gerado")
    if gerar_laudo and notas_medicas:
        with st.spinner("Processando achados e validando scores..."):
            try:
                # Inicializa o modelo Gemini 1.5 Pro com temperatura zero para máxima precisão clínica
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    system_instruction=SYSTEM_INSTRUCTION,
                    generation_config={"temperature": 0.0}
                )
                
                prompt_final = notas_medicas if idioma == "Mesmo do texto de entrada" else f"Gere o laudo em {idioma}. Notas: {notas_medicas}"
                response = model.generate_content(prompt_final)
                
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.info("O laudo estruturado aparecerá aqui assim que você clicar no botão à esquerda.")
