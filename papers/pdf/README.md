# Compiled SSV Papers (PDFs)

This folder collects the compiled PDF of every paper in the SSV series,
named for easy browsing (`SSV I.pdf`, `SSV II.pdf`, ...).  Each is
produced from `papers/SSV-<X>/main.tex` by running `pdflatex` (twice for
cross-references); the source files remain the canonical version.

## Current contents

| File | Source | Notes |
|---|---|---|
| `SSV I.pdf` | `papers/SSV-I/main.tex` | Foundations: LogSE, electron, ladder, proton (1.2% match) |
| `SSV II.pdf` | `papers/SSV-II/main.tex` | Muon ring-breathing mode derivation |
| `SSV III.pdf` | `papers/SSV-III/main.tex` | |
| `SSV IV.pdf` | `papers/SSV-IV/main.tex` | |
| `SSV V.pdf` | `papers/SSV-V/main.tex` | |
| `SSV VI-a.pdf` | `papers/SSV-VI-a/main.tex` | |
| `SSV VI-b.pdf` | `papers/SSV-VI-b/main.tex` | |
| `SSV VII-a.pdf` | `papers/SSV-VII-a/main.tex` | |
| `SSV VII-b.pdf` | `papers/SSV-VII-b/main.tex` | |
| `SSV VIII.pdf` | `papers/SSV-VIII/main.tex` | |
| `SSV Alpha.pdf` | `papers/SSV-Alpha/main.tex` | Fine-structure constant |
| `SSV Goldstone.pdf` | `papers/SSV-Goldstone/main.tex` | EM propagation as transverse Goldstone |

`SSV-IX/` contains only a `README.md` (CMB paper outline, no `main.tex` yet)
so no PDF is generated.

## Rebuilding

To refresh all PDFs after editing source files:

```bash
for dir in SSV-I SSV-II SSV-III SSV-IV SSV-V SSV-VI-a SSV-VI-b \
           SSV-VII-a SSV-VII-b SSV-VIII SSV-Alpha SSV-Goldstone; do
  (cd papers/$dir && pdflatex -interaction=nonstopmode main.tex && \
                     pdflatex -interaction=nonstopmode main.tex) > /dev/null
  out_name=$(echo "$dir" | sed 's/SSV-/SSV /')
  cp papers/$dir/main.pdf "papers/pdf/${out_name}.pdf"
done
```

Or compile a single paper:

```bash
(cd papers/SSV-I && pdflatex main.tex && pdflatex main.tex)
cp papers/SSV-I/main.pdf "papers/pdf/SSV I.pdf"
```
