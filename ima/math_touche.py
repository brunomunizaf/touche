from io import StringIO
import svgwrite
import matplotlib.patches as patches

def export_to_svg(path, width, height, depth, thickness, tongue_height=None):
    # Conversão para milímetros
    W = width * 10
    H = height * 10
    D = depth * 10
    T = thickness

    if tongue_height is not None:
        TH = tongue_height
    else:
        TH = D - 5

    margin = 5

    SPACING = 5
    x0 = 0
    x1 = x0 + W + 15

    raio = 7

    total_height = max(H + 2 * D, 3 * SPACING + TH + H + D + H + 10)
    total_width = W + 2 * D + margin + W

    dwg = svgwrite.Drawing(
        path,
        size=(f"{total_width + 500}mm", f"{total_height + 100}mm"),
        viewBox=f"0 0 {total_width} {total_height}"
    )

    def add_vinco(x0, y0, x1, y1):
        dwg.add(dwg.polyline([
            (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 
            stroke="red", 
            fill="none", 
            stroke_width='0.1'
        ))

    def draw_rect(x, y, w, h):
        dwg.add(dwg.rect(
            insert=(x, y), 
            size=(w, h), 
            fill='none', 
            stroke='black', 
            stroke_width=0.1
        ))

    def draw_top(x_offset, y_offset):
        y_lingua = 0
        y_base_sup = y_lingua + TH + SPACING
        y_lombada = y_base_sup + H + SPACING
        y_base_inf = y_lombada + D + SPACING
        y_end = y_base_inf + H + 10

        x_lingua = x0 + 2 * D + W + margin 
        draw_rect(x_lingua, y_lingua, W + 15, TH)  # língua
        draw_rect(x_lingua, y_base_sup, W + 15, H)    # base superior
        draw_rect(x_lingua, y_lombada, W + 15, D)     # lombada
        draw_rect(x_lingua, y_base_inf, W + 15, H + 10)    # base inferior
    
        magnets_path = dwg.path(stroke="black", fill="none", stroke_width='0.1')

        if TH > 70:
            cy = 30
        else:
            cy = (y_base_sup - 5)/2

        tampaX0 = 2 * D + W + margin
        tampaXF = tampaX0 + W + 15

        if W + 15 > 100:
            cx1 = tampaX0 + ((tampaXF - tampaX0)/4)
            cx2 = tampaXF - ((tampaXF - tampaX0)/4)
            magnets_path.push(
                "M", cx1 + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx1 - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx1 + raio, cy   # Arco de volta até a direita
            )
            magnets_path.push(
                "M", cx2 + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx2 - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx2 + raio, cy   # Arco de volta até a direita
            )
        else:
            cx = (x1 - x0) / 2
            magnets_path.push(
                "M", cx + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx + raio, cy   # Arco de volta até a direita
            )
        dwg.add(magnets_path)

    def draw_base(x_offset, y_offset):
        x0 = x_offset + D
        y0 = D
        x1 = x0 + W
        y1 = y0 + H
        xL = x0 - D
        xR = x1 + D
        yT = y1 + D
        yB = y0 - D

        add_vinco(x0, y0, x1, y1)

        path = dwg.path(stroke="black", fill="none", stroke_width='0.1')

        path.push("M", x0, y1)
        path.push("L", x0 - T, y1, x0 - T, y1 + D/2, x0, y1 + D/2, x0, y1 + D,
                  x1, y1 + D, x1, y1 + D/2, x1 + T, y1 + D/2, x1 + T, y1, x1, y1)

        path.push("M", x0, y0)
        path.push("L", x0 - T, y0, x0 - T, y0 - D/2, x0, y0 - D/2, x0, y0 - D,
                  x1, y0 - D, x1, y0 - D/2, x1 + T, y0 - D/2, x1 + T, y0, x1, y0)

        path.push("M", x0, y0)
        path.push("L", x0 - D/2, y0, x0 - D/2, y0 - T, xL, y0 - T,
                  xL, y1 + T, x0 - D/2, y1 + T, x0 - D/2, y1, x0, y1)

        path.push("M", x1, y0)
        path.push("L", xR - D/2, y0, xR - D/2, y0 - T, xR, y0 - T,
                  xR, y1 + T, xR - D/2, y1 + T, xR - D/2, y1, x1, y1)

        dwg.add(path)

        magnets_path = dwg.path(stroke="red", fill="none", stroke_width='0.1')

        if TH > 70:
            cy = y0 - 30
        else:
            cy = y0 / 2

        if W + 15 > 100:
            cx1 = x0 + ((x1 - x0)/4)
            cx2 = x1 - ((x1 - x0)/4)
            magnets_path.push(
                "M", cx1 + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx1 - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx1 + raio, cy   # Arco de volta até a direita
            )
            magnets_path.push(
                "M", cx2 + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx2 - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx2 + raio, cy   # Arco de volta até a direita
            )
        else:
            cx = (x1 - x0) / 2
            magnets_path.push(
                "M", cx + raio, cy,  # Move para a borda direita do círculo
                "A", raio, raio, 0, 1, 0, cx - raio, cy,  # Arco até a borda esquerda
                "A", raio, raio, 0, 1, 0, cx + raio, cy   # Arco de volta até a direita
            )
        dwg.add(magnets_path)

    draw_base(0, 0)
    draw_top(0, 0)
    dwg.save()
    #svg_io = StringIO()
    #dwg.write(svg_io)
    #return svg_io.getvalue()

def draw_preview_base(ax, width, height, depth, thickness, tongue_height=None, tongue_height_var=None):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    W = width * 10
    H = height * 10
    D = depth * 10
    T = thickness
    D2 = D / 2

    if tongue_height is None:
        TH = D - 5
    else:
        TH = tongue_height * 10

    x0, y0 = 0, 0
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    xb = x1 + D

    raio = 7

    # Aba superior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y1, y1, y1 + D2, y1 + D2, y1 + D, y1 + D, y1 + D2, y1 + D2, y1, y1
    ], 'black', linewidth=1)

    # Aba inferior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0
    ], 'black', linewidth=1)

    if TH > 70:
        cy = y0 - 30
    else:
        cy = (y0 - D) / 2

    if W + 15 > 100:
        cx1 = (x1 - x0) / 4
        cx2 = ((x1 - x0) / 4) * 3
        circulo_a = patches.Circle((cx1, cy), raio, edgecolor='red', facecolor='none', linewidth=1)
        circulo_b = patches.Circle((cx2, cy), raio, edgecolor='red', facecolor='none', linewidth=1)
        ax.add_patch(circulo_a)
        ax.add_patch(circulo_b)
    else:
        cx = (x1 - x0) / 2
        circulo = patches.Circle((cx, cy), raio, edgecolor='red', facecolor='none', linewidth=1)
        ax.add_patch(circulo)

    # Aba esquerda
    ax.plot([
        x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)

    ax.text(xL, (y0 + y1) / 2, f"{(H + (2 * T))/10:.1f} cm", fontsize=8, color='black', ha='right', va='center', rotation=90)

    # Aba direita
    ax.plot([
        x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)

    # Base (vinco)
    ax.plot([
        x0, x1, x1, x0, x0
    ], [
        y0, y0, y1, y1, y0
    ], 'red', linewidth=1)
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)
    ax.text(x1 - 22, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

    # No final de draw_preview_base(...)
    x_center = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    y_center = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2

    # Texto com medida
    ax.text((x0 + x1) / 2, y1 + D, f"{(W - (2 * T))/10:.1f} cm", ha='center', va='bottom', fontsize=8, color='black')

    largura_total = W + 2 * D
    x_ext_esq = x0 - D
    x_ext_dir = x1 + D
    y_ref = y0 - D - 25  # abaixo das abas inferiores


def draw_preview_top(ax, width, height, depth, tongue_height=None, tongue_height_var=None):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    W = (width * 10) + 15       # largura da tampa (mm)
    H = height * 10             # altura da tampa (mm)
    D = depth * 10              # profundidade da lombada (mm)

    if tongue_height is None:
        TH = D - 5
    else:
        TH = tongue_height * 10  # altura da língua (mm)
        print(TH)

    SPACING = 5
    y_lingua = 0
    y_base_sup = y_lingua + TH + SPACING
    y_lombada = y_base_sup + H + SPACING
    y_base_inf = y_lombada + D + SPACING
    y_end = y_base_inf + H + 10

    x0 = 0
    x1 = x0 + W
    
    # Raio em mm
    raio = 7
    
    if TH > 70:
        cy = 30
    else:
        cy = (y_base_sup - SPACING) / 2
    
    if W > 100:
        cx1 = ((x1 - x0) / 4) * 3
        cx2 = (x1 - x0) / 4
        circulo_a = patches.Circle((cx1, cy), raio, edgecolor='black', facecolor='none', linewidth=1)
        circulo_b = patches.Circle((cx2, cy), raio, edgecolor='black', facecolor='none', linewidth=1)
        ax.add_patch(circulo_a)
        ax.add_patch(circulo_b)
    else:
        cx = (x1 - x0) / 2
        circulo = patches.Circle((cx, cy), raio, edgecolor='black', facecolor='none', linewidth=1)
        ax.add_patch(circulo)
    
    # Desenho das partes (agora retângulos empilhados verticalmente)
    ax.plot([x0, x1, x1, x0, x0], [y_lingua, y_lingua, TH, TH, y_lingua], 'black', linewidth=1)
    ax.plot([x0, x1, x1, x0, x0], [y_base_sup, y_base_sup, y_base_sup + H, y_base_sup + H, y_base_sup], 'black', linewidth=1)
    ax.plot([x0, x1, x1, x0, x0], [y_lombada, y_lombada, y_lombada + D, y_lombada + D, y_lombada], 'black', linewidth=1)
    ax.plot([x0, x1, x1, x0, x0], [y_base_inf, y_base_inf, y_base_inf + H, y_base_inf + H, y_base_inf], 'black', linewidth=1)
    
    # 📏 Anotações de tamanho vertical
    ax.annotate(
        f"{(y_base_sup - y_lingua - SPACING)/10:.1f} cm",
        xy=(0, 0),
        xytext=(x1 + 8, (y_lingua + y_base_sup)/2), 
        va='center', 
        fontsize=8, 
        color="black"
    )
    ax.annotate(
        f"{(y_lombada - y_base_sup - SPACING)/10:.1f} cm", 
        xy=(0, 0),
        xytext=(x1 + 8, (y_base_sup + y_lombada)/2),
        va='center', 
        fontsize=8, 
        color="black"
    )
    ax.annotate(
        f"{(y_base_inf - y_lombada - SPACING)/10:.1f} cm", 
        xy=(0, 0),
        xytext=(x1 + 8, (y_lombada + y_base_inf)/2), 
        va='center', 
        fontsize=8, 
        color="black"
    )
    ax.annotate(
        f"{(y_end - y_base_inf)/10:.1f} cm", 
        xy=(0, 0),
        xytext=(x1 + 8, (y_base_inf + y_end)/2),
        va='center', 
        fontsize=8, 
        color="black"
    )

    # 📏 Anotação de largura
    ax.annotate(
        f"{W/10:.1f} cm", 
        xy=(0, 0), 
        xytext=(x1/2, y_end),
        ha='center',
        fontsize=8, 
        color="black"
    )
