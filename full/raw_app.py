import os
from datetime import datetime

from models import Box
from enums import CoverSide

from svg.paper.base import export as paper_base
from svg.paper.top_book import export as paper_top_book
from svg.paper.top_lose import export as paper_top_lose
from svg.paper.top_magnet import export as paper_top_magnet

from svg.cardboard.base import export as cardboard_base
from svg.cardboard.top_book import export as cardboard_top_book
from svg.cardboard.top_lose import export as cardboard_top_lose
from svg.cardboard.top_magnet import export as cardboard_top_magnet

def ask(texto, tipo=str):
	while True:
		try:
			return tipo(input(f"{texto}: ").strip())
		except ValueError:
			print("Entrada inválida. Tente novamente.")

def main():
	print("=== Gerador de linhas de corte ===")
	client_name = ask("Nome do projeto?")
	width = ask("Largura da caixa? (em cm)", float)
	height = ask("Comprimento da caixa? (em cm)", float)
	depth = ask("Profundidade da caixa? (em cm)", float)
	thickness = ask("Espessura do papelão? (em mm)", float)

	box = Box(client_name, width, height, depth, thickness)

	desktop = os.path.join(os.path.expanduser("~"), "Desktop")
	folder_name = client_name.strip().replace(" ", "_")
	folder = os.path.join(desktop, folder_name)
	os.makedirs(folder, exist_ok=True)

	cardboard_base(box)
	cardboard_top_book(box)
	cardboard_top_lose(box)
	cardboard_top_magnet(box)

	paper_top_book(box, CoverSide.EXTERNAL)
	paper_top_book(box, CoverSide.INTERNAL)

	paper_top_magnet(box, CoverSide.EXTERNAL)
	paper_top_magnet(box, CoverSide.INTERNAL)

	# paper_base(box, CoverSide.EXTERNAL)
	# paper_base(box, CoverSide.INTERNAL)

	# paper_top_lose(box, CoverSide.EXTERNAL)
	# paper_top_lose(box, CoverSide.INTERNAL)

if __name__ == "__main__":
	main()