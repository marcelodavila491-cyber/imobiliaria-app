import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ImóvelFácil", page_icon="🏠", layout="wide")

st.markdown("""
    <style>
    .stButton>button { background-color: #3f51b5; color: white; border-radius: 8px; font-weight: bold; }
    .card-imovel { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 15px; }
    .preco { font-size: 22px; font-weight: bold; color: #1a237e; }
    </style>
""", unsafe_allow_html=True)

if "imoveis" not in st.session_state:
    st.session_state.imoveis = [
        {
            "id": 101,
            "titulo": "Apartamento Moderno próximo ao Metrô",
            "tipo": "Apartamento",
            "bairro": "Vila Matilde",
            "cidade": "São Paulo",
            "aluguel": 2200.0,
            "condominio": 450.0,
            "iptu": 80.0,
            "quartos": 2,
            "vagas": 1,
            "aceita_pet": True,
            "proprietario": "Carlos Mendes",
            "telefone_prop": "(11) 99999-1111",
            "foto": "https://unsplash.com",
            "status": "Disponível"
        },
        {
            "id": 102,
            "titulo": "Casa Espaçosa com Quintal Gourmet",
            "tipo": "Casa",
            "bairro": "Tatuapé",
            "cidade": "São Paulo",
            "aluguel": 3800.0,
            "condominio": 0.0,
            "iptu": 150.0,
            "quartos": 3,
            "vagas": 2,
            "aceita_pet": True,
            "proprietario": "Fernanda Lima",
            "telefone_prop": "(11) 98888-2222",
            "foto": "https://unsplash.com",
            "status": "Disponível"
        }
    ]

if "corretores" not in st.session_state:
    st.session_state.corretores = [{"nome": "Marcelo D'Avila", "creci": "123456-F", "telefone": "(11) 97777-3333", "regiao": "Zona Leste"}]

if "visitas" not in st.session_state:
    st.session_state.visitas = []

if "contratos" not in st.session_state:
    st.session_state.contratos = []

st.sidebar.title("🏠 ImóvelFácil")
menu = st.sidebar.radio("Menu", ["🔍 Buscar Imóveis", "➕ Cadastrar Imóvel", "👔 Corretores e Visitas", "💰 Comissões"])

if menu == "🔍 Buscar Imóveis":
    st.title("Encontre seu novo lar")
    c1, c2, c3, c4 = st.columns(4)
    bairro = c1.text_input("Bairro ou Cidade")
    valor_max = c2.number_input("Pacote Máximo (R$)", 500, 50000, 10000, 200)
    quartos = c3.selectbox("Quartos (mínimo)", [1, 2, 3, 4])
    pet = c4.checkbox("Aceita Pet")

    st.divider()
    lista = [
        im for im in st.session_state.imoveis
        if im["status"] == "Disponível"
        and (not bairro or bairro.lower() in im["bairro"].lower() or bairro.lower() in im["cidade"].lower())
        and (im["aluguel"] + im["condominio"] + im["iptu"]) <= valor_max
        and im["quartos"] >= quartos
        and (not pet or im["aceita_pet"])
    ]

    st.subheader(f"{len(lista)} imóveis disponíveis")
    cols = st.columns(2)
    for i, im in enumerate(lista):
        total = im["aluguel"] + im["condominio"] + im["iptu"]
        with cols[i % 2]:
            st.markdown('<div class="card-imovel">', unsafe_allow_html=True)
            st.image(im["foto"], use_container_width=True)
            st.subheader(im["titulo"])
            st.write(f"📍 {im['bairro']}, {im['cidade']} | 🛏️ {im['quartos']} quartos | 🚗 {im['vagas']} vagas")
            st.markdown(f"<div class='preco'>Total: R$ {total:,.2f} /mês</div>", unsafe_allow_html=True)
            st.caption(f"Aluguel: R$ {im['aluguel']:,.2f} | Condomínio: R$ {im['condominio']:,.2f} | IPTU: R$ {im['iptu']:,.2f}")

            with st.expander("📅 Agendar Visita"):
                with st.form(f"visita_{im['id']}"):
                    nome_cli = st.text_input("Seu Nome")
                    tel_cli = st.text_input("Seu WhatsApp")
                    dt_visita = st.date_input("Data", min_value=date.today())
                    hr_visita = st.selectbox("Horário", ["09:00", "11:00", "14:00", "16:00"])
                    corr = st.selectbox("Corretor", [c["nome"] for c in st.session_state.corretores])
                    if st.form_submit_button("Confirmar"):
                        if nome_cli and tel_cli:
                            st.session_state.visitas.append({
                                "Imóvel": im["titulo"], "Cliente": nome_cli, "WhatsApp": tel_cli,
                                "Data": str(dt_visita), "Hora": hr_visita, "Corretor": corr
                            })
                            st.success("Visita agendada!")
                        else:
                            st.error("Preencha nome e WhatsApp.")
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "➕ Cadastrar Imóvel":
    st.title("Cadastrar Imóvel e Proprietário")
    with st.form("cad_imovel"):
        p_nome = st.text_input("Nome do Proprietário*")
        p_tel = st.text_input("WhatsApp do Proprietário*")
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
        foto = st.text_input("Link da Foto", value="https://unsplash.com")

        if st.form_submit_button("Salvar Imóvel"):
            if p_nome and titulo and bairro:
                st.session_state.imoveis.append({
                    "id": len(st.session_state.imoveis) + 101,
                    "titulo": titulo, "tipo": tipo, "bairro": bairro, "cidade": cidade,
                    "aluguel": aluguel, "condominio": cond, "iptu": iptu,
                    "quartos": quartos, "vagas": vagas, "aceita_pet": pet,
                    "proprietario": p_nome, "telefone_prop": p_tel, "foto": foto, "status": "Disponível"
                })
                st.success("Imóvel cadastrado com sucesso!")
            else:
                st.error("Preencha os campos obrigatórios (*).")

elif menu == "👔 Corretores e Visitas":
    st.title("Corretores e Visitas")
    aba1, aba2 = st.tabs(["📅 Visitas Agendadas", "👔 Cadastrar Corretor"])
    with aba1:
        if st.session_state.visitas:
            st.dataframe(pd.DataFrame(st.session_state.visitas), use_container_width=True)
        else:
            st.info("Nenhuma visita agendada.")
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

elif menu == "💰 Comissões":
    st.title("Fechamento e Comissões")
    disp = [im for im in st.session_state.imoveis if im["status"] == "Disponível"]
    if not disp:
        st.warning("Sem imóveis disponíveis.")
    else:
        with st.form("fechar_contrato"):
            opcoes = {f"#{im['id']} - {im['titulo']} (R$ {im['aluguel']:,.2f})": im for im in disp}
            sel = st.selectbox("Imóvel", list(opcoes.keys()))
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
                    st.session_state.contratos.append({
                        "Imóvel": im_sel["titulo"], "Inquilino": inq, "Corretor": corr,
                        "Assinatura": str(dt_ass), "Vigência": str(dt_vig),
                        "Comissão (R$)": comissao, "Repasse": repasse
                    })
                    im_sel["status"] = "Alugado"
                    st.success(f"Contrato fechado! Comissão: R$ {comissao:,.2f} ({repasse}).")

    if st.session_state.contratos:
        df = pd.DataFrame(st.session_state.contratos)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Comissões", f"R$ {df['Comissão (R$)'].sum():,.2f}")
