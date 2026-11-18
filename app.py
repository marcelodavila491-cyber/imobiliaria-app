import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse

NOME_EMPRESA = "MMI IMÓVEIS"
WHATSAPP_NUMERO = "5511986738169"
SENHA_ADMIN = "640491"

st.set_page_config(page_title="MMI IMÓVEIS", page_icon="🏢", layout="wide")

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
menu = st.sidebar.radio("Navegação", ["🔍 Vitrine de Imóveis", "➕ Cadastrar Imóvel", "👔 Corretores e Visitas", "💰 Comissões"])
st.sidebar.divider()
st.sidebar.markdown("**Atendimento Direto:**\n📱 (11) 98673-8169")

def tela_login():
    st.warning("🔒 Área restrita da equipe MMI IMÓVEIS.")
    senha = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ADMIN:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta.")

if menu == "🔍 Vitrine de Imóveis":
    st.title(f"🏢 {NOME_EMPRESA} — Encontre seu novo lar")
    c1, c2, c3, c4 = st.columns(4)
    bairro = c1.text_input("Bairro ou Cidade", placeholder="Ex: Tatuapé, Vila Matilde")
    valor_max = c2.number_input("Pacote Máximo (R$)", 500, 50000, 10000, 200)
    quartos = c3.selectbox("Quartos (mínimo)", [1, 2, 3, 4])
    pet = c4.checkbox("Aceita Pet")
    st.divider()

    lista = []
    for im in st.session_state.imoveis:
        pacote = im["aluguel"] + im["condominio"] + im["iptu"]
        if im["status"] != "Disponível":
            continue
        if bairro and bairro.lower() not in im["bairro"].lower() and bairro.lower() not in im["cidade"].lower():
            continue
        if pacote > valor_max or im["quartos"] < quartos:
            continue
        if pet and not im["aceita_pet"]:
            continue
        lista.append(im)

    st.subheader(f"{len(lista)} imóveis disponíveis")
    cols = st.columns(2)
    for i, im in enumerate(lista):
        total = im["aluguel"] + im["condominio"] + im["iptu"]
        col_atual = cols[i % 2]
        col_atual.markdown('<div class="card-imovel">', unsafe_allow_html=True)
        col_atual.image(im["foto"], use_container_width=True)
        col_atual.subheader(im["titulo"])
        col_atual.write(f"📍 **{im['bairro']}**, {im['cidade']} • {im['tipo']}")
        col_atual.write(f"🛏️ {im['quartos']} quartos | 🚗 {im['vagas']} vagas | 🐾 {'Aceita Pet' if im['aceita_pet'] else 'Não aceita pet'}")
        col_atual.markdown(f"<div class='preco'>Total: R$ {total:,.2f} /mês</div>", unsafe_allow_html=True)
        col_atual.caption(f"Aluguel: R$ {im['aluguel']:,.2f} | Condomínio: R$ {im['condominio']:,.2f} | IPTU: R$ {im['iptu']:,.2f}")

        msg_whats = urllib.parse.quote(f"Olá! Vi o imóvel '{im['titulo']}' (Cód #{im['id']}) no site da MMI IMÓVEIS e gostaria de mais informações.")
        col_atual.markdown(f'<a href="https://wa.me{WHATSAPP_NUMERO}?text={msg_whats}" target="_blank" class="btn-whats">💬 Chamar no WhatsApp agora</a>', unsafe_allow_html=True)

        exp = col_atual.expander("📅 Ou agende uma visita pelo site")
        form_v = exp.form(f"visita_{im['id']}")
        nome_cli = form_v.text_input("Seu Nome")
        tel_cli = form_v.text_input("Seu WhatsApp")
        dt_visita = form_v.date_input("Data", min_value=date.today())
        hr_visita = form_v.selectbox("Horário", ["09:00", "11:00", "14:00", "16:00", "17:30"])
        corr = form_v.selectbox("Corretor", [c["nome"] for c in st.session_state.corretores])
        if form_v.form_submit_button("Confirmar Agendamento"):
            if nome_cli and tel_cli:
                st.session_state.visitas.append({"Imóvel": im["titulo"], "Cliente": nome_cli, "WhatsApp": tel_cli, "Data": str(dt_visita), "Hora": hr_visita, "Corretor": corr})
                exp.success("Visita agendada!")
            else:
                exp.error("Preencha nome e WhatsApp.")
        col_atual.markdown('</div>', unsafe_allow_html=True)

elif menu == "➕ Cadastrar Imóvel":
    if not st.session_state.autenticado:
        tela_login()
    else:
        st.title("Cadastrar Imóvel e Proprietário")
        form_im = st.form("cad_imovel")
        col_p1, col_p2 = form_im.columns(2)
        p_nome = col_p1.text_input("Nome do Proprietário*")
        p_tel = col_p2.text_input("WhatsApp do Proprietário*")
        titulo = form_im.text_input("Título do Anúncio*")
        c1, c2, c3 = form_im.columns(3)
        tipo = c1.selectbox("Tipo", ["Apartamento", "Casa", "Studio", "Comercial"])
        bairro = c2.text_input("Bairro*")
        cidade = c3.text_input("Cidade*", value="São Paulo")
        c4, c5, c6 = form_im.columns(3)
        quartos = c4.number_input("Quartos", 0, 10, 2)
        vagas = c5.number_input("Vagas", 0, 10, 1)
        pet = c6.checkbox("Aceita Pet", value=True)
        v1, v2, v3 = form_im.columns(3)
        aluguel = v1.number_input("Aluguel (R$)*", 100.0, 50000.0, 2000.0, 50.0)
        cond = v2.number_input("Condomínio (R$)", 0.0, 20000.0, 400.0, 10.0)
        iptu = v3.number_input("IPTU (R$)", 0.0, 10000.0, 50.0, 10.0)
        arquivo_foto = form_im.file_uploader("Subir foto do celular ou computador", type=["jpg", "jpeg", "png"])
        foto_link = form_im.text_input("Ou cole um link de foto", value="https://unsplash.com")
        if form_im.form_submit_button("Publicar na Vitrine MMI IMÓVEIS"):
            if p_nome and titulo and bairro:
                img = arquivo_foto if arquivo_foto is not None else foto_link
                st.session_state.imoveis.append({"id": len(st.session_state.imoveis) + 101, "titulo": titulo, "tipo": tipo, "bairro": bairro, "cidade": cidade, "aluguel": aluguel, "condominio": cond, "iptu": iptu, "quartos": quartos, "vagas": vagas, "aceita_pet": pet, "proprietario": p_nome, "telefone_prop": p_tel, "foto": img, "status": "Disponível"})
                st.success("Imóvel publicado com sucesso!")
            else:
                st.error("Preencha os campos obrigatórios (*).")

elif menu == "👔 Corretores e Visitas":
    if not st.session_state.autenticado:
        tela_login()
    else:
        st.title("Gestão de Corretores e Visitas")
        aba1, aba2 = st.tabs(["📅 Visitas Agendadas", "👔 Cadastrar Corretor"])
        if st.session_state.visitas:
            aba1.dataframe(pd.DataFrame(st.session_state.visitas), use_container_width=True)
        else:
            aba1.info("Nenhuma visita agendada ainda.")
        form_c = aba2.form("cad_corretor")
        cn = form_c.text_input("Nome do Corretor*")
        cc = form_c.text_input("CRECI*")
        ct = form_c.text_input("WhatsApp")
        cr = form_c.text_input("Região")
        if form_c.form_submit_button("Cadastrar Corretor"):
            if cn and cc:
                st.session_state.corretores.append({"nome": cn, "creci": cc, "telefone": ct, "regiao": cr})
                aba2.success("Corretor salvo!")
        aba2.dataframe(pd.DataFrame(st.session_state.corretores), use_container_width=True)

elif menu == "💰 Comissões":
    if not st.session_state.autenticado:
        tela_login()
    else:
        st.title("Fechamento de Contratos e Comissões")
        disp = [im for im in st.session_state.imoveis if im["status"] == "Disponível"]
        if not disp:
            st.warning("Sem imóveis disponíveis no momento.")
        else:
            form_f = st.form("fechar_contrato")
            opcoes = {f"#{im['id']} - {im['titulo']} (R$ {im['aluguel']:,.2f})": im for im in disp}
            sel = form_f.selectbox("Imóvel Fechado", list(opcoes.keys()))
            im_sel = opcoes[sel]
            inq = form_f.text_input("Nome do Inquilino*")
            corr = form_f.selectbox("Corretor", [c["nome"] for c in st.session_state.corretores])
            dt_ass = form_f.date_input("Data Assinatura", value=date.today())
            dt_vig = form_f.date_input("Início Vigência", value=date.today())
            perc = form_f.slider("Comissão (%)", 50, 100, 100)
if form_f.form_submit_button("Fechar Contrato"):
if inq:
comissao = im_sel["aluguel"] * (perc / 100.0)
repasse = "Dia 01 do próximo mês" if dt_vig.day <= 20 else "Dia 15 do próximo mês"
st.session_state.contratos.append({"Imóvel": im_sel["titulo"], "Inquilino": inq, "Corretor": corr, "Assinatura": str(dt_ass), "Vigência": str(dt_vig), "Comissão (R$)": comissao, "Repasse": repasse})
im_sel["status"] = "Alugado"
st.success(f"Contrato fechado! Comissão: R$ {comissao:,.2f} ({repasse}).")
else:
st.error("Informe o nome do inquilino.")
if st.session_state.contratos:
df = pd.DataFrame(st.session_state.contratos)
st.dataframe(df, use_container_width=True)
st.metric("Total em Comissões", f"R$ {df['Comissão (R$)'].sum():,.2f}")
