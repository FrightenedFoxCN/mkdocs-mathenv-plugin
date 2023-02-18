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
\theorem
    here is a theorem
```

Configurations:

- enable: boolean, whether the theorem environment is enabled
- definition/lemma/theorem/proof/proposition: the string to show on title of the box

### TikZcd environment

```
\tikzcd
    \mathsf{DA} \arrow[rr, bend left]{}{\bar 2} \arrow[dd]{}{U}& \perp & \mathsf{DA^{\mathrm{op}}} \arrow[ll, bend left]{}{\bar 2^{\mathrm{op}}}\arrow[dd]{}{U}\\
    & & \\
    \mathsf{Set} \arrow[rr, bend left]{}{2} & \perp & \mathsf{Set^{\mathrm{op}}} \arrow[ll, bend left]{}{2^{\mathrm{op}}}\\
```

Requires xelatex and dvisvgm to work properly.

We use embedded svg diagram on the html file. Generation of the diagram may take a while, since it requires multiple intermediate stage.

## TODO

Too much things to do yet!

- [ ] write specialized css for theorem environment
- [ ] add tikz support via local compilation
- [x] fix tikzcd picture problem
- [ ] add tikzcd configurations: especially night mode
- [ ] add svg support in css