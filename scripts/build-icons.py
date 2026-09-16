#!/usr/bin/env python3
"""Build the original Darcula symbol glyphs and their VS Code mappings.

Build-only requirement: FontTools 4.65.0 (python3 -m pip install fonttools==4.65.0).
Run from any directory with python3 scripts/build-icons.py. The extension loads
only the generated JSON and WOFF; Python and FontTools are not runtime requirements.
COLR/CPAL layers keep each symbol color unchanged when VS Code selects its row.
The outlines below are original, single-color, 16px designs under this project's
MIT license, inspired by letter badges used in JetBrains IDEs.
"""
import json
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path

ROOT = Path(__file__).resolve().parents[1]
FONT_ID = "darcula-symbols"
# Opposite winding leaves a transparent center, preserving contrast on selection.
CIRCLE = (
    "M15 8 A7 7 0 1 1 1 8 A7 7 0 1 1 15 8 Z "
    "M14 8 A6 6 0 1 0 2 8 A6 6 0 1 0 14 8 Z"
)
DIAMOND = "M8 .5 L15.5 8 L8 15.5 L.5 8 Z M8 1.9 L1.9 8 L8 14.1 L14.1 8 Z"
LETTERS = {
    "C": "M11 5.3 L10.2 6 C8.2 3.8 5.7 5.2 5.7 8 C5.7 10.8 8.2 12.2 10.2 10 L11 10.7 C8.4 13.6 4.6 11.6 4.6 8 C4.6 4.4 8.4 2.4 11 5.3 Z",
    "S": "M10.9 5.1 L10.2 5.9 C8.8 4.4 6.1 4.8 6.1 6.2 C6.1 7.2 7.3 7.4 8.6 7.8 C10 8.2 11 8.7 11 10.1 C11 12.7 6.7 13 4.8 10.9 L5.6 10.1 C7.1 11.8 9.9 11.5 9.9 10.1 C9.9 9.1 8.6 8.9 7.3 8.5 C5.9 8.1 5 7.5 5 6.2 C5 3.8 8.8 3.3 10.9 5.1 Z",
    "I": "M6 4.5 H10 V5.5 H8.5 V10.5 H10 V11.5 H6 V10.5 H7.5 V5.5 H6 Z",
    "T": "M4.8 4.5 H11.2 V5.5 H8.55 V11.5 H7.45 V5.5 H4.8 Z",
    "E": "M5.5 4.5 H10.5 V5.5 H6.6 V7.5 H10 V8.5 H6.6 V10.5 H10.5 V11.5 H5.5 Z",
    "K": "M5.4 4.5 H6.5 V7.7 L9.7 4.5 H11 L7.8 7.8 L11.2 11.5 H9.8 L6.5 8 V11.5 H5.4 Z",
    "f": "M7 12 V7.3 H5.7 V6.3 H7 V5.5 C7 4.2 7.8 3.7 9 3.7 H10 V4.7 H9 C8.4 4.7 8.1 4.9 8.1 5.5 V6.3 H10 V7.3 H8.1 V12 Z",
    "m": "M3.8 10.8 V5.8 H4.8 V6.5 C5.6 5.4 7.3 5.3 8 6.6 C9 5.1 12.2 5.2 12.2 7.7 V10.8 H11.2 V7.7 C11.2 6.2 8.6 6.2 8.6 8 V10.8 H7.6 V7.7 C7.6 6.2 4.8 6.2 4.8 8 V10.8 Z",
    "v": "M4.8 5.5 H6 L8 10.5 L10 5.5 H11.2 L8.6 11.5 H7.4 Z",
    "p": "M5.5 12.5 V5.5 H6.5 V6.2 C8.4 4.3 11 5.7 11 8 C11 10.4 8.4 11.6 6.5 10 V12.5 Z M6.5 8 C6.5 10.5 9.9 10.5 9.9 8 C9.9 5.5 6.5 5.5 6.5 8 Z",
}
FOLDER = "M1 3 H6 L8 5 H15 V13 H1 Z M2 4 V12 H14 V6 H7.6 L5.6 4 Z"
PACKAGE = FOLDER + " M6 8 H10 V11 H6 Z M7 9 V10 H9 V9 Z"
SNIPPET = (
    "M1 2 H15 V14 H1 Z M2 3 V13 H14 V3 Z "
    "M6.5 5 L3.5 8 L6.5 11 L7.2 10.3 L4.9 8 L7.2 5.7 Z "
    "M9.5 5 L8.8 5.7 L11.1 8 L8.8 10.3 L9.5 11 L12.5 8 Z"
)
TEXT = "M2 4 H14 V5 H2 Z M2 7.5 H11 V8.5 H2 Z M2 11 H8 V12 H2 Z"
# Keep codepoints stable. Multiple VS Code IDs can share a semantic glyph.
GLYPHS = [
    ("struct", CIRCLE + LETTERS["S"], ["symbol-struct"]),
    ("class", CIRCLE + LETTERS["C"], ["symbol-class"]),
    ("interface", CIRCLE + LETTERS["I"], ["symbol-interface"]),
    ("type", CIRCLE + LETTERS["T"], ["symbol-type-parameter"]),
    ("function", CIRCLE + LETTERS["f"], ["symbol-function"]),
    ("method", CIRCLE + LETTERS["m"], ["symbol-method", "symbol-constructor"]),
    ("field", CIRCLE + LETTERS["f"], ["symbol-field"]),
    ("variable", CIRCLE + LETTERS["v"], ["symbol-variable", "symbol-parameter"]),
    ("property", CIRCLE + LETTERS["p"], ["symbol-property"]),
    ("constant", DIAMOND + LETTERS["C"], ["symbol-constant"]),
    ("enum", CIRCLE + LETTERS["E"], ["symbol-enum"]),
    ("enumMember", DIAMOND + LETTERS["E"], ["symbol-enum-member"]),
    ("package", PACKAGE, ["symbol-module", "symbol-namespace", "symbol-package"]),
    ("keyword", CIRCLE + LETTERS["K"], ["symbol-keyword"]),
    ("snippet", SNIPPET, ["symbol-snippet"]),
    ("text", TEXT, ["symbol-text"]),
]


def main():
    order = [".notdef"] + [name for name, _, _ in GLYPHS]
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    mappings = {}
    for index, (name, path, ids) in enumerate(GLYPHS):
        pen = TTGlyphPen(None)
        # SVG's downward Y axis becomes a 1024-unit font with a 128-unit descent.
        parse_path(path, TransformPen(Cu2QuPen(pen, 0.5), (64, 0, 0, -64, 0, 896)))
        glyphs[name] = pen.glyph()
        for icon_id in ids:
            mappings[icon_id] = {"fontCharacter": f"\\{0xE000 + index:x}", "fontId": FONT_ID}
    # Fixed palette entries prevent the suggest widget's selected foreground
    # from repainting icons. The original outlines remain as a fallback.
    colors = json.loads((ROOT / "themes/darcula.json").read_text())["colors"]
    color_keys = {"type": "typeParameter", "enum": "enumerator",
                  "enumMember": "enumeratorMember", "package": "module"}
    palette = []
    layers = {}
    for index, (name, _, _) in enumerate(GLYPHS):
        layer = name + ".color"
        order.append(layer)
        glyphs[layer] = glyphs[name]
        layers[name] = [(layer, index)]
        rgb = colors[f"symbolIcon.{color_keys.get(name, name)}Foreground"].lstrip("#")
        palette.append(tuple(int(rgb[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,))
    font = FontBuilder(1024, isTTF=True)
    font.setupGlyphOrder(order)
    font.setupCharacterMap({0xE000 + i: name for i, (name, _, _) in enumerate(GLYPHS)})
    font.setupGlyf(glyphs)
    font.setupHorizontalMetrics({name: (1024, getattr(glyphs[name], "xMin", 0)) for name in order})
    font.setupHorizontalHeader(ascent=896, descent=-128)
    font.setupNameTable({
        "familyName": "Darcula Symbols", "styleName": "Regular",
        "uniqueFontIdentifier": "DarculaSymbols-1.0", "fullName": "Darcula Symbols",
        "psName": "DarculaSymbols", "version": "Version 1.0",
        "copyright": "Original glyphs, MIT license; see the extension LICENSE.",
    })
    font.setupOS2(sTypoAscender=896, sTypoDescender=-128, usWinAscent=896, usWinDescent=128)
    font.setupPost()
    font.setupCOLR(layers, version=0)
    font.setupCPAL([palette])
    # Fixed timestamp makes repeated builds byte-for-byte identical.
    font.font["head"].created = font.font["head"].modified = 3800000000
    font.font.recalcTimestamp = False
    font.font.flavor = "woff"
    font.save(ROOT / "themes/darcula-symbols.woff")
    theme = {
        "fonts": [{"id": FONT_ID, "src": [{"path": "./darcula-symbols.woff", "format": "woff"}],
                   "weight": "normal", "style": "normal"}],
        "iconDefinitions": mappings,
    }
    (ROOT / "themes/darcula-product-icon-theme.json").write_text(json.dumps(theme, indent=2) + "\n")
    print(f"Built {len(GLYPHS)} glyphs covering {len(mappings)} symbol IDs.")


if __name__ == "__main__":
    main()
