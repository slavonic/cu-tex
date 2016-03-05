# cu-num TeX package

Provide Church Slavonic Numbers

## Usage

```TeX
...
\usepackage{cu-num}

\begin{document}

\cunum{12345}

\end{document}
```

## Testing

To test, run `cu-num-test.tex`:
```bash
xelatex cu-num-test.tex
```
It should generate no errors and complete cleanly, generating 0 pages. Example log:
```
This is XeTeX, Version 3.14159265-2.6-0.99992 (TeX Live 2015) (preloaded format=xelatex)
 restricted \write18 enabled.
entering extended mode
(./cu-num-test.tex
LaTeX2e <2015/01/01>
Babel <3.9l> and hyphenation patterns for 29 languages loaded.
(/usr/local/texlive/2015basic/texmf-dist/tex/latex/base/article.cls
Document Class: article 2014/09/29 v1.4h Standard LaTeX document class
(/usr/local/texlive/2015basic/texmf-dist/tex/latex/base/size12.clo))
(./cu-num-test.sty (./cu-num.sty)) (./cu-num-test.aux) (./cu-num-test-data.tex)
 (./cu-num-test.aux) )
No pages of output.
Transcript written on cu-num-test.log.
```
