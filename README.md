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

## TODO

Too much things to do yet!

- [ ] write specialized css for theorem environment
- [ ] add tikz & tikzcd support via local compilation