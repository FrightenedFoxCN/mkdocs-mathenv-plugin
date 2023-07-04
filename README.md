# mkdocs-mathenv-plugin

A simple environment support on mkdocs-material for maths writing.

Example & Usage: https://frightenedfoxcn.github.io/mkdocs-mathenv-plugin/

## Installation

Install from source:

```
pip install -e .
```

## Usage

Enable on mkdocs.yml:

```
plugins:
    - mathenv
        theorem:
            ...
        ...
```

Currently only theorem & tikzcd is supported.

### Theorem environment

Set the paragraph as definition/lemma/theorem/proof/proposition.

### TikZcd environment

Embedding commutative diagram into html.

Requires xelatex and dvisvgm to work properly.

Generation of the diagram may take a while, since it requires multiple intermediate stage.

## TODO

Too much things to do yet!

- [ ] write specialized css for theorem environment
- [ ] add tikz support via local compilation
- [x] fix tikzcd picture problem
- [x] add tikzcd configurations: especially night mode
- [x] add svg support in css
- [ ] fix theorem environment: \theorem in codeblock, etc.
- [ ] fix the indented block after tikzcd
- [x] add caching to tikzcd environment to accelerate generation.
- [ ] more tikzcd configurations
- [ ] add alias system to replace the `\newcommand` like items in LaTeX