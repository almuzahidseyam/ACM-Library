import os
import re

TEX_HEADER = r'''\documentclass[10pt,landscape,a4paper,twocolumn]{article}
\usepackage{fontspec}
\setmainfont{FreeSerif}
\setsansfont{FreeSans}
\setmonofont{FreeMono}

\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{multicol}
\usepackage{tocloft}
\usepackage{hyperref}

\geometry{left=1cm,right=1cm,top=1.5cm,bottom=1.5cm}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{ACM ICPC Reference Notebook}
\fancyhead[R]{\thepage}
\fancyfoot[C]{Al-Muzahid Seyam}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.97,0.97,0.97}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{blue},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
\lstset{style=mystyle}

\title{\vspace{-2cm}ACM ICPC C++ Reference Notebook}
\author{Al-Muzahid Seyam | BUET}
\date{\today}

\begin{document}
\maketitle
\begin{multicols}{2}
\tableofcontents
\end{multicols}
\pagebreak
'''

TEX_FOOTER = r'''\end{document}
'''

def get_sections(root_dir):
    sections = {}
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath or 'scripts' in dirpath or '.github' in dirpath:
            continue
        
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == '.':
            continue
            
        section_name = rel_path.replace('\\', '/').split('/')[0]
        if section_name not in sections:
            sections[section_name] = []
            
        for file in filenames:
            if file.endswith('.cpp'):
                full_path = os.path.join(dirpath, file)
                sections[section_name].append(full_path)
    
    return sections

def escape_latex(text):
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('_', '\\_')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    return text

def main():
    root = '.'
    sections = get_sections(root)
    
    with open('notebook.tex', 'w', encoding='utf-8') as tex:
        tex.write(TEX_HEADER)
        
        for section in sorted(sections.keys()):
            tex.write(r'\section{' + escape_latex(section) + '}\n')
            
            for file_path in sorted(sections[section]):
                file_name = os.path.basename(file_path)
                display_name = file_name.replace('.cpp', '')
                
                tex.write(r'\subsection{' + escape_latex(display_name) + '}\n')
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        code = f.read()
                        
                tex.write(r'\begin{lstlisting}[language=C++]' + '\n')
                tex.write(code + '\n')
                tex.write(r'\end{lstlisting}' + '\n\n')
                
        tex.write(TEX_FOOTER)
    
    print("notebook.tex generated successfully for xelatex!")

if __name__ == '__main__':
    main()
