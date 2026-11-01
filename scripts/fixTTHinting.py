import os
from ttfautohint import ttfautohint
from ttfautohint.options import parse_args as ttfautohint_parse_args

ttfs_fonts_dir = "fonts/ttf"
roman_referenceFontPath = "fonts/ttf/SoftnessMono-Regular.ttf"
italic_referenceFontPath = "fonts/ttf/SoftnessMono-Italic.ttf"

for fontfile in os.listdir(ttfs_fonts_dir):
    if fontfile.split(".")[-1] == "ttf":
        inPath = outPath = os.path.join(ttfs_fonts_dir, fontfile)
        if inPath in [roman_referenceFontPath, italic_referenceFontPath]:
            continue

        args = []
        if "Italic" in fontfile:
            args.append("-R" + italic_referenceFontPath)
        else:
            args.append("-R" + roman_referenceFontPath)

        ttfautohint(**ttfautohint_parse_args([inPath, outPath, *args]))
        print(f"Fixed TT hints {fontfile}")