from models import Box
from svg.enums import TopType
from svg.enums import CoverSide

from svg.paper.base import export as export_paper_base
from svg.paper.top_book import export as export_paper_top_book
from svg.paper.top_lose import export as export_paper_top_lose
from svg.paper.top_magnet import export as export_paper_top_magnet

from svg.cardboard.base import export as export_cardboard_base
from svg.cardboard.top_book import export as export_cardboard_top_book
from svg.cardboard.top_lose import export as export_cardboard_top_lose
from svg.cardboard.top_magnet import export as export_cardboard_top_magnet

width = 10
height = 10
depth = 10
thickness = 1.9

box = Box('MOURA_DUBEUX', width, height, depth, thickness)

# export_paper_base(box, CoverSide.EXTERNAL)
# export_paper_base(box, CoverSide.INTERNAL)

export_paper_top_book(box, CoverSide.EXTERNAL)
export_paper_top_book(box, CoverSide.INTERNAL)

# export_paper_top_lose(box, CoverSide.EXTERNAL)
# export_paper_top_lose(box, CoverSide.INTERNAL)

export_paper_top_magnet(box, CoverSide.EXTERNAL)
export_paper_top_magnet(box, CoverSide.INTERNAL)

# export_cardboard_base(box)
# export_cardboard_top_book(box)
# export_cardboard_top_lose(box)
# export_cardboard_top_magnet(box)