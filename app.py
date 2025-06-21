import io
import streamlit as st

from models import Box
from export.layout import BoxLayout, MultiInstanceLayout
from export.svg_exporter import SVGExporter

# Cardboard
from export.components import CardboardBaseComponent
from export.components import CardboardLooseTopComponent
from export.components import CardboardBookTopComponent
from export.components import CardboardMagnetTopComponent

# Internal Lining
from export.components import InternalLiningLooseTopComponent
from export.components import InternalLiningBookTopComponent
from export.components import InternalLiningMagnetTopComponent

# Internal Lining Base
from export.components import InternalLiningBaseForLooseTopComponent
from export.components import InternalLiningBaseForBookTopComponent
from export.components import InternalLiningBaseForMagnetTopComponent

# External Lining
from export.components import ExternalLiningBookTopComponent
from export.components import ExternalLiningMagnetTopComponent
from export.components import ExternalLiningLooseTopComponent
from export.components import ExternalLiningBaseLooseComponent
from export.components import ExternalLiningBaseNonLooseComponent

st.set_page_config(
	page_title="Touché", 
	layout="wide"
)

# Step 1: Select box type
if 'box_type' not in st.session_state:
    st.session_state['box_type'] = None

st.title("Touché | Gerador de linhas de corte e vinco")

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
            base = CardboardBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
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
        def merged_loose_internal_lining_export():
            thickness = st.session_state['thickness']
            paper_base = InternalLiningBaseForLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
            paper_top = InternalLiningLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], thickness)
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
            data=merged_loose_internal_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Interno - Base + Tampa Solta.svg",
            mime="image/svg+xml",
            disabled=not st.session_state['project_name']
        )
        st.subheader("Revestimento Externo")
        def merged_loose_external_lining_export():
            thickness = st.session_state['thickness']
            top = ExternalLiningLooseTopComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness
            )
            base = ExternalLiningBaseLooseComponent(
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
            label="🎁 Exportar Revestimento Externo - Base + Tampa Solta (Novo)",
            data=merged_loose_external_lining_export(),
            file_name=f"{st.session_state['project_name']} | Revestimento Externo - Base + Tampa Solta.svg",
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
            base = CardboardBaseComponent(
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
            base = InternalLiningBaseForBookTopComponent(
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
            base = ExternalLiningBaseNonLooseComponent(
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
            base = CardboardBaseComponent(
                st.session_state['width'],
                st.session_state['height'],
                st.session_state['depth'],
                thickness,
                with_magnets=True
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
            base = InternalLiningBaseForMagnetTopComponent(
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
            base = ExternalLiningBaseNonLooseComponent(
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

    # New section for multiple instance exports
    st.header("4. Exportar Múltiplas Instâncias")
    st.write("Exporte múltiplas instâncias dos elementos com um retângulo representando o papelão completo.")
    
    # Create a dictionary to store export functions
    export_functions = {}
    
    if box_type == "Tampa Solta":
        export_functions = {
            "Papelão - Base + Tampa Solta": lambda: (
                CardboardBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                CardboardLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Interno - Base + Tampa Solta": lambda: (
                InternalLiningBaseForLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                InternalLiningLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Externo - Base + Tampa Solta": lambda: (
                ExternalLiningBaseLooseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                ExternalLiningLooseTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            )
        }
    elif box_type == "Tampa Livro":
        export_functions = {
            "Papelão - Base + Tampa Livro": lambda: (
                CardboardBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                CardboardBookTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Interno - Base + Tampa Livro": lambda: (
                InternalLiningBaseForBookTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                InternalLiningBookTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Externo - Base + Tampa Livro": lambda: (
                ExternalLiningBaseNonLooseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                ExternalLiningBookTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            )
        }
    elif box_type == "Tampa Imã":
        export_functions = {
            "Papelão - Base + Tampa Imã": lambda: (
                CardboardBaseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'], with_magnets=True),
                CardboardMagnetTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Interno - Base + Tampa Imã": lambda: (
                InternalLiningBaseForMagnetTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                InternalLiningMagnetTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            ),
            "Revestimento Externo - Base + Tampa Imã": lambda: (
                ExternalLiningBaseNonLooseComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness']),
                ExternalLiningMagnetTopComponent(st.session_state['width'], st.session_state['height'], st.session_state['depth'], st.session_state['thickness'])
            )
        }
    
    # Dropdown to select export type
    selected_export = st.selectbox(
        "Escolha o tipo de exportação:",
        list(export_functions.keys()),
        key="multi_export_type"
    )
    
    # Number input for instances
    instances = st.number_input(
        "Número de instâncias:",
        min_value=1,
        max_value=20,
        value=4,
        key="multi_instances"
    )
    
    # Function to create multi-instance export
    def create_multi_instance_export():
        if selected_export in export_functions:
            components = export_functions[selected_export]()
            layout = MultiInstanceLayout(list(components), instances, spacing=20, margin=30)
            
            exporter = SVGExporter(layout.total_width, layout.total_height)
            
            # Add all components
            for comp, x, y in layout.arrange():
                exporter.add_component(comp, x, y)
            
            buffer = io.StringIO()
            exporter.dwg.write(buffer)
            return buffer.getvalue()
        return ""
    
    # Download button for multi-instance export
    st.download_button(
        label=f"📦 Exportar {instances} Instâncias - {selected_export}",
        data=create_multi_instance_export(),
        file_name=f"{st.session_state['project_name']} | {instances}x {selected_export}.svg",
        mime="image/svg+xml",
        disabled=not st.session_state['project_name']
    )