### 数学题库

本软件是为管理数学题目而设计，目的是解决数学题目录入困难和自由组织导出题目等问题，避免每学期都要花大量时间出练习题给学生。

共设置六类题目类型，每道题目可添加题干、解答、所属章节（以同济七版高等数学为参考）、难度和题目来源。具体区别如下：

- 单选题：题干只能有一个待填空位；答案支持最多4个选项，至少需要填写A、B两项
- 多选题：题干可以有1-4个待填空位；答案支持最多4个选项，至少需要填写A、B两项；每个空位支持指定多个答案
- 判断题：可设定题干正确或错误
- 填空题：题干可以有1-4个待填空位；每个空位对应一个答案
- 计算题：只能录入题干和解答
- 证明题：只能录入题干和解答
  
在添加过程中支持预览，预览以 MathJax 渲染公式，支持大部分 $latex$ 语法。

导出的题目实际上是$latex$源码，编译 template.tex 即可生成题目文档。因此需要安装$tex$发行版，或在[overleaf](https://cn.overleaf.com/)等在线$latex$平台上编译。

目前具有以下功能：
- 浏览题库中的题目，可按章节和题目类型筛选
- 添加、修改、删除题目
- 导出题目时可选择多个章节，将提示各章节各类型题目数量
- 自选是否导出解答

本程序已在 Windows 10 上测试可用。

#### 计划功能
- 乱序导出
- 导出html页面
- 按题目难度筛选导出
- 添加、修改、删除章节
- 添加、修改、删除难度
- 添加、修改、删除题目来源
- 自由选择题目导出
- 保存、读取导出题目id

#### Required Python packages
- webbrowser, requests
- PyQt5, PyQtWebEngine, datetime, sys, os, configparser, regex

#### 使用方法

运行 questions.py

#### 更新记录
ver. 2020.03.12
- 输入题干和计算题证明题解答、其余题型解析时支持用`\sub`表示子问题

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
