import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter.filedialog import asksaveasfilename

from math_touche import export_to_svg, draw_preview_base, draw_preview_top

VERSAO_ATUAL = "v0.1.0"

root = tk.Tk()
root.title(f"Touché | Caixa de tampa com imã - {VERSAO_ATUAL}")
root.geometry("1200x800")

# Parâmetros
params_tampa = {
    'Altura da língua (cm)': tk.DoubleVar(value=5),
}

usar_altura_lingua_personalizada = tk.BooleanVar(value=False)

params_caixa = {
    'Largura (cm)': tk.DoubleVar(value=20),
    'Comprimento (cm)': tk.DoubleVar(value=15),
    'Profundidade (cm)': tk.DoubleVar(value=8),
}

params_geral = {
    'Espessura (mm)': tk.DoubleVar(value=1.9),
}

espessuras_disponiveis = [
    1.50, 
    1.90, 
    2.00, 
    2.55
]

# Atualiza preview
def update_preview(event=None):
    if usar_altura_lingua_personalizada.get():
        altura_lingua_valor = params_tampa['Altura da língua (cm)'].get()
    else:
        altura_lingua_valor = None

    draw_preview_top(
        ax_top,
        params_caixa['Largura (cm)'].get(),
        params_caixa['Comprimento (cm)'].get(),
        params_caixa['Profundidade (cm)'].get(),
        altura_lingua_valor,
        params_tampa['Altura da língua (cm)'] if not usar_altura_lingua_personalizada.get() else None,
    )
    draw_preview_base(
        ax_base,
        params_caixa['Largura (cm)'].get(),
        params_caixa['Comprimento (cm)'].get(),
        params_caixa['Profundidade (cm)'].get(),
        params_geral['Espessura (mm)'].get(),
        altura_lingua_valor,
        params_tampa['Altura da língua (cm)'] if not usar_altura_lingua_personalizada.get() else None,
    )
    canvas.draw()

def gerar_svg():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"tampa-solta_{timestamp}.svg"
    caminho = asksaveasfilename(
        defaultextension=".svg",
        filetypes=[("Arquivo SVG", "*.svg")],
        initialfile=file_name,
        title="Salvar arquivo SVG"
    )

    if usar_altura_lingua_personalizada.get():
        altura_lingua_valor = params_tampa['Altura da língua (cm)'].get()
    else:
        altura_lingua_valor = None

    if caminho:
        export_to_svg(
            caminho,
            params_caixa['Largura (cm)'].get(),
            params_caixa['Comprimento (cm)'].get(),
            params_caixa['Profundidade (cm)'].get(),
            params_geral['Espessura (mm)'].get(),
            altura_lingua_valor
        )
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

# Alerta temporário
def mostrar_alerta_temporario(msg, tempo=3000):
    alerta = tk.Label(root, text=msg, bg='green', fg='white', font=('Arial', 10, 'bold'))
    alerta.place(relx=0.5, rely=0.97, anchor='center')
    root.after(tempo, alerta.destroy)

# Frame principal
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Frame esquerdo (preview)
preview_frame = ttk.Frame(main_frame)
preview_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

fig = plt.Figure(figsize=(2, 8), dpi=120)
ax_top = fig.add_subplot(122)
ax_base = fig.add_subplot(121)


canvas = FigureCanvasTkAgg(fig, master=preview_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)
canvas.get_tk_widget().configure(width=400, height=1000)

# Frame direito (controles)
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side='left', fill='y')

# Parâmetros da tampa
inputs_tampa = ttk.LabelFrame(controls_frame, text="Parâmetros da tampa", padding=15)
inputs_tampa.pack(fill="x")

for nome, var in params_tampa.items():
    frame = ttk.Frame(inputs_tampa)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=15).pack(side='left')

    if nome == 'Altura da língua (cm)':
        altura_lingua_frame = ttk.Frame(frame)
        altura_lingua_frame.pack(side='right')

        chk = ttk.Checkbutton(altura_lingua_frame, variable=usar_altura_lingua_personalizada, text="🔓", command=update_preview)
        chk.pack(side='left')

        entry = ttk.Entry(altura_lingua_frame, textvariable=var, width=5)
        entry.pack(side='right', padx=(0, 0))
        entry.bind("<KeyRelease>", update_preview)
    else:
        entry = ttk.Entry(frame, textvariable=var, width=5)
        entry.pack(side='right')
        entry.bind("<KeyRelease>", update_preview)

        scale_range = (0, 10)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)


# Parâmetros da caixa
inputs_caixa = ttk.LabelFrame(controls_frame, text="Parâmetros da caixa", padding=15)
inputs_caixa.pack(fill="x", pady=10)

for nome, var in params_caixa.items():
    frame = ttk.Frame(inputs_caixa)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=15).pack(side='left')

    entry = ttk.Entry(frame, textvariable=var, width=5)
    entry.pack(side='right')
    entry.bind("<KeyRelease>", update_preview)

    scale_range = (0, 30)
    scale = ttk.Scale(
        frame, from_=scale_range[0], to=scale_range[1],
        orient='horizontal', variable=var,
        command=lambda val: update_preview()
    )
    scale.pack(side='left', fill='x', expand=True, padx=5)

# Parâmetros da gerais
inputs_geral = ttk.LabelFrame(controls_frame, text="Parâmetros gerais", padding=15)
inputs_geral.pack(fill="x")

for nome, var in params_geral.items():
    frame = ttk.Frame(inputs_geral)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=12).pack(side='left')

    if nome == 'Espessura (mm)':
        radiobutton_frame = ttk.Frame(frame)
        radiobutton_frame.pack(side='right', fill='x', expand=True)

        for valor in espessuras_disponiveis:
            ttk.Radiobutton(
                radiobutton_frame,
                text=f"{valor}",
                value=valor,
                variable=var,
                command=update_preview
            ).pack(side='left', padx=10)
    else:
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side='right')
        entry.bind("<KeyRelease>", update_preview)

        scale_range = (0, 5)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)

# Botões
botoes = ttk.Frame(controls_frame)
botoes.pack(pady=5, anchor='center')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(side='left', padx=5)

# Inicia preview
update_preview()
root.mainloop()

# (Papelão) Tampa ima:
# 2. Os imas da caixa ficam centralizados na metade da língua se a língua tiver ate 7cm de altura, depois disso o ima vai estar 3 cm da parte de cima (consequentemente o que fica na caixa desce)
# 4. Até 10cm de largura da caixa, se usa 1 ima. 15cm é 2 imas (1/4 - 2/4 - 1/4)
# 
# O circulo do ima na tampa é corte, na caixa é vinco.
# A altura da lombada é igual a profundidade da caixa
# A altura do tampo é igual a altura da base
# A língua tem 0.5cm a menos que a lombada (ou seja, a profundidade da caixa)
# 
