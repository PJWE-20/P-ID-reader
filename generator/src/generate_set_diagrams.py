"""
Generates a set of diagrams
"""
import argparse
import random
from random import randint, shuffle
from typing import List

from PIL import Image
from config import SYMBOL_DEBUG
from metadata import (
    SymbolStorage,
    BlockedSymbolsStorage,
    DiagramSymbolsStorage,
    DiagramStorage,
)
from symbol import GenericSymbol, SymbolGenerator, SymbolConfiguration, SymbolPositioner


def generate_diagram(
    symbol_storage: SymbolStorage,
    dss: DiagramSymbolsStorage,
    diagram_matters: List[str],
):
    number_of_symbols = randint(100, 200)
    possible_orientation = [90]
    DIAGRAM_SIZE = (5000, 3500)
    image_diagram = Image.new("LA", DIAGRAM_SIZE, 255)
    symbols = []

    for matter in diagram_matters:
        symbols.extend(symbol_storage.get_symbols_by_matter(matter))

    blocked_symbol_st = BlockedSymbolsStorage()
    symbols = blocked_symbol_st.filter_out_blocked_symbols(
        symbols, blocked_symbol_st.blocked_symbols
    )

    shuffle(symbols)
    diagram_symbols = []
    ctbm = SymbolConfiguration()
    symbol_generator = SymbolGenerator(ctbm=ctbm)
    positions = SymbolPositioner.get_symbol_position(number_of_symbols, DIAGRAM_SIZE)

    for i in range(number_of_symbols):
        symbol = symbols[i % len(symbols)]
        coords = positions[i]
        orientation = possible_orientation[0] if i % 4 == 0 else 0
        symbol_generic = GenericSymbol(
            symbol.name, coords[0], coords[1], orientation=orientation
        )
        symbol_generator.inject_symbol(symbol_generic, image_diagram)
        if SYMBOL_DEBUG:
            symbol_generator.draw_boxes(symbol_generic, image_diagram)
        diagram_symbols.append(symbol_generic)

    diagram_storage = DiagramStorage()
    diagram_storage.store_image(dss, image_diagram, diagram_symbols)
    return diagram_symbols


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a set of diagrams and the input for the NNet"
    )
    parser.add_argument(
        "--number_diagrams",
        type=int,
        nargs=1,
        help="Number of diagrams to produce",
        default=[1],
    )
    parser.add_argument(
        "--diagram_matter",
        type=str,
        nargs="*",
        help="""Matters of the diagram, at least two: 'P-Process', 'L-Piping', 'H-HVAC', 'T-telecom', 'N-Structural',
       'R-Mechanical', 'E-Electro', 'J-Instrument', 'S-Safety'""",
        default=None,
    )
    symbol_storage = SymbolStorage()
    dss = DiagramSymbolsStorage()
    args = parser.parse_args()
    number_diagrams = int(args.number_diagrams[0])
    for i in range(number_diagrams):
        if args.diagram_matter:
            if type(args.diagram_matter) == list:
                diagram_matters = args.diagram_matter
            else:
                diagram_matters = [args.diagram_matter]
        else:
            matters = symbol_storage.get_matters()
            random.choices(matters, k=2)

    generate_diagram(symbol_storage, dss, diagram_matters)
