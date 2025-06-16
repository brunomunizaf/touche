import io
import streamlit as st

from models import Box
from export.layout import BoxLayout
from export.svg_exporter import SVGExporter

from export.components import CardboardLooseBaseComponent, CardboardLooseTopComponent, CardboardBookTopComponent, InternalLiningBaseComponent, InternalLiningTopComponent, InternalLiningBookTopComponent, CardboardMagnetTopComponent, InternalLiningMagnetTopComponent, ExternalLiningBookTopComponent, ExternalLiningMagnetTopComponent

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
    images = ["images/lose_box.png", "images/book_box.png", "images/magnet_box.png"]
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
    # Export buttons
    st.subheader("Exportar")
    # Only show relevant options for the selected box type
    if box_type == "Tampa Solta":
        st.subheader("Papelão")
        def merged_export():
            thickness = st.session_state['thickness']
            base = CardboardLooseBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
            top = CardboardLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📦 Exportar Base + Tampa Solta (Novo)",
            data=merged_export(),
            file_name=f"{st.session_state['project_name']} | Papelão - Base + Tampa Solta.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Interno")
        def merged_paper_export():
            thickness = st.session_state['thickness']
            paper_base = InternalLiningBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
            paper_top = InternalLiningTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
            layout = BoxLayout([paper_top, paper_base], spacing=20)
            svg_width = max(paper_top.total_width, paper_base.total_width)
            svg_height = paper_top.total_height + paper_base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📩 Exportar Revestimento Interno - Base + Tampa Solta (Novo)",
            data=merged_paper_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Interno - Base + Tampa Solta.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Externo")
        def merged_magnet_external_lining_export():
            thickness = st.session_state['thickness']
            top = ExternalLiningMagnetTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = InternalLiningBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="🎁 Exportar Revestimento Externo - Base + Tampa Imã (Novo)",
            data=merged_magnet_external_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Externo - Base + Tampa Imã.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
    elif box_type == "Tampa Livro":
        st.subheader("Papelão")
        def merged_book_export():
            thickness = st.session_state['thickness']
            top = CardboardBookTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = CardboardLooseBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📦 Exportar Papelão - Base + Tampa Livro (Novo)",
            data=merged_book_export(),
            file_name=f"{st.session_state['project_name']} | Papelão - Base + Tampa Livro.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Interno")
        def merged_book_internal_lining_export():
            thickness = st.session_state['thickness']
            top = InternalLiningBookTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = InternalLiningBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📩 Exportar Revestimento Interno - Base + Tampa Livro (Novo)",
            data=merged_book_internal_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Interno - Base + Tampa Livro.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Externo")
        def merged_book_external_lining_export():
            thickness = st.session_state['thickness']
            top = ExternalLiningBookTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = InternalLiningBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="🎁 Exportar Revestimento Externo - Base + Tampa Livro (Novo)",
            data=merged_book_external_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Externo - Base + Tampa Livro.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
    elif box_type == "Tampa Imã":
        st.subheader("Papelão")
        def merged_magnet_export():
            thickness = st.session_state['thickness']
            top = CardboardMagnetTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = CardboardLooseBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📦 Exportar Papelão - Base + Tampa Imã (Novo)",
            data=merged_magnet_export(),
            file_name=f"{st.session_state['project_name']} | Papelão - Base + Tampa Imã.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Interno")
        def merged_magnet_internal_lining_export():
            thickness = st.session_state['thickness']
            top = InternalLiningMagnetTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = InternalLiningBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="📩 Exportar Revestimento Interno - Base + Tampa Imã (Novo)",
            data=merged_magnet_internal_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Interno - Base + Tampa Imã.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Externo")
        def merged_magnet_external_lining_export():
            thickness = st.session_state['thickness']
            top = ExternalLiningMagnetTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = InternalLiningBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            layout = BoxLayout([top, base], spacing=20)
            svg_width = max(top.total_width, base.total_width)
            svg_height = top.total_height + base.total_height + layout.spacing
            exporter = SVGExporter(svg_width, svg_height)
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        st.download_button(
            label="🎁 Exportar Revestimento Externo - Base + Tampa Imã (Novo)",
            data=merged_magnet_external_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Externo - Base + Tampa Imã.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )