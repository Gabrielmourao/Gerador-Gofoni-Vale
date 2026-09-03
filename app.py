import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import google.generativeai as genai

# 1. Configura a página e a memória
st.set_page_config(page_title="Gofoni Advogados - Automação", layout="wide")

if 'documentos_prontos' not in st.session_state:
    st.session_state['documentos_prontos'] = False
    st.session_state['nome_cliente'] = ""

# 2. Conecta a API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Erro de conexão com a API.")

# 3. Lógica da data
meses_pt = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}
data_atual = datetime.now()
dia = data_atual.strftime("%d")
mes = meses_pt[data_atual.month]
ano = data_atual.year
data_formatada = f"{dia} de {mes} de {ano}"

st.title("⚖️ Sistema de Geração de Contratos")
st.markdown("Preencha os dados abaixo para gerar a Procuração, Hipossuficiência e Contrato.")

# --- SEÇÃO 1: Dados do Cliente ---
st.header("👤 Dados do Cliente")
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome Completo")
    nacionalidade = st.text_input("Nacionalidade", value="brasileiro(a)")
    estado_civil = st.selectbox("Estado Civil", ["solteiro(a)", "casado(a)", "divorciado(a)", "viúvo(a)", "união estável"])
    rg = st.text_input("RG")
    orgao_emissor = st.text_input("Órgão Emissor", value="Detran/RJ")

with col2:
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço Completo (Rua, nº, Bairro, CEP)")
    telefone = st.text_input("Telefone / WhatsApp")
    cidade_assinatura = st.text_input("Cidade da Assinatura", value="Nova Iguaçu/RJ")
    data = st.text_input("Data do Documento", value=data_formatada)

# --- SEÇÃO 2: Condições de Pagamento ---
st.header("💰 Condições de Pagamento")

col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    st.markdown("**Cláusula 3ª (Honorários / Êxito)**")
    input_clausula_3 = st.text_area("Descreva a forma de cobrança do êxito ou valor principal:", 
                                    placeholder="Ex: 30% sobre o proveito econômico da causa ao final do processo.")

with col_ia2:
    st.markdown("**Cláusula 4ª (Atendimentos e Despesas)**")
    input_clausula_4 = st.text_area("Descreva a cobrança inicial ou de despesas:", 
                                    placeholder="Ex: 1500 de entrada no pix hoje e 3x de 500 no boleto todo dia 10.")

st.markdown("---")

# --- SEÇÃO 3: Geração dos Documentos ---
if st.button("🚀 GERAR KIT DE DOCUMENTOS", use_container_width=True):
    if nome == "" or input_clausula_3 == "" or input_clausula_4 == "":
        st.error("Por favor, preencha o Nome do Cliente e os campos de Condições de Pagamento.")
    else:
        with st.spinner("Processando e gerando documentos..."):
            try:
                # Prompt para a Cláusula 3
                prompt_3 = f"""
                Você é um advogado brasileiro redigindo um contrato de honorários.
                Escreva APENAS o texto contínuo da Cláusula de Honorários Contratuais, baseada neste acordo: "{input_clausula_3}".
                Escreva valores em números e por extenso. 
                NÃO coloque o título da cláusula, NÃO converse comigo e NÃO use formatação (sem negrito ou asteriscos). Apenas o texto.
                """
                resposta_3 = modelo_ia.generate_content(prompt_3)
                texto_final_3 = resposta_3.text.strip()

                # Prompt para a Cláusula 4
                prompt_4 = f"""
                Você é um advogado brasileiro redigindo um contrato de honorários.
                Escreva APENAS o texto contínuo da Cláusula de Atendimentos e Despesas, baseada neste acordo: "{input_clausula_4}".
                Escreva valores em números e por extenso. 
                NÃO coloque o título da cláusula, NÃO converse comigo e NÃO use formatação (sem negrito ou asteriscos). Apenas o texto.
                """
                resposta_4 = modelo_ia.generate_content(prompt_4)
                texto_final_4 = resposta_4.text.strip()
                
                # Juntando tudo para mandar pro Word
                dados_cliente = {
                    'NOME_CLIENTE': nome.upper(),
                    'NACIONALIDADE': nacionalidade,
                    'ESTADO_CIVIL': estado_civil,
                    'RG': rg,
                    'ORGAO_EMISSOR': orgao_emissor,
                    'CPF': cpf,
                    'ENDERECO': endereco,
                    'TELEFONE': telefone,
                    'CIDADE_ASSINATURA': cidade_assinatura,
                    'DATA': data,
                    'TEXTO_CLAUSULA_3': texto_final_3,
                    'TEXTO_CLAUSULA_4': texto_final_4
                }

                documentos = ['modelo_procuracao.docx', 'modelo_hipossuficiencia.docx', 'modelo_contrato.docx']
                
                for doc_nome in documentos:
                    template = DocxTemplate(doc_nome)
                    template.render(dados_cliente)
                    novo_nome = doc_nome.replace("modelo_", f"{nome}_")
                    template.save(novo_nome)
                
                st.session_state['documentos_prontos'] = True
                st.session_state['nome_cliente'] = nome
                
                st.success(f"✅ Kit de documentos gerado com sucesso.")
                
            except Exception as erro:
                st.error(f"Ocorreu um erro durante a geração: {erro}")
                
                # O CÓDIGO DETETIVE ENTRA EM AÇÃO AQUI:
                st.info("🔍 DIAGNÓSTICO: Buscando diretamente no Google quais modelos a sua chave tem acesso...")
                try:
                    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.write("**Estes são os modelos que apareceram:**")
                    st.code(modelos_disponiveis)
                except Exception as erro2:
                    st.error(f"Não conseguimos puxar a lista. Verifique se a sua chave está 100% certa no Streamlit Secrets. Detalhe: {erro2}")

# --- SEÇÃO 4: Download Fixo ---
if st.session_state['documentos_prontos']:
    st.markdown("### 📥 Arquivos Prontos para Download:")
    documentos = ['modelo_procuracao.docx', 'modelo_hipossuficiencia.docx', 'modelo_contrato.docx']
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    for i, doc_nome in enumerate(documentos):
        novo_nome = doc_nome.replace("modelo_", f"{st.session_state['nome_cliente']}_")
        try:
            with open(novo_nome, "rb") as file:
                if i == 0:
                    col_btn1.download_button(label=f"📄 Procuração", data=file, file_name=novo_nome, use_container_width=True)
                elif i == 1:
                    col_btn2.download_button(label=f"📄 Hipossuficiência", data=file, file_name=novo_nome, use_container_width=True)
                else:
                    col_btn3.download_button(label=f"📄 Contrato", data=file, file_name=novo_nome, use_container_width=True)
        except:
            pass
