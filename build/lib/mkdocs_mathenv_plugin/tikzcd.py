from .tex import TeXWriter

from hashlib import sha256
from mkdocs.utils import log
import os

class TikZcdObject:
    """
    TikZcd object, to be generated to svg
    """
    def __init__(self, options: str, contents: str) -> None:
        self.options = options
        self.contents = contents

    def write_to_svg(self, cachefile: bool) -> str:
        filename = sha256(self.contents.encode()).hexdigest()

        if cachefile == True:
            try:
                os.chdir("cache")
            except OSError:
                log.error("[mathenv] cache directory not found!")

        if cachefile == True and os.path.exists(f"{filename}.svg"):
            log.info("[mathenv] load from existed file...")
            with open(f"{filename}.svg", "r", encoding="utf-8") as f:
                svg_str = f.read(None)
            os.chdir("..")
            return svg_str

        writer = TeXWriter()
        writer.config.preamble = r'''
\documentclass{standalone}
\usepackage{tikz}
\usepackage{amssymb}
\usetikzlibrary{cd}
\usetikzlibrary{decorations.markings}
\tikzset{double line with arrow/.style args={#1,#2}{decorate,decoration={markings,%
mark=at position 0 with {\coordinate (ta-base-1) at (0,1pt);
\coordinate (ta-base-2) at (0,-1pt);},
mark=at position 1 with {\draw[#1] (ta-base-1) -- (0,1pt);
\draw[#2] (ta-base-2) -- (0,-1pt);
}}}}
        '''
        begin_command = r"\[ \begin{tikzcd}[%s]" % self.options if self.options else r"\[ \begin{tikzcd}"
        writer.create_tex_file("\n".join((
            begin_command,
            self.contents.strip(),
            r'''\end{tikzcd} 
'''
        )), filename)

        writer.create_svg_from_tex(filename)

        with open(f"{filename}.svg", "r", encoding="utf-8") as f:
            svg_str = f.read(None)

        # clean up
        if cachefile == False :
            try:
                os.remove(filename + ".svg")
            except FileNotFoundError:
                pass

        os.chdir("..")

        return svg_str

        