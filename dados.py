import streamlit as st

NOME_EMPRESA = "MMI IMÓVEIS"
WHATSAPP_NUMERO = "5511986738169"
SENHA_ADMIN = "640491"

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
