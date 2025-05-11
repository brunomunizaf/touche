import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter.filedialog import asksaveasfilename

from math_touche import export_to_svg, draw_preview_base, draw_preview_top

VERSAO_ATUAL = "v0.1.0"

root = tk.Tk()
root.title(f"Touché | Caixa de tampa livro - {VERSAO_ATUAL}")
root.geometry("1200x800")

# Parâmetros
params = {
    'Largura (cm)': tk.DoubleVar(value=20),
    'Comprimento (cm)': tk.DoubleVar(value=15),
    'Profundidade (cm)': tk.DoubleVar(value=8),
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
    draw_preview_top(
        ax_top,
        params['Largura (cm)'].get(),
        params['Comprimento (cm)'].get(),
        params['Profundidade (cm)'].get()
    )
    draw_preview_base(
        ax_base,
        params['Largura (cm)'].get(),
        params['Comprimento (cm)'].get(),
        params['Profundidade (cm)'].get(),
        params['Espessura (mm)'].get()
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

    if caminho:
        export_to_svg(
            caminho,
            params['Largura (cm)'].get(),
            params['Comprimento (cm)'].get(),
            params['Profundidade (cm)'].get(),
            params['Espessura (mm)'].get()
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

# Parâmetros da caixa
inputs_caixa = ttk.LabelFrame(controls_frame, text="Parâmetros", padding=15)
inputs_caixa.pack(fill="x", pady=10)

for nome, var in params.items():
    frame = ttk.Frame(inputs_caixa)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=15).pack(side='left')

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

# Botões
botoes = ttk.Frame(controls_frame)
botoes.pack(pady=5, anchor='center')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(side='left', padx=5)

# Inicia preview
update_preview()
root.mainloop()
