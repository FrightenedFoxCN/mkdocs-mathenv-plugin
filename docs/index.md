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
        tikzcd:
            ...
        ...
```

Currently only theorem and tikzcd are supported.

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

!!! warning
    In the rare case where you'd like to use "\\theorem" directly, use "\\\\theorem" instead, even in the code snipet. I know it's disturbing, but it requires some effort to fix it since parsing markdown is quite annoying.

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

We use embedded svg diagram on the html file. Generation of the diagram may take a while, since it requires multiple intermediate stage. After generated once, with `cachefile` option set to true, the cached svg file will be in `cache` directory and would not rebuild unless the file has changed. No auto-cleaning of the deprecated cache file is available currently, so you'll have to clean & rebuild periodically for disk space (although it's not so large admittedly). 

You can also use enable to control whether tikzcd is needed. True by default.

TikZcd can be embedded into other environments:

```
\\definition
    The automaton is reachable if and only if $r$ is surjective. The automaton is observable if and only if $o$ is injective. 

    \\tikzcd
        1 \arrow[rd]{}{i} \arrow[d]{}{\varepsilon}&      & 2\\
        \Sigma^\ast \arrow[r, dashed]{}{r} \arrow[d]{}{\alpha} & K \arrow[ru]{}{f} \arrow[r, dashed]{}{o} \arrow[d]{}{t} & 2^{\Sigma^\ast} \arrow[u]{}{\varepsilon?} \arrow[d]{}{\beta}\\
        (\Sigma^\ast)^\Sigma \arrow[r, dashed]{}{r^\Sigma} & K^\Sigma \arrow[r, dashed]{}{o^\Sigma} & (2^{\Sigma^\ast})^\Sigma
```

\definition
    The automaton is reachable if and only if $r$ is surjective. The automaton is observable if and only if $o$ is injective. 

    \tikzcd
        1 \arrow[rd]{}{i} \arrow[d]{}{\varepsilon}&      & 2\\
        \Sigma^\ast \arrow[r, dashed]{}{r} \arrow[d]{}{\alpha} & K \arrow[ru]{}{f} \arrow[r, dashed]{}{o} \arrow[d]{}{t} & 2^{\Sigma^\ast} \arrow[u]{}{\varepsilon?} \arrow[d]{}{\beta}\\
        (\Sigma^\ast)^\Sigma \arrow[r, dashed]{}{r^\Sigma} & K^\Sigma \arrow[r, dashed]{}{o^\Sigma} & (2^{\Sigma^\ast})^\Sigma

!!! warning
    An indented block after tikzcd environment is not supported currently!