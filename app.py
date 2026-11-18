import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse
from dados import NOME_EMPRESA, WHATSAPP_NUMERO, SENHA_ADMIN, ESTILO_CSS, iniciar_banco, conectar

st.set_page_config(page_title=NOME_EMPRESA, page_icon="🏢", layout="wide")
st.markdown(ESTILO_CSS, unsafe_allow_html=True)
iniciar_banco()
db = conectar()

st.sidebar.title(f"🏢 {NOME_EMPRESA}")
menu = st.sidebar.radio("Menu", ["🔍 Vitrine", "➕ Cadastrar Imóvel", "👔 Corretores e Visitas", "💰 Comissões"])
st.sidebar.markdown("**WhatsApp:** (11) 98673-8169")

def verificar_senha():
    if st.session_state.autenticado:
        return True
    s = st.text_input("Senha da equipe MMI IMÓVEIS:", type="password")
    if st.button("Entrar") and s == SENHA_ADMIN:
        st.session_state.autenticado = True
        st.rerun()
    return False

if menu == "🔍 Vitrine":
    st.title(f"🏢 {NOME_EMPRESA} — Encontre seu imóvel")
    c1, c2, c3 = st.columns(3)
    bairro = c1.text_input("Bairro ou Cidade")
    vmax = c2.number_input("Pacote Máximo (R$)", 500, 50000, 10000, 200)
    pet = c3.checkbox("Aceita Pet")
    st.divider()

    cols = st.columns(2)
    idx = 0
    for im in st.session_state.imoveis:
        total = im["aluguel"] + im["condominio"] + im["iptu"]
        if im["status"] != "Disponível" or total > vmax or (pet and not im["aceita_pet"]):
            continue
        if bairro and bairro.lower() not in im["bairro"].lower() and bairro.lower() not in im["cidade"].lower():
            continue
        col = cols[idx % 2]
        idx += 1
        col.markdown('<div class="card-imovel">', unsafe_allow_html=True)
        col.image(im["foto"], use_container_width=True)
        col.subheader(im["titulo"])
        col.write(f"📍 {im['bairro']}, {im['cidade']} | 🛏️ {im['quartos']} quartos | 🚗 {im['vagas']} vagas")
        col.markdown(f"<div class='preco'>Total: R$ {total:,.2f} /mês</div>", unsafe_allow_html=True)
        col.caption(f"Aluguel: R$ {im['aluguel']:,.2f} | Cond: R$ {im['condominio']:,.2f} | IPTU: R$ {im['iptu']:,.2f}")
        msg = urllib.parse.quote(f"Olá! Vi o imóvel '{im['titulo']}' (#{im['id']}) na MMI IMÓVEIS.")
        col.markdown(f'<a href="https://wa.me{WHATSAPP_NUMERO}?text={msg}" target="_blank" class="btn-whats">💬 Chamar no WhatsApp</a>', unsafe_allow_html=True)
        with col.expander("📅 Agendar Visita"):
            with st.form(f"v_{im['id']}"):
                nc = st.text_input("Seu Nome")
                tc = st.text_input("Seu WhatsApp")
                dt = st.date_input("Data", min_value=date.today())
                if st.form_submit_button("Agendar") and nc and tc:
                    db.table("visitas").insert({"imovel": im["titulo"], "cliente": nc, "whatsapp": tc, "data_visita": str(dt)}).execute()
                    st.success("Visita agendada!")
                    st.rerun()
        col.markdown('</div>', unsafe_allow_html=True)

elif menu == "➕ Cadastrar Imóvel" and verificar_senha():
    st.title("Cadastrar Imóvel")
    with st.form("cad_im"):
        pn = st.text_input("Proprietário*")
        pt = st.text_input("WhatsApp Proprietário*")
        tit = st.text_input("Título*")
        c1, c2, c3 = st.columns(3)
        tipo = c1.selectbox("Tipo", ["Apartamento", "Casa", "Studio", "Comercial"])
        bairro = c2.text_input("Bairro*")
        cidade = c3.text_input("Cidade*", value="São Paulo")
        c4, c5, c6 = st.columns(3)
        q = c4.number_input("Quartos", 0, 10, 2)
        v = c5.number_input("Vagas", 0, 10, 1)
        pet = c6.checkbox("Aceita Pet", value=True)
        v1, v2, v3 = st.columns(3)
        alu = v1.number_input("Aluguel*", 100.0, 50000.0, 2000.0, 50.0)
        cond = v2.number_input("Condomínio", 0.0, 20000.0, 400.0, 10.0)
        iptu = v3.number_input("IPTU", 0.0, 10000.0, 50.0, 10.0)
        foto_url = st.text_input("Link da Foto", value="https://unsplash.com")
        if st.form_submit_button("Publicar") and pn and tit and bairro:
            db.table("imoveis").insert({"titulo": tit, "tipo": tipo, "bairro": bairro, "cidade": cidade, "aluguel": alu, "condominio": cond, "iptu": iptu, "quartos": q, "vagas": v, "aceita_pet": pet, "proprietario": pn, "telefone_prop": pt, "foto": foto_url, "status": "Disponível"}).execute()
            st.success("Imóvel salvo no banco de dados!")
            st.rerun()

elif menu == "👔 Corretores e Visitas" and verificar_senha():
    st.title("Corretores e Visitas")
    if st.session_state.visitas:
        st.dataframe(pd.DataFrame(st.session_state.visitas), use_container_width=True)
    with st.form("cad_cor"):
        cn = st.text_input("Nome Corretor*")
        cc = st.text_input("CRECI*")
        ct = st.text_input("WhatsApp")
        if st.form_submit_button("Salvar Corretor") and cn and cc:
            db.table("corretores").insert({"nome": cn, "creci": cc, "telefone": ct, "regiao": "SP"}).execute()
            st.success("Corretor salvo!")
            st.rerun()
    if st.session_state.corretores:
        st.dataframe(pd.DataFrame(st.session_state.corretores), use_container_width=True)

elif menu == "💰 Comissões" and verificar_senha():
    st.title("Fechamento e Comissões")
    disp = [im for im in st.session_state.imoveis if im["status"] == "Disponível"]
    if disp:
        with st.form("fechar"):
            op = {f"#{im['id']} - {im['titulo']}": im for im in disp}
            im_s = op[st.selectbox("Imóvel", list(op.keys()))]
            inq = st.text_input("Inquilino*")
            nomes_c = [c["nome"] for c in st.session_state.corretores] or ["Marcelo D'Avila"]
            cor = st.selectbox("Corretor", nomes_c)
            vig = st.date_input("Início Vigência", value=date.today())
            perc = st.slider("Comissão (%)", 50, 100, 100)
            if st.form_submit_button("Fechar Contrato") and inq:
                com = im_s["aluguel"] * (perc / 100.0)
                rep = "Dia 01 próximo mês" if vig.day <= 20 else "Dia 15 próximo mês"
                db.table("contratos").insert({"imovel": im_s["titulo"], "inquilino": inq, "corretor": cor, "comissao": com, "repasse": rep}).execute()
                db.table("imoveis").update({"status": "Alugado"}).eq("id", im_s["id"]).execute()
                st.success(f"Fechado! Comissão: R$ {com:,.2f} ({rep})")
                st.rerun()
    if st.session_state.contratos:
        df = pd.DataFrame(st.session_state.contratos)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Comissões", f"R$ {df['comissao'].sum():,.2f}")
