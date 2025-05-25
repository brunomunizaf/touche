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

st.title("Touché | Caixas Cartonadas")

with st.sidebar:
	st.title("📦 Dados do projeto")

	project_name = st.text_input(
		"Nome do projeto/cliente",
		placeholder="Ex: Melissa_Casamento"
  )

	width = st.number_input(
		"Largura (cm)", 
		min_value=1.0, 
		step=0.1, 
		value=20.0
	)

	height = st.number_input(
		"Altura (cm)", 
		min_value=1.0, 
		step=0.1, 
		value=15.0
	)

	depth = st.number_input(
		"Profundidade (cm)", 
		min_value=1.0, 
		step=0.1, 
		value=10.0
	)

	thickness = st.number_input(
		"Espessura do papelão (mm)", 
		min_value=0.5, 
		step=0.1, 
		value=1.9
	)

box = Box(project_name, width, height, depth, thickness)

def gerar_download(label, file_label, export_func, *args):
    try:
        bundle = export_func(box, *args, returning=True)
        file_name = f"{project_name} | {file_label}.svg" if project_name else "arquivo.svg"

        st.download_button(
            label=f"📥 {label}",
            data=bundle.svg_string,
            file_name=file_name,
            mime="image/svg+xml",
            disabled=not project_name
        )
    except NotImplementedError as e:
        st.warning(f"⚠️ {label}: {str(e)}")
    except Exception as e:
        st.error(f"❌ Erro ao gerar '{label}': {str(e)}")
col1, col2, col3 = st.columns(3)

with col1:
	with st.expander("Papelão", expanded=True):
		gerar_download(
			"📦 Base", "Papelão - Base", 
			cardboard_base
		)
		gerar_download(
			"📦 Base (com imã)", "Papelão - Base com imã", 
			cardboard_base_with_magnets
		)
		gerar_download(
			"📦 Tampa Solta", "Papelão - Tampa Solta", 
			cardboard_top_lose
		)
		gerar_download(
			"📦 Tampa Livro", "Papelão - Tampa Livro", 
			cardboard_top_book
		)
		gerar_download(
			"📦 Tampa Imã", "Papelão - Tampa Imã", 
			cardboard_top_magnet
		)

with col2:
	with st.expander("Revestimento Interno", expanded=True):
		gerar_download(
			"📩 Base (tampa solta)", "Revestimento Interno - Base (tampa solta)", 
			paper_base_lose, 
			CoverSide.INTERNAL
		)
		gerar_download(
			"📩 Base (exceto tampa solta)", "Revestimento Interno - Base (exceto tampa solta)", 
			paper_base_not_lose, 
			CoverSide.INTERNAL
		)
		gerar_download(
			"📩 Tampa Solta", "Revestimento Interno - Tampa Solta", 
			paper_top_lose, 
			CoverSide.INTERNAL
		)
		gerar_download(
			"📩 Tampa Livro", "Revestimento Interno - Tampa Livro", 
			paper_top_book, 
			CoverSide.INTERNAL
		)
		gerar_download(
			"📩 Tampa Imã", "Revestimento Interno - Tampa Imã", 
			paper_top_magnet, 
			CoverSide.INTERNAL
		)

with col3:
	with st.expander("Revestimento Externo", expanded=True):
		gerar_download(
			"🎁 Base (tampa solta)", "Revestimento Externo - Base (tampa solta)", 
			paper_base_lose, 
			CoverSide.EXTERNAL
		)
		gerar_download(
			"🎁 Base (exceto tampa solta)", "Revestimento Externo - Base (exceto tampa solta)", 
			paper_base_not_lose, 
			CoverSide.EXTERNAL
		)
		gerar_download(
			"🎁 Tampa Solta", "Revestimento Externo - Tampa Solta", 
			paper_top_lose, 
			CoverSide.EXTERNAL
		)
		gerar_download(
			"🎁 Tampa Livro", "Revestimento Externo - Tampa Livro", 
			paper_top_book, 
			CoverSide.EXTERNAL
		)
		gerar_download(
			"🎁 Tampa Imã", "Revestimento Externo - Tampa Imã", 
			paper_top_magnet, 
			CoverSide.EXTERNAL
		)