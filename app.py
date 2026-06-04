import streamlit as st
import google.generativeai as genai

# Configuração de Segurança (Usando Secrets do Streamlit Cloud)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Erro na configuração da API. Verifique os Secrets.")

st.set_page_config(layout="wide", page_title="Copiloto de Código")
st.title("🤖 Gerenciador Inteligente de Código")

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    codigo_original = st.text_area("1. Código Original", height=300)
    instrucoes = st.text_area("2. O que deseja atualizar?", height=150)
    
    if st.button("ANALISAR E GERAR"):
        with st.spinner("O Gemini está analisando..."):
            prompt = f"Analise este código:\n{codigo_original}\n\nInstrução:\n{instrucoes}\n\n1. Explique o que será feito (sem mostrar código).\n2. Forneça apenas o código atualizado final."
            resposta = model.generate_content(prompt)
            st.session_state.resposta = resposta.text
            # Preenche automaticamente o campo 4 com a resposta
            st.session_state.codigo_sugerido = resposta.text

with col2:
    st.write("3. Interação:")
    st.info(st.session_state.get("resposta", "Aguardando instrução..."))
    
    # Campo 4: Código Atualizado
    codigo_novo = st.text_area("4. Código Atualizado", value=st.session_state.get("codigo_sugerido", ""), height=300)
    
    # Botão de download em vez de salvar no disco
    st.download_button(
        label="5. BAIXAR CÓDIGO ATUALIZADO",
        data=codigo_novo,
        file_name="codigo_atualizado.py",
        mime="text/x-python"
    )

resultado_final = st.text_area("5. Resultado Final (Cópia para clipboard)", value=codigo_novo, height=200)
