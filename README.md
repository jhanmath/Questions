### 数学题库

#### 软件介绍

本软件是为管理数学题目而设计，目的是解决数学题目录入困难和自由组织导出题目等问题，避免每学期都要花大量时间出练习题给学生。

共设置六类题目类型，每道题目可添加题干、解答、所属章节（以同济七版高等数学为参考）、难度和题目来源。各题型特征如下：

- 单选题：题干只能有一个待填空位；答案支持最多4个选项，至少需要填写A、B两项
- 多选题：题干可以有 1-4 个待填空位；答案支持最多4个选项，至少需要填写A、B两项；每个空位支持指定多个答案
- 判断题：可设定题干正确或错误
- 填空题：题干可以有 1-4 个待填空位；每个空位对应一个答案
- 计算题：只能录入题干和解答
- 证明题：只能录入题干和解答
  
在添加过程中支持预览，预览以 MathJax 渲染公式，支持大部分 $\LaTeX$ 语法，具体支持的命令可以参见[这里](https://docs.mathjax.org/en/latest/input/tex/macros/index.html)。另外针对 MathJax 渲染添加了以下宏：

| 宏 | 显示为 |
| ----- | -------- |
| \Prj | $\text{Prj}$ |
| \oiint | $\unicode{x222F}$ |
| \oiiint | $\unicode{x2230}$ |

可导出的文档格式有两种
1. $\LaTeX$ 源码( .tex )，用 `xelatex` 编译即可生成题目文档。因此需要安装 $\TeX$ 发行版，或在[overleaf](https://cn.overleaf.com/)等在线 $\LaTeX$ 平台上编译。
2. HTML文件( .html )，用浏览器打开即可，可打印成 pdf 文档。请注意该文档需联网才能正确显示公式，且该文档中对于 MathJax 不支持的 $\LaTeX$ 环境或命令，如 `minipage` 环境、 `tikz` 环境等，将不显示或显示为警告信息。

本软件目前主要功能如下：
- 浏览题库中的题目，可按章节和题目类型筛选
- 添加、修改、删除题目
- 导出题目时可选择多个章节，将提示各章节各类型题目数量
- 导出题目时将同时导出所选题目的id，可以随时导入
- 可以在题库中自由选题（逐道勾选），自由选题时可以导入以前导出的题目id，导入后的题目顺序和选项顺序和之前一致
- 导出选项包括
  - 指定各类型题目数量
  - 包含解答（解答在所有题目后面）
  - 解答跟随小题
  - 主观题后留空 (同时选中“主观题后留空”和“解答跟随小题”时，在 tex 文件中可以通过更改 \usetag 来选择显示解答还是显示空白还是同时显示，在html文件中将同时显示)
  - 打乱题目顺序
  - 打乱选择题选项顺序
  - 指定导出文档的标题
  - 按难度筛选

本程序已在 Windows 10 上测试可用。

#### 计划功能
- 添加、修改、删除章节、难度、题目来源
- 新建数据库
- 开发在线版

#### 已知问题
- tabular, minipage, tikzpicture 环境不能被 html 识别

#### Required Python packages
- webbrowser, requests
- PyQt5, PyQtWebEngine, sys, os, configparser, regex, random, datetime

#### 使用方法

运行 questions.py

#### 更新记录
ver. 2020.04.14
- 添加文本框用以输入导出习题集的标题
- 导入题目id时支持读取选项顺序，在自由选题时如果删去题目则将丢失选项顺序，新选中的题目采取默认选项顺序
- 子问题命令变更为`\subq`

ver. 2020.04.06
- 支持导出html
- 支持自由选择题目导出
- 从按章节导出保留题目切换至自由选题导出
- 按章节导出时可指定各类型题目数量，系统将随机抽取指定数量的题目，抽取原则基本遵循题目数量较多的章节中抽取的概率较大。
- 导出时可使选择题选项随机排序（导入题目id功能暂不能导入选择题选项顺序）
- 同时选中“主观题后留空”和“解答跟随小题”时，在tex文件中可以通过更改\usetag来选择显示解答还是显示空白还是同时显示，在html文件中将同时显示

ver. 2020.03.19
- 保存、读取导出题目 id

ver. 2020.03.16
- 增加按难度筛选题目
- 可以在主观题后加入空白
- 可选题目乱序
  
ver. 2020.03.15
- 增加导出解答紧跟题目选项，选中后每一小题的解答将出现在该题目之后；不选中时所有解答统一出现在文档最后
- 修复若干字符转换 bug

ver. 2020.03.12
- 输入所有题干、计算题证明题解答、以及其余题型解析时，支持用`\sub`表示子问题

ver. 2020.03.11
- 增加删除题目功能
- 增加复制题目功能
- 在导出题目标签页上，选择章节的控件更换为树状
- 界面微调
  
ver. 2020.03.10
- 增加修改题目功能
  
ver. 2020.03.07
- 修改界面为3个标签页：题库概览，录入与修改题目，导出题目
- 在题库概览标签页上可以浏览选中章节中的题目，并按题目类型筛选
- 导出选择题时自动判断选项以1、2或4列显示
- 添加题目窗口上设置了快捷键

ver. 2010.03.06
- 第一版
