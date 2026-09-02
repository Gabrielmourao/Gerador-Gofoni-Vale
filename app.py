import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime

# 1. Configura a página
st.set_page_config(page_title="Gofoni Advogados - Automação", layout="wide")

# --- A MÁGICA DA MEMÓRIA COMEÇA AQUI ---
# Cria uma memória para o aplicativo não esquecer que gerou os documentos
if 'documentos_prontos' not in st.session_state:
    st.session_state['documentos_prontos'] = False
    st.session_state['nome_cliente'] = ""
# ---------------------------------------

# 2. Lógica da data automática
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

# Título do sistema
st.title("⚖️ Sistema de Geração de Contratos")
st.markdown("Preencha os dados abaixo para gerar a Procuração, Hipossuficiência e Contrato automaticamente.")

# Dados do Cliente
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

# Dados do Contrato
st.header("💰 Dados do Contrato")
col3, col4 = st.columns(2)

with col3:
    porcentagem = st.text_input("Porcentagem de Êxito", value="30% (trinta por cento)")
with col4:
    valor_consulta = st.text_input("Valor Adicional (R$)", value="R$ 300,00")
    valor_consulta_extenso = st.text_input("Valor Adicional por extenso", value="trezentos reais")

st.markdown("---")

# Botão Gerar
if st.button("🚀 GERAR KIT DE DOCUMENTOS", use_container_width=True):
    if nome == "":
        st.error("Por favor, preencha pelo menos o Nome do Cliente!")
    else:
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
            'PORCENTAGEM_HONORARIOS': porcentagem,
            'VALOR_CONSULTA': valor_consulta,
            'VALOR_CONSULTA_EXTENSO': valor_consulta_extenso
        }

        documentos = ['modelo_procuracao.docx', 'modelo_hipossuficiencia.docx', 'modelo_contrato.docx']
        
        try:
            for doc_nome in documentos:
                template = DocxTemplate(doc_nome)
                template.render(dados_cliente)
                novo_nome = doc_nome.replace("modelo_", f"{nome}_")
                template.save(novo_nome)
            
            # Avisa a "memória" que está tudo pronto e guarda o nome do cliente
            st.session_state['documentos_prontos'] = True
            st.session_state['nome_cliente'] = nome
            
            st.success(f"✅ Sucesso! O Kit de {nome} foi gerado!")
            st.balloons()
            
        except Exception as erro:
            st.error(f"Ocorreu um erro: {erro}")

# --- SEÇÃO DE DOWNLOAD FIXA ---
# Como ela está fora do botão de Gerar, ela não some quando a página recarrega!
if st.session_state['documentos_prontos']:
    st.markdown("### 📥 Arquivos Prontos para Download:")
    
    documentos = ['modelo_procuracao.docx', 'modelo_hipossuficiencia.docx', 'modelo_contrato.docx']
    
    # Criamos 3 colunas para colocar um botão do lado do outro (fica mais bonito!)
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    for i, doc_nome in enumerate(documentos):
        novo_nome = doc_nome.replace("modelo_", f"{st.session_state['nome_cliente']}_")
        try:
            with open(novo_nome, "rb") as file:
                # Distribui os botões nas colunas
                if i == 0:
                    col_btn1.download_button(label=f"📄 Procuração", data=file, file_name=novo_nome, use_container_width=True)
                elif i == 1:
                    col_btn2.download_button(label=f"📄 Hipossuficiência", data=file, file_name=novo_nome, use_container_width=True)
                else:
                    col_btn3.download_button(label=f"📄 Contrato", data=file, file_name=novo_nome, use_container_width=True)
        except:
            pass
