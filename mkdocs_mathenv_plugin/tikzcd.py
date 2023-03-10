from .tex import TeXWriter

from hashlib import sha256
import os

class TikZcdObject:
    """
    TikZcd object, to be generated to svg
    """
    def __init__(self, options: str, contents: str) -> None:
        self.options = options
        self.contents = contents

    def write_to_svg(self) -> str:
        filename = sha256(self.contents.encode()).hexdigest()

        writer = TeXWriter()
        writer.config.preamble = r'''
\documentclass[tikz]{standalone}
\usepackage{tikz}
\usetikzlibrary{cd}
        '''
        begin_command = r"\begin{tikzcd}[%s]" % self.options if self.options else r"\begin{tikzcd}"
        writer.create_tex_file("\n".join((
            begin_command,
            self.contents.strip(),
            r"\end{tikzcd}"
        )), filename)

        writer.create_svg_from_tex(filename)

        with open(f"{filename}.svg", "r", encoding="utf-8") as f:
            svg_str = f.read(None)

        # clean up
        try:
            os.remove(filename + ".svg")
        except FileNotFoundError:
            pass

        return svg_str

        