import io
import zipfile
import streamlit as st

from models import Box, ExportBundle
from enums import TopType, CoverSide

# Paper

from svg.paper.base import export as export_paper_base
from svg.paper.top_book import export as export_paper_top_book
from svg.paper.top_lose import export as export_paper_top_lose
from svg.paper.top_magnet import export as export_paper_top_magnet

from preview.paper.base import preview_internal as preview_paper_base_internal
from preview.paper.top_book import preview_internal as preview_paper_top_book_internal
from preview.paper.top_lose import preview_internal as preview_paper_top_lose_internal
from preview.paper.top_magnet import preview_internal as preview_paper_top_magnet_internal

from preview.paper.base import preview_external as preview_paper_base_external
from preview.paper.top_book import preview_external as preview_paper_top_book_external
from preview.paper.top_lose import preview_external as preview_paper_top_lose_external
from preview.paper.top_magnet import preview_external as preview_paper_top_magnet_external

# Cardboard

from svg.cardboard.base import export as export_cardboard_base
from svg.cardboard.top_book import export as export_cardboard_top_book
from svg.cardboard.top_lose import export as export_cardboard_top_lose
from svg.cardboard.top_magnet import export as export_cardboard_top_magnet

from preview.cardboard.base import preview as preview_cardboard_base
from preview.cardboard.top_book import preview as preview_cardboard_top_book
from preview.cardboard.top_lose import preview as preview_cardboard_top_lose
from preview.cardboard.top_magnet import preview as preview_cardboard_top_magnet

with st.sidebar:
	st.header("📦 Dados do projeto")
	client_name = st.text_input("Nome do cliente/projeto", placeholder="Ex: The Shining Paper")
	width = st.number_input("Largura (cm)", min_value=1.0, step=0.1, value=20.0)
	height = st.number_input("Altura (cm)", min_value=1.0, step=0.1, value=15.0)
	depth = st.number_input("Profundidade (cm)", min_value=1.0, step=0.1, value=10.0)
	thickness = st.number_input("Espessura do papelão (mm)", min_value=0.5, step=0.1, value=1.9)

	if client_name:
		box = Box(
			client_name=client_name,
			width=width,
			height=height,
			depth=depth,
			thickness=thickness
		)

		# export_paper_base(box, CoverSide.EXTERNAL)
		# export_paper_base(box, CoverSide.INTERNAL)
		# export_paper_top_lose(box, CoverSide.EXTERNAL)
		# export_paper_top_lose(box, CoverSide.INTERNAL)

		paper_top_book_external_bundle = export_paper_top_book(box, CoverSide.EXTERNAL, returning=True)
		paper_top_book_internal_bundle = export_paper_top_book(box, CoverSide.INTERNAL, returning=True)
		paper_top_magnet_external_bundle = export_paper_top_magnet(box, CoverSide.EXTERNAL, returning=True)
		paper_top_magnet_internal_bundle = export_paper_top_magnet(box, CoverSide.INTERNAL, returning=True)
		cardboard_top_book_bundle = export_cardboard_top_book(box, returning=True)
		cardboard_top_lose_bundle = export_cardboard_top_lose(box, returning=True)
		cardboard_top_magnet_bundle = export_cardboard_top_magnet(box, returning=True)
		cardboard_base_bundle = export_cardboard_base(box, returning=True)

		files = {
			paper_top_book_external_bundle.file_name: paper_top_book_external_bundle.svg_string,
			paper_top_book_internal_bundle.file_name: paper_top_book_internal_bundle.svg_string,
			paper_top_magnet_external_bundle.file_name: paper_top_magnet_external_bundle.svg_string,
			paper_top_magnet_internal_bundle.file_name: paper_top_magnet_internal_bundle.svg_string,
			cardboard_top_book_bundle.file_name: cardboard_top_book_bundle.svg_string,
			cardboard_top_lose_bundle.file_name: cardboard_top_lose_bundle.svg_string,
			cardboard_top_magnet_bundle.file_name: cardboard_top_magnet_bundle.svg_string,
			cardboard_base_bundle.file_name: cardboard_base_bundle.svg_string
		}

		zip_buffer = io.BytesIO()
		with zipfile.ZipFile(zip_buffer, "w") as zip_file:
		    for nome, conteudo in files.items():
		        zip_file.writestr(nome, conteudo)
		
		zip_buffer.seek(0)

		st.download_button(
			label="📥 Baixar todas as linhas de corte/vinco",
			data=zip_buffer,
			file_name=box.client_name,
			mime="application/zip"
		)

st.title("Touché | Caixas Cartonadas")
#st.header("📐 Renderização em tempo real")
st.subheader(f"(L){width:.1f}cm × (A){height:.1f}cm × (P){depth:.1f}cm, (E){thickness:.1f}mm")
st.subheader("📦 Papelão")

drawings_cardboard = {
    "Base": preview_cardboard_base,
    "Tampa solta": preview_cardboard_top_lose,
    "Tampa livro": preview_cardboard_top_book,
    "Tampa imã": preview_cardboard_top_magnet
}

drawing_cardboard_items = list(drawings_cardboard.items())

for nome, funcao in drawing_cardboard_items:
    st.markdown(f"### {nome}")
    fig = funcao(width, height, depth, thickness)
    st.pyplot(fig)

# st.subheader("📥 Revestimento interno")

# drawings_internal_paper = {
#     "Base": preview_paper_base_internal,
#     "Tampa solta": preview_paper_top_lose_internal,
#     "Tampa livro": preview_paper_top_book_internal,
#     "Tampa imã": preview_paper_top_magnet_internal
# }

# drawing_internal_paper_items = list(drawings_internal_paper.items())

# for i in range(0, len(drawing_internal_paper_items), 3):
#     cols = st.columns(3)
#     for col, (nome, funcao) in zip(cols, drawing_internal_paper_items[i:i+3]):
#         with col:
#             st.markdown(f"**{nome}**")
#             fig = funcao(width, height, depth, thickness)
#             st.pyplot(fig)

# st.subheader("📩 Revestimento externo")

# drawings_external_paper = {
#     "Base": preview_paper_base_external,
#     "Tampa solta": preview_paper_top_lose_external,
#     "Tampa livro": preview_paper_top_book_external,
#     "Tampa imã": preview_paper_top_magnet_external
# }

# drawing_external_paper_items = list(drawings_external_paper.items())

# for i in range(0, len(drawing_external_paper_items), 3):
#     cols = st.columns(3)
#     for col, (nome, funcao) in zip(cols, drawing_external_paper_items[i:i+3]):
#         with col:
#             st.markdown(f"**{nome}**")
#             fig = funcao(width, height, depth, thickness)
#             st.pyplot(fig)