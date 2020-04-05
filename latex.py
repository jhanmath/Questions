# -*- coding: utf-8 -*-

docclass=r'''% !TeX program = xelatex
\documentclass{ctexart}
'''
preamble=r'''\usepackage[margin=1in]{geometry}
\usepackage{tasks}
\usepackage{enumerate}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{physics}
\usepackage{tagging}
\usepackage{tikz,pgfplots} %绘图
\usetikzlibrary{arrows,intersections}
\usepgfplotslibrary{fillbetween}
\usetikzlibrary{patterns}

\pagestyle{plain}
\ctexset{
	section = {
		name = {,、},
		number = \chinese{section},
	}
}

\NewTasksEnvironment[
label = ({\Alph*}) ,
label-width = 14pt
]{choice}[\choice]

\newcommand{\emptychoice}{（\makebox[1cm]{}）}
\newcommand{\blank}[1][3em]{\underline{\makebox[#1]{}}}
\newcommand{\ds}{\displaystyle}
\newcommand{\Prj}{\text{Prj}}
\usetag{sol} % 不显示解答为nosol，显示解答为sol

\title{'''

title = '多元函数微分法作业2'

begindocument = r'''}
\date{}

\begin{document}

\maketitle

'''

contents = ''

enddocument = r'''

\end{document}'''