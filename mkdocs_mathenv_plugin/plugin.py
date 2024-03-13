import os
import re

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files, File
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.config import base, config_options, Config
from mkdocs.utils import log, copy_file

from typing import Optional, Dict, Any

from .tikzcd import TikZcdObject
from .markdown_utils import replace_indented_block_start_with_options, get_indentation_level

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))

class _TheoremOptions(base.Config):
    enable = config_options.Type(bool, default=True)
    theorem = config_options.Type(str, default="定理")
    lemma = config_options.Type(str, default="引理")
    proposition = config_options.Type(str, default="命题")
    definition = config_options.Type(str, default="定义")
    proof = config_options.Type(str, default="证明")
    exercise = config_options.Type(str, default="习题")

class _TikZcdOptions(base.Config):
    enable = config_options.Type(bool, default=True)
    cachefile = config_options.Type(bool, default=True)

class _AliasOptions(base.Config):
    enable = config_options.Type(bool, default=True)
    alias_list = config_options.Type(Dict, default={})

class MathEnvConfig(base.Config):
    theorem = config_options.SubConfig(_TheoremOptions)
    tikzcd = config_options.SubConfig(_TikZcdOptions)
    alias = config_options.SubConfig(_AliasOptions)

class MathEnvPlugin(BasePlugin[MathEnvConfig]):

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        config["extra_css"] = ["css/svg.css"] + config["extra_css"]

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

        if self.config.tikzcd.enable:
            log.debug("[mathenv] tikzcd enabled!")
        if self.config.tikzcd.cachefile:
            log.debug("[mathenv] cache file enabled!")
            if not os.path.exists("cache"):
                os.mkdir("cache")
                log.debug("[mathenv] created path cache/")
        
        if self.config.alias.enable:
            log.debug("[mathenv] alias enabled!")
            log.debug(f"[mathenv] current alias list: {self.config.alias.alias_list}")
        
        return config

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        """
        On markdown, extend the theorem expression
        """
        def _replace_tikzcd(matched: re.Match[str]) -> str:
            """
            For each matched string, clean the first line label and transform it into html script 
            """
            options = matched.group("options")
            contents = matched.group("contents")
            first_line_indentation_level = get_indentation_level(matched.group("contents"))

            contents = [i for i in contents.splitlines()]

            contents_remain = []

            for idx, i in enumerate(contents):
                if get_indentation_level(i) < first_line_indentation_level:
                    contents_remain = contents[idx:]
                    contents = contents[:idx]
                    break

            contents = "\n".join(contents)
            tikzcd = TikZcdObject(options, contents)

            # The string should not be splitted into lines, since markdown parser won't recognize it
            svg_str = "".join(tikzcd.write_to_svg(self.config.tikzcd.cachefile).removeprefix("<?xml version='1.0' encoding='UTF-8'?>\n").splitlines())

            return matched.group("leading") + f"<center>{svg_str}</center>" + "\n" + "\n".join(contents_remain)

        if self.config.theorem.enable:
            markdown = re.sub(r"(?<!\\)\\theorem", "!!! success \"%s\"" % self.config.theorem.theorem, markdown)
            # fix possible use of "\theorem" when you don't need it
            markdown = re.sub(r"\\\\theorem", r"\\theorem", markdown)
            markdown = re.sub(r"(?<!\\)\\lemma", "!!! success \"%s\"" % self.config.theorem.lemma, markdown)
            markdown = re.sub(r"\\\\lemma", r"\\lemma", markdown)
            markdown = re.sub(r"(?<!\\)\\proposition", "!!! success \"%s\"" % self.config.theorem.proposition, markdown)
            markdown = re.sub(r"\\\\proposition", r"\\proposition", markdown)
            markdown = re.sub(r"(?<!\\)\\definition", "!!! info \"%s\"" % self.config.theorem.definition, markdown)
            markdown = re.sub(r"\\\\definition", r"\\definition", markdown)
            markdown = re.sub(r"(?<!\\)\\proof", "???+ info \"%s\"" % self.config.theorem.proof, markdown)
            markdown = re.sub(r"\\\\proof", r"\\proof", markdown)
            markdown = re.sub(r"(?<!\\)\\exercise", "!!! question \"%s\"" % self.config.theorem.exercise, markdown)
            markdown = re.sub(r"\\\\exercise", r"\\exercise", markdown)

        if self.config.tikzcd.enable:
            replaced_markdown = replace_indented_block_start_with_options(r"(?<!\\)\\tikzcd", _replace_tikzcd, markdown)

            # stupid way to fix the recursion problem
            while replaced_markdown != markdown:
                markdown = replaced_markdown
                replaced_markdown = replace_indented_block_start_with_options(r"(?<!\\)\\tikzcd", _replace_tikzcd, markdown)
            markdown = re.sub(r"\\\\tikzcd", r"\\tikzcd", markdown)

        log.debug(f"markdown file: \n{markdown}")

        return markdown

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        """
        On each page, find the environment to replace and generate something
        """

    def on_post_build(self, config: Dict[str, Any], **kwargs) -> None:
        """
        Add svg stylesheet support
        """ 
        files = ["css/svg.css"]
        for file in files:
            dest_file_path = os.path.join(config["site_dir"], file)
            src_file_path = os.path.join(PLUGIN_DIR, file)
            # print(src_file_path)
            assert os.path.exists(src_file_path)
            copy_file(src_file_path, dest_file_path)