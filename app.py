import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime # <- Biblioteca nova para lidar com datas!

# 1. Configura a página para ficar mais larga e com título
st.set_page_config(page_title="Gofoni Advogados - Automação", layout="wide")

# 2. Lógica para pegar a data atual e formatar em português
meses_pt = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}
data_atual = datetime.now()
dia = data_atual.strftime("%d") # Pega o dia com dois dígitos (ex: 02)
mes = meses_pt[data_atual.month] # Puxa o nome do mês do nosso dicionário
ano = data_atual.year
data_formatada = f"{dia} de {mes} de {ano}" # Monta a frase final!

# Título do nosso sistema
st.title("⚖️ Sistema de Geração de Contratos")
st.markdown("Preencha os dados abaixo para gerar a Procuração, Hipossuficiência e Contrato automaticamente.")

# Seção 1: Dados do Cliente
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
    cidade_assinatura = st.text_input("Cidade da Assinatura", value="Nova Iguaçu - RJ")
    # Repare que substituímos o texto fixo pela variável 'data_formatada'
    data = st.text_input("Data do Documento", value=data_formatada)

# Seção 2: Dados Financeiros
st.header("💰 Dados do Contrato")
col3, col4 = st.columns(2)

with col3:
    porcentagem = st.text_input("Porcentagem de Êxito", value="30% (trinta por cento)")
with col4:
    valor_consulta = st.text_input("Valor Adicional (R$)", value="R$ 300,00")
    valor_consulta_extenso = st.text_input("Valor Adicional por extenso", value="trezentos reais")

st.markdown("---")

# O Botão Mágico
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
                template = DocxTemplate(f"modelos/{doc_nome}")
                template.render(dados_cliente)
                novo_nome = doc_nome.replace("modelo_", f"{nome}_")
                template.save(f"saida/{novo_nome}")
            
            st.success(f"✅ Sucesso! O Kit de {nome} foi gerado lá na pasta 'saida'!")
            st.balloons()
            
        except Exception as erro:
            st.error(f"Ocorreu um erro: {erro}")