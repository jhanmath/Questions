### 数学题库

本软件是为管理数学题目而设计，目的是解决数学题目录入困难和自由组织导出题目等问题，避免每学期都要花大量时间出练习题给学生。

共设置六类题目类型：单选题，多选题，判断题，填空题，计算题，证明题。每道题目可添加题干、解答、所属章节（以同济七版高等数学为参考）、难度和题目来源。在添加过程中支持预览，预览以 MathJax 渲染公式，支持大部分 $latex$ 语法。

导出的题目实际上是$latex$源码，编译 template.tex 即可生成题目文档。因此需要安装$tex$发行版，或在[overleaf](https://cn.overleaf.com/)等在线$latex$平台上编译。

目前具有以下功能：
- 添加题目
- 选择章节（可选多个），预览各章节各类型题目数量，并导出题目
- 自选是否导出解答

本程序已在 Windows 10 上测试可用。

#### Required Python packages
- webbrowser, requests
- PyQt5, PyQtWebEngine, datetime, sys, os, configparser, re

#### 使用方法

运行 questions.py

#### 更新记录

ver. 2010.03.06
- 第一版
