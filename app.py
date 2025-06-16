import io
import zipfile
import streamlit as st

from models import Box, ExportBundle
from enums import TopType, CoverSide

# Paper

from paper.top_book import export as paper_top_book
from paper.top_lose import export as paper_top_lose
from paper.top_magnet import export as paper_top_magnet

from paper.base_lose import export as paper_base_lose
from paper.base_not_lose import export as paper_base_not_lose

# Cardboard

from cardboard.base import export as cardboard_base
from cardboard.top_book import export as cardboard_top_book
from cardboard.top_lose import export as cardboard_top_lose
from cardboard.top_magnet import export as cardboard_top_magnet
from cardboard.base import export_with_magnets as cardboard_base_with_magnets

st.set_page_config(
	page_title="Touché", 
	layout="wide"
)

# Step 1: Select box type
if 'box_type' not in st.session_state:
    st.session_state['box_type'] = None

st.title("Touché | Caixas Cartonadas")

step = 1
if st.session_state['box_type'] is None:
    st.header("1. Qual tipo de caixa você quer construir?")
    box_types = ["Tampa Solta", "Tampa Livro", "Tampa Imã"]
    images = ["lose_box.png", "book_box.png", "magnet_box.png"]
    cols = st.columns(3)
    for i, (col, box_type, img) in enumerate(zip(cols, box_types, images)):
        with col:
            st.image(img, caption=box_type, use_container_width=True)
            if st.button(f"Selecionar: {box_type}", key=f"select_{i}"):
                st.session_state['box_type'] = box_type
                st.rerun()
else:
    box_type = st.session_state['box_type']
    st.success(f"Tipo de caixa selecionado: {box_type}")
    if st.button("Trocar tipo de caixa", key="change_type"):
        st.session_state['box_type'] = None
        st.rerun()
    step = 2

# Step 2: Enter dimensions
if step == 2:
    st.header("2. Informe as dimensões da caixa")
    with st.form("dimensions_form"):
        project_name = st.text_input(
            "Nome do projeto/cliente",
            placeholder="Ex: Melissa_Casamento",
            key="project_name"
        )
        width = st.number_input(
            "Largura (cm)", min_value=1.0, step=0.1, value=20.0, key="width")
        height = st.number_input(
            "Altura (cm)", min_value=1.0, step=0.1, value=15.0, key="height")
        depth = st.number_input(
            "Profundidade (cm)", min_value=1.0, step=0.1, value=10.0, key="depth")
        thickness = st.number_input(
            "Espessura do papelão (mm)", min_value=0.5, step=0.1, value=1.9, key="thickness")
        submitted = st.form_submit_button("Próximo")
        if submitted:
            st.session_state['dimensions_done'] = True
            st.rerun()
    if st.session_state.get('dimensions_done'):
        step = 3

# Step 3: Show relevant export options
if step == 3:
    st.header("3. Exportar linhas de corte")
    box = Box(
        st.session_state['project_name'],
        st.session_state['width'],
        st.session_state['height'],
        st.session_state['depth'],
        st.session_state['thickness']
    )
    def gerar_download(label, file_label, export_func, *args):
        try:
            bundle = export_func(box, *args, returning=True)
            file_name = f"{st.session_state['project_name']} | {file_label}.svg" if st.session_state['project_name'] else "arquivo.svg"
            st.download_button(
                label=f"📥 {label}",
                data=bundle.svg_string,
                file_name=file_name,
                mime="image/svg+xml",
                disabled=not st.session_state['project_name']
            )
        except NotImplementedError as e:
            st.warning(f"⚠️ {label}: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro ao gerar '{label}': {str(e)}")
    # Only show relevant options for the selected box type
    if box_type == "Tampa Solta":
        st.subheader("Papelão")
        gerar_download("📦 Base", "Papelão - Base", cardboard_base)
        gerar_download("📦 Tampa Solta", "Papelão - Tampa Solta", cardboard_top_lose)
        st.subheader("Revestimento Interno")
        gerar_download("📩 Base (tampa solta)", "Revestimento Interno - Base (tampa solta)", paper_base_lose, CoverSide.INTERNAL)
        gerar_download("📩 Tampa Solta", "Revestimento Interno - Tampa Solta", paper_top_lose, CoverSide.INTERNAL)
        st.subheader("Revestimento Externo")
        gerar_download("🎁 Base (tampa solta)", "Revestimento Externo - Base (tampa solta)", paper_base_lose, CoverSide.EXTERNAL)
        gerar_download("🎁 Tampa Solta", "Revestimento Externo - Tampa Solta", paper_top_lose, CoverSide.EXTERNAL)
    elif box_type == "Tampa Livro":
        st.subheader("Papelão")
        gerar_download("📦 Base", "Papelão - Base", cardboard_base)
        gerar_download("📦 Tampa Livro", "Papelão - Tampa Livro", cardboard_top_book)
        st.subheader("Revestimento Interno")
        gerar_download("📩 Base (exceto tampa solta)", "Revestimento Interno - Base (exceto tampa solta)", paper_base_not_lose, CoverSide.INTERNAL)
        gerar_download("📩 Tampa Livro", "Revestimento Interno - Tampa Livro", paper_top_book, CoverSide.INTERNAL)
        st.subheader("Revestimento Externo")
        gerar_download("🎁 Base (exceto tampa solta)", "Revestimento Externo - Base (exceto tampa solta)", paper_base_not_lose, CoverSide.EXTERNAL)
        gerar_download("🎁 Tampa Livro", "Revestimento Externo - Tampa Livro", paper_top_book, CoverSide.EXTERNAL)
    elif box_type == "Tampa Imã":
        st.subheader("Papelão")
        gerar_download("📦 Base (com imã)", "Papelão - Base com imã", cardboard_base_with_magnets)
        gerar_download("📦 Tampa Imã", "Papelão - Tampa Imã", cardboard_top_magnet)
        st.subheader("Revestimento Interno")
        gerar_download("📩 Base (exceto tampa solta)", "Revestimento Interno - Base (exceto tampa solta)", paper_base_not_lose, CoverSide.INTERNAL)
        gerar_download("📩 Tampa Imã", "Revestimento Interno - Tampa Imã", paper_top_magnet, CoverSide.INTERNAL)
        st.subheader("Revestimento Externo")
        gerar_download("🎁 Base (exceto tampa solta)", "Revestimento Externo - Base (exceto tampa solta)", paper_base_not_lose, CoverSide.EXTERNAL)
        gerar_download("🎁 Tampa Imã", "Revestimento Externo - Tampa Imã", paper_top_magnet, CoverSide.EXTERNAL)