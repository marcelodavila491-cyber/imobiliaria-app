import streamlit as st
from supabase import create_client

NOME_EMPRESA = "MMI IMÓVEIS"
WHATSAPP_NUMERO = "5511986738169"
SENHA_ADMIN = "640491"

SUPABASE_URL = "https://ljnozxgcbnjllbdqivab.supabase.co"
SUPABASE_KEY = "sb_publishable_zlpN6FMkBJ45aMIlHNFsbA_K7i8APrR"

@st.cache_resource
def conectar():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

ESTILO_CSS = """
<style>
.main { background-color: #f4f6f9; }
.stButton>button { background-color: #102a43; color: #f0b429; border-radius: 8px; border: 1px solid #f0b429; font-weight: bold; }
.card-imovel { background-color: white; padding: 20px; border-radius: 12px; border-top: 4px solid #f0b429; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }
.preco { font-size: 22px; font-weight: bold; color: #102a43; margin-top: 8px; }
.btn-whats { display: inline-block; width: 100%; text-align: center; background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 10px 0; }
</style>
"""

def iniciar_banco():
    db = conectar()
    st.session_state.imoveis = db.table("imoveis").select("*").execute().data
    st.session_state.corretores = db.table("corretores").select("*").execute().data
    st.session_state.visitas = db.table("visitas").select("*").execute().data
    st.session_state.contratos = db.table("contratos").select("*").execute().data
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
