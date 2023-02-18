# mkdocs-mathenv-plugin

A simple environment support on mkdocs-material for maths writing.

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

Currently only theorem is supported.

### Theorem environment

Set the paragraph as definition/lemma/theorem/proof/proposition by something like:

```
\\theorem
    here is a theorem
```

\theorem
    here is a theorem

```
\\definition
    here is a definition
```

\definition
    here is a definition

```
\\proof
    here is a proof
```

\proof
    here is a proof (can be collapsed)

Configurations:

- enable: boolean, whether the theorem environment is enabled
- definition/lemma/theorem/proof/proposition: the string to show on title of the box

Requires following markdown extensions:

```
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
```

### TikZcd environment

```
\\tikzcd
    \mathsf{DA} \arrow[rr, bend left]{}{\bar 2} \arrow[dd]{}{U}& \perp & \mathsf{DA^{\mathrm{op}}} \arrow[ll, bend left]{}{\bar 2^{\mathrm{op}}}\arrow[dd]{}{U}\\
    & & \\
    \mathsf{Set} \arrow[rr, bend left]{}{2} & \perp & \mathsf{Set^{\mathrm{op}}} \arrow[ll, bend left]{}{2^{\mathrm{op}}}
```

\tikzcd
    \mathsf{DA} \arrow[rr, bend left]{}{\bar 2} \arrow[dd]{}{U}& \perp & \mathsf{DA^{\mathrm{op}}} \arrow[ll, bend left]{}{\bar 2^{\mathrm{op}}}\arrow[dd]{}{U}\\
    & & \\
    \mathsf{Set} \arrow[rr, bend left]{}{2} & \perp & \mathsf{Set^{\mathrm{op}}} \arrow[ll, bend left]{}{2^{\mathrm{op}}}

Requires xelatex and dvisvgm to work properly.

We use embedded svg diagram on the html file. Generation of the diagram may take a while, since it requires multiple intermediate stage.