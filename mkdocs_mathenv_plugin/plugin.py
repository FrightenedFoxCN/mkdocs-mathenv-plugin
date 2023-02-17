import os
import re

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files, File
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.config import base, config_options
from mkdocs.utils import log

from typing import Optional

from .tikzcd import TikZcdObject

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(PLUGIN_DIR, 'templates')

class _TheoremOptions(base.Config):
    enable = config_options.Type(bool, default=True)
    theorem = config_options.Type(str, default="定理")
    lemma = config_options.Type(str, default="引理")
    proposition = config_options.Type(str, default="命题")
    definition = config_options.Type(str, default="定义")
    proof = config_options.Type(str, default="证明")

class MathEnvConfig(base.Config):
    theorem = config_options.SubConfig(_TheoremOptions)

class MathEnvPlugin(BasePlugin[MathEnvConfig]):

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        """
        Just for debugging
        """
        if self.config.theorem.enable:
            log.debug("[mathenv] theorem environment enabled!")
            log.debug("[mathenv] theorem titled with %s" % self.config.theorem.theorem)
            log.debug("[mathenv] lemma titled with %s" % self.config.theorem.lemma)
            log.debug("[mathenv] proposition titled with %s" % self.config.theorem.proposition)
            log.debug("[mathenv] definition titled with %s" % self.config.theorem.definition)
            log.debug("[mathenv] proof replaced with %s" % self.config.theorem.proof)
        return config



    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        """
        On markdown, extend the theorem expression
        """
        log.info(f"the file uris are {files.src_uris}")
        log.info(f"current page is {page.file.src_uri}")

        def _replace_tikzcd(matched: re.Match[str]) -> str:
            """
            For each matched string, clean the first line label and transform it into html script 
            """
            options = matched.group("options")
            contents = matched.group("contents")
            log.debug(f"matched option: {options}")
            log.debug(f"matched option: {contents}")
            tikzcd = TikZcdObject(options, contents)
            svg_name = tikzcd.write_to_svg()
            log.debug(f"write to svg {svg_name}")
            os.system
            svg_file = File(
                f"{svg_name}",
                "",
                f"docs/images",
                False
            )
            files.append(svg_file)
            return f"<center><img src=\"/images/{svg_name}\"/></center>"

        markdown = re.sub(r"\\theorem", "!!! success \"%s\"" % self.config.theorem.theorem, markdown)
        markdown = re.sub(r"\\lemma", "!!! success \"%s\"" % self.config.theorem.lemma, markdown)
        markdown = re.sub(r"\\proposition", "!!! success \"%s\"" % self.config.theorem.proposition, markdown)
        markdown = re.sub(r"\\definition", "!!! info \"%s\"" % self.config.theorem.definition, markdown)
        markdown = re.sub(r"\\proof", "???+ info \"%s\"" % self.config.theorem.proof, markdown)

        markdown = re.sub(r"(?P<overall>\\tikzcd(\[(?P<options>.*)\])?.*\n(?P<contents>([\t(    )]*.*\n)*))", _replace_tikzcd, markdown)

        return markdown

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        """
        On each page, find the environment to replace and generate something
        """