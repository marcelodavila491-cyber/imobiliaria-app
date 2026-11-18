import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse

NOME_EMPRESA = "MMI IMÓVEIS"
WHATSAPP_NUMERO = "5511986738169"
SENHA_ADMIN = "640491"

st.set_page_config(page_title=f"{NOME_EMPRESA} - Aluguel e Venda", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button { background-color: #102a43; color: #f0b429; border-radius: 8px; border: 1px solid #f0b429; font-weight: bold; }
    .card-imovel { background-color: white; padding: 20px; border-radius: 12px; border-top: 4px solid #f0b429; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .preco { font-size: 22px; font-weight: bold; color: #102a43; margin-top: 8px; }
    .btn-whats { display: inline-block; width: 100%; text-align: center; background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

if "imoveis" not in st.session_state:
    st.session_state.imoveis = [
        {"id": 101, "titulo": "Apartamento Moderno próximo ao Metrô", "tipo": "Apartamento", "bairro": "Vila Matilde", "cidade": "São Paulo", "aluguel": 2200.0, "condominio": 450.0, "iptu": 80.0, "quartos": 2, "vagas": 1, "aceita_pet": True, "proprietario": "Carlos Mendes", "telefone_prop": "(11) 99999-1111", "foto": "https://unsplash.com", "status": "Disponível"},
        {"id": 102, "titulo": "Casa Espaçosa com Quintal Gourmet", "tipo": "Casa", "bairro": "Tatuapé", "cidade": "São Paulo", "aluguel": 3800.0, "condominio": 0.0, "iptu": 150.0, "quartos": 3, "vagas": 2, "aceita_pet": True, "proprietario": "Fernanda Lima", "telefone_prop": "(11) 98888-2222", "foto": "https://unsplash.com", "status": "Disponível"}
    ]

if "corretores" not in st.session_state:
    st.session_state.corretores = [{"nome": "Marcelo D'Avila", "creci": "Ativo", "telefone": "(11) 98673-8169", "regiao": "São Paulo"}]

if "visitas" not in st.session_state:
    st.session_state.visitas = []

if "contratos" not in st.session_state:
    st.session_state.contratos = []

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

st.sidebar.title(f"🏢 {NOME_EMPRESA}")
st.sidebar.caption("Locação e Venda Digital")
menu = st.sidebar.radio("Navegação", ["🔍 Vitrine de Imóveis", "➕ Cadastrar Imóvel (Restrito)", "👔 Corretores e Visitas (Restrito)", "💰 Fechamento e Comissões (Restrito)"])
st.sidebar.divider()
st.sidebar.markdown("**Atendimento Direto:**\n📱 (11) 98673-8169")

def verificar_acesso():
    if st.session_state.autenticado:
        return True
    st.warning("🔒 Área exclusiva da equipe MMI IMÓVEIS.")
    senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar no Painel"):
        if senha_digitada == SENHA_ADMIN:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

if menu == "🔍 Vitrine de Imóveis":
    st.title(f"🏢 {NOME_EMPRESA} — Encontre seu novo lar")
    c1, c2, c3, c4 = st.columns(4)
    bairro = c1.text_input("Bairro ou Cidade", placeholder="Ex: Tatuapé, Vila Matilde")
    valor_max = c2.number_input("Pacote Máximo (R$)", 500, 50000, 10000, 200)
    quartos = c3.selectbox("Quartos (mínimo)", [1, 2, 3, 4])
    pet = c4.checkbox("Aceita Pet")
    st.divider()
    lista = [im for im in st.session_state.imoveis if im["status"] == "Disponível" and (not bairro or bairro.lower() in im["bairro"].lower() or bairro.lower() in im["cidade"].lower()) and (im["aluguel"] + im["condominio"] + im["iptu"]) <= valor_max and im["quartos"] >= quartos and (not pet or im["aceita_pet"])]
    st.subheader(f"{len(lista)} imóveis disponíveis")
    cols = st.columns(2)
    for i, im in enumerate(lista):
        total = im["aluguel"] + im["condominio"] + im["iptu"]
        with cols[i % 2]:
            st.markdown('<div class="card-imovel">', unsafe_allow_html=True)
            st.image(im["foto"], use_container_width=True)
            st.subheader(im["titulo"])
            st.write(f"📍 **{im['bairro']}**, {im['cidade']} • {im['tipo']}")
            st.write(f"🛏️ {im['quartos']} quartos | 🚗 {im['vagas']} vagas | 🐾 {'Aceita Pet' if im['aceita_pet'] else 'Não aceita pet'}")
            st.markdown(f"<div class='preco'>Total: R$ {total:,.2f} /mês</div>", unsafe_allow_html=True)
            st.caption(f"Aluguel: R$ {im['aluguel']:,.2f} | Condomínio: R$ {im['condominio']:,.2f} | IPTU: R$ {im['iptu']:,.2f}")
            msg_whats = urllib.parse.quote(f"Olá! Vi o imóvel '{im['titulo']}' (Cód #{im['id']}) no site da MMI IMÓVEIS e gostaria de mais informações.")
            st.markdown(f'<a href="https://wa.me{WHATSAPP_NUMERO}?text={msg_whats}" target="_blank" class="btn-whats">💬 Chamar no WhatsApp agora</a>', unsafe_allow_html=True)
            with st.expander("📅 Ou agende uma visita pelo site"):
                with st.form(f"visita_{im['id']}"):
                    nome_cli = st.text_input("Seu Nome")
                    tel_cli = st.text_input("Seu WhatsApp")
                    dt_visita = st.date_input("Data", min_value=date.today())
                    hr_visita = st.selectbox("Horário", ["09:00", "11:00", "14:00", "16:00", "17:30"])
                    corr = st.selectbox("Corretor", [c["nome"] for c in st.session_state.corretores])
                    if st.form_submit_button("Confirmar Agendamento"):
                        if nome_cli and tel_cli:
                            st.session_state.visitas.append({"Imóvel": im["titulo"], "Cliente": nome_cli, "WhatsApp": tel_cli, "Data": str(dt_visita), "Hora": hr_visita, "Corretor": corr})
                            st.success("Visita agendada! Nossa equipe entrará em contato.")
                        else:
                            st.error("Preencha nome e WhatsApp.")
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "➕ Cadastrar Imóvel (Restrito)":
    if verificar_acesso():
        st.title("Cadastrar Imóvel e Proprietário")
        with st.form("cad_imovel"):
            col_p1, col_p2 = st.columns(2)
            p_nome = col_p1.text_input("Nome do Proprietário*")
            p_tel = col_p2.text_input("WhatsApp do Proprietário*")
            titulo = st.text_input("Título do Anúncio*")
            c1, c2, c3 = st.columns(3)
            tipo = c1.selectbox("Tipo", ["Apartamento", "Casa", "Studio", "Comercial"])
            bairro = c2.text_input("Bairro*")
            cidade = c3.text_input("Cidade*", value="São Paulo")
            c4, c5, c6 = st.columns(3)
            quartos = c4.number_input("Quartos", 0, 10, 2)
            vagas = c5.number_input("Vagas", 0, 10, 1)
            pet = c6.checkbox("Aceita Pet", value=True)
            v1, v2, v3 = st.columns(3)
            aluguel = v1.number_input("Aluguel (R$)*", 100.0, 50000.0, 2000.0, 50.0)
            cond = v2.number_input("Condomínio (R$)", 0.0, 20000.0, 400.0, 10.0)
            iptu = v3.number_input("IPTU (R$)", 0.0, 10000.0, 50.0, 10.0)
            arquivo_foto = st.file_uploader("Subir foto do celular ou computador", type=["jpg", "jpeg", "png"])
            foto_link = st.text_input("Ou cole um link de foto", value="https://unsplash.com")
            if st.form_submit_button("Publicar na Vitrine MMI IMÓVEIS"):
                if p_nome and titulo and bairro:
                    imagem_final = arquivo_foto if arquivo_foto is not None else foto_link
                    st.session_state.imoveis.append({"id": len(st.session_state.imoveis) + 101, "titulo": titulo, "tipo": tipo, "bairro": bairro, "cidade": cidade, "aluguel": aluguel, "condominio": cond, "iptu": iptu, "quartos": quartos, "vagas": vagas, "aceita_pet": pet, "proprietario": p_nome, "telefone_prop": p_tel, "foto": imagem_final, "status": "Disponível"})
                    st.success("Imóvel publicado com sucesso na vitrine!")
                else:
                    st.error("Preencha os campos obrigatórios (*).")

elif menu == "👔 Corretores e Visitas (Restrito)":
    if verificar_acesso():
        st.title("Gestão de Corretores e Visitas")
        aba1, aba2 = st.tabs(["📅 Visitas Agendadas", "👔 Cadastrar Corretor"])
        with aba1:
            if st.session_state.visitas:
                st.dataframe(pd.DataFrame(st.session_state.visitas), use_container_width=True)
            else:
                st.info("Nenhuma visita agendada ainda.")
        with aba2:
            with st.form("cad_corretor"):
                cn = st.text_input("Nome do Corretor*")
                cc = st.text_input("CRECI*")
                ct = st.text_input("WhatsApp")
                cr = st.text_input("Região")
                if st.form_submit_button("Cadastrar Corretor"):
                    if cn and cc:
                        st.session_state.corretores.append({"nome": cn, "creci": cc, "telefone": ct, "regiao": cr})
                        st.success("Corretor salvo!")
            st.dataframe(pd.DataFrame(st.session_state.corretores), use_container_width=True)

elif menu == "💰 Fechamento e Comissões (Restrito)":
    if verificar_acesso():
        st.title("Fechamento de Contratos e Comissões")
        disp = [im for im in st.session_state.imoveis if im["status"] == "Disponível"]
        if not disp:
            st.warning("Sem imóveis disponíveis no momento.")
        else:
            with st.form("fechar_contrato"):
                opcoes = {f"#{im['id']} - {im['titulo']} (R$ {im['aluguel']:,.2f})": im for im in disp}
                sel = st.selectbox("Imóvel Fechado", list(opcoes.keys()))
                im_sel = opcoes[sel]
                inq = st.text_input("Nome do Inquilino*")
                corr = st.selectbox("Corretor", [c["nome"] for c in st.session_state.corretores])
dt_ass = st.date_input("Data Assinatura", value=date.today())
dt_vig = st.date_input("Início Vigência", value=date.today())
perc = st.slider("Comissão (%)", 50, 100, 100)
if st.form_submit_button("Fechar Contrato"):
if inq:
comissao = im_sel["aluguel"] * (perc / 100.0)
repasse = "Dia 01 do próximo mês" if dt_vig.day <= 20 else "Dia 15 do próximo mês"
st.session_state.contratos.append({"Imóvel": im_sel["titulo"], "Inquilino": inq, "Corretor": corr, "Assinatura": str(dt_ass), "Vigência": str(dt_vig), "Comissão (R$)": comissao, "Repasse": repasse})
im_sel["status"] = "Alugado"
st.success(f"Contrato fechado! Comissão: R$ {comissao:,.2f} ({repasse}).")
if st.session_state.contratos:
df = pd.DataFrame(st.session_state.contratos)
st.dataframe(df, use_container_width=True)
st.metric("Total em Comissões", f"R$ {df['Comissão (R$)'].sum():,.2f}")
