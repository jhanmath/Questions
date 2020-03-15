# -*- coding: utf-8 -*-

from PyQt5.QtCore import QDir
import regex

def mathlength(string):
    string_altered = string
    frac = regex.findall(r'(\\frac{([^{}]+|(?1))*}{([^{}]++|(?2))*})', string_altered)
    if frac:
        for i in range(len(frac)):
            if len(frac[i][1]) > len(frac[i][2]):
                string_altered = string_altered.replace(frac[i][0], frac[i][1])
            else:
                string_altered = string_altered.replace(frac[i][0], frac[i][2])
    commands = regex.findall(r'(\\.*?)(?:[^a-zA-Z])', string_altered)
    for command in commands:
        string_altered = string_altered.replace(command, 'a')
    # print(string, string_altered)
    total_len = len(string_altered.encode('gb18030'))
    return total_len

def format_questiondata_to_html(question, question_type, number='', fromdatabase=0): # 将题目转化为html，参数为问题数据，问题类型，问题编号（默认为空）
    if number == '':
        format_number = number
    else:
        format_number = number + '. '
    if question_type == '单选题':
        questionstring = ('<p>' + format_number + format_question_to_html(question[0], '单选题', fromdatabase)
                                    + '</p><p>A. ' + format_enter_to_html(question[1])
                                    + '</p><p>B. ' + format_enter_to_html(question[2]))
        if question[3] != '':
            questionstring += ('</p><p>C. ' + format_enter_to_html(question[3]))
        if question[4] != '':
            questionstring += ('</p><p>D. ' + format_enter_to_html(question[4]))
        questionstring += ('</p><p>答案: ' + question[5]
                           + '</p><p>解析： ' + format_subquestion_to_html(question[6], fromdatabase))
    elif question_type == '多选题':
        answer = ''
        answer_raw = question[5:9]
        for j in range(1, max(answer_raw)+1):
            thisanswer = ''
            for k in range(4):
                if answer_raw[k] == j:
                    thisanswer = thisanswer + chr(k+65)
            answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
        questionstring = ('<p>' + format_number + format_question_to_html(question[0], '多选题', fromdatabase)
                                    + '</p><p>A. ' + format_enter_to_html(question[1])
                                    + '</p><p>B. ' + format_enter_to_html(question[2]))
        if question[3] != '':
            questionstring += ('</p><p>C. ' + format_enter_to_html(question[3]))
        if question[4] != '':
            questionstring += ('</p><p>D. ' + format_enter_to_html(question[4]))
        questionstring += ('</p><p>答案： ' + answer
                            + '</p><p>解析： ' + format_subquestion_to_html(question[9], fromdatabase))
    elif question_type == '判断题':
        answertext = ['错误', '正确']
        questionstring = ('<p>' + format_number + format_question_to_html(question[0], '判断题', fromdatabase)
                                    + '</p><p>答案： ' + answertext[question[1]]
                                    + '</p><p>解析： ' + format_subquestion_to_html(question[2], fromdatabase))
    elif question_type == '填空题':
        if question[4] != '':
            answer = '第1空：%s；第2空：%s；第3空：%s；第四空%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]),format_enter_to_html(question[3]),format_enter_to_html(question[4]))
        elif question[3] != '':
            answer = '第1空：%s；第2空：%s；第3空：%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]),format_enter_to_html(question[3]))
        elif question[2] != '':
            answer = '第1空：%s；第2空：%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]))
        else:
            answer = '第1空：%s' % (format_enter_to_html(question[1]))
        questionstring = ('<p>' + format_number + format_question_to_html(question[0], '填空题', fromdatabase)
                                    + '</p><p>答案： ' + answer
                                    + '</p><p>解析： ' + format_subquestion_to_html(question[5], fromdatabase))
    elif question_type == '计算题':
        questionstring = ('<p>' + format_question_to_html(question[0], '计算题', fromdatabase)
                                    + '</p><p>解： ' + format_subquestion_to_html(question[1], fromdatabase))
    elif question_type == '证明题':
        questionstring = ('<p>' + format_question_to_html(question[0], '证明题', fromdatabase)
                                    + '</p><p>证明： ' + format_subquestion_to_html(question[1], fromdatabase))
    return questionstring


# path = QDir.current().filePath(r'MathJax-3.0.1/es5/tex-mml-chtml.js') 
# mathjax = QUrl.fromLocalFile(path).toString()
def gethtml(width, contents=''):
    mathjax = QDir.currentPath() + r'/MathJax-3.0.1/es5/tex-mml-chtml.js'
    pageSourceHead1 = r'''
    <html><head>
    <script>
        window.MathJax = {
            loader: {load: ['[tex]/physics']},
            tex: {
                packages: {'[+]': ['physics']},
                inlineMath: [['$','$'],['\\(','\\)']],
                macros: {
                    Prj: "{\\text{Prj}}",
                }
            }
        };
        </script>
    <script type="text/javascript" id="MathJax-script" async src="''' + mathjax + r'''"></script>
    <style>
        body {
            margin: 0 auto;
            width: '''
    pageSourceHead2 = r'''px;
        }
        p {
            font-size: 18pt;
        }
    </style>
    </head>
    <body>
    <p>'''
    pageSourceFoot = r'''</p>
    </body>
    </html>'''
    return pageSourceHead1 + str(width-5) + pageSourceHead2 + contents + pageSourceFoot

def transform_latex_to_plaintext(question): # 从数据库latex转换为窗口输入的文字
    # 将数学环境以外的\\删除
    mathenv1_regex = ['\\$\\$', '\\$', '\\\\\\(', '\\\\\\[', '\\\\begin\{equation\}']
    mathenv2_regex = ['\\$\\$', '\\$', '\\\\\\)', '\\\\\\]', '\\\\end\{equation\}']
    text = question.strip()
    pattern = '(?>' + mathenv1_regex[0] + '(?>.|\\n)*?' + mathenv2_regex[0] + ')'
    for i in range(1, len(mathenv1_regex)):
        pattern += ('|' + '(?>' + mathenv1_regex[i] + '(?>.|\\n)*?' + mathenv2_regex[i] + ')')
    text_splited = regex.split(pattern, text)
    keepstring = regex.findall(pattern, text)
    text = text_splited[0].replace('\\\\\n', '\n')
    for i in range(len(keepstring)):
        text += (keepstring[i] + text_splited[i+1].replace('\\\\\n', '\n'))

    text = text.replace('\t\t\\begin{enumerate}[(1)]\n', '')
    text = text.replace('\\begin{enumerate}[(1)]\n', '')
    text = text.replace('\t\t\\end{enumerate}\n', '')
    text = text.replace('\t\t\\end{enumerate}', '')
    text = text.replace('\t\t\t\\item', '\\sub')
    text, _ = regex.subn(r'\\n(?>\\t)+', r'\n', text)
    text, _ = regex.subn( r'\\blank[(\d+)em]', r'\\blank{\1}', text)
    return text

def format_question_to_html(question, question_type, fromdatabase = 0): # 将题干转化为html
    text = question.strip()
    if fromdatabase == 1:
        text = transform_latex_to_plaintext(text)
    newtext = format_blank_to_html(text, question_type)
    newtext = format_subquestion_to_html(newtext)
    return newtext

def format_enter_to_html(text):
    # 将数学环境以外的回车改成</br>
    mathenv1_regex = ['\\$\\$', '\\$', '\\\\\\(', '\\\\\\[', '\\\\begin\{equation\}']
    mathenv2_regex = ['\\$\\$', '\\$', '\\\\\\)', '\\\\\\]', '\\\\end\{equation\}']
    newtext = text.strip()
    pattern = '(?>' + mathenv1_regex[0] + '(?>.|\\n)*?' + mathenv2_regex[0] + ')'
    for i in range(1, len(mathenv1_regex)):
        pattern += ('|' + '(?>' + mathenv1_regex[i] + '(?>.|\\n)*?' + mathenv2_regex[i] + ')')
    text_splited = regex.split(pattern, newtext)
    keepstring = regex.findall(pattern, newtext)
    newtext = text_splited[0].replace('\n', '</br>')
    for i in range(len(keepstring)):
        newtext += (keepstring[i] + text_splited[i+1].replace('\n', '</br>'))
    return newtext

def format_subquestion_to_html(question, fromdatabase = 0): # 格式化字符串中的子问题
    text = question.strip()
    if fromdatabase == 1:
        text = transform_latex_to_plaintext(text)
    text = format_enter_to_html(text)
    text , _ = regex.subn(r'(?>\\sub)+', r'\sub', text) # 连续出现多个\sub的话，替换为1个
    num = text.count(r'\sub')
    if num == 0:
        return text
    splited = text.split(r'\sub')
    while len(splited[-1]) and splited[-1][0] == '\n':
        splited[-1]=splited[-1][1:]
    splited[-1] = ('(%d)' % (num)) + splited[-1]
    for i in range(len(splited)-2, 0, -1):
        while splited[i][0] == '\n':
            splited[i]=splited[i][1:]
        if splited[i][len(splited[i])-1] != '\n':
            splited[i] += '\n'
        splited.insert(i,'(%d)' % (i))
    if len(splited[0]) and splited[0][-1] != '\n':
        splited[0] = splited[0] + '\n'
    return ''.join(splited)

def format_blank_to_html(question, question_type): # 格式化字符串中的空括号和空填空
    text = question.strip()
    if question_type == '单选题' or question_type == '多选题':
        delimiter = r'"\\emptychoice"'
        pattern = r'\emptychoice'
        text_splited = regex.split(delimiter, question)
        keepstring = regex.findall(delimiter, question)
        for i in range(len(text_splited)):
            s = text_splited[i].replace(pattern, '（&emsp;）')
            text_splited[i] = s
        newtext = text_splited[0]
        for i in range(len(keepstring)):
            newtext += (keepstring[i] + text_splited[i+1])
    elif question_type == '填空题':
        delimiter = r'"\\blank"|"\\blank\[\d+em\]"'
        pattern = r'\\blank\[(\d+)em\]'
        text_splited = regex.split(delimiter, question)
        keepstring = regex.findall(delimiter, question)
        for i in range(len(text_splited)):
            s = text_splited[i]
            lengths = list(set(regex.findall(pattern, s)))
            for j in lengths:
                blank = '<span style="text-decoration:underline">'
                for k in range(int(j)):
                    blank += '&emsp;'
                blank += '</span>'
                s = s.replace(r'\blank[' + j + 'em]', blank)
            s = s.replace(r'\blank', '<span style="text-decoration:underline">&emsp;&emsp;&emsp;</span>')
            text_splited[i] = s
        newtext = text_splited[0]
        for i in range(len(keepstring)):
            newtext += (keepstring[i] + text_splited[i+1])
    else:
        return question
    return newtext

def format_question_to_latex(question, question_type): # 将题干转化为latex
    newtext = format_blank_to_latex(question, question_type)
    newtext = format_enter_to_latex(newtext)
    newtext = format_subquestion_to_latex(newtext)
    return newtext

def format_explain_to_latex(text):
    # 以下两函数顺序不能更改
    newtext = format_enter_to_latex(text)
    newtext = format_subquestion_to_latex(newtext)
    return newtext

def format_subquestion_to_latex(question): # 格式化字符串中的子问题
    text = question.strip()
    text , _ = regex.subn(r'(?>\\sub)+', r'\sub', text) # 连续出现多个\sub的话，替换为1个
    num = text.count(r'\sub')
    if num == 0:
        return text
    splited = text.split(r'\sub')
    splited[-1]=splited[-1].strip()
    if splited[-1].find('\\\\\n') == -1: # 如果最后一段没有回车，则在末尾添加所需字符
        splited[-1] += ('\n\t\t\\end{enumerate}')
    else: # 如果最后一段有回车，则将第1个回车替换为所需字符
        splited[-1] = splited[-1].replace('\\\\\n','\\\\\n\t\t\\end{enumerate}\n\t\t', 1)
    splited[-1] = '\t\t\t\\item ' + splited[-1]
    for i in range(len(splited)-2, 0, -1):
        splited[i] = splited[i].strip()
        splited[i] = splited[i].replace('\\\\\n', '\\\\\n\t\t\t\t')
        if splited[i][-2:] == '\\\\': # 删除最后的\\
            splited[i] = splited[i][:-2]
        splited[i] += '\n'
        splited.insert(i,'\t\t\t\\item ')
    splited[0] = splited[0].strip()
    splited[0] = splited[0].replace('\\\\\n', '\\\\\n\t\t')
    if splited[0][-2:] == '\\\\': # 删除最后的\\
        splited[0] = splited[0][:-2]
    splited[0] = splited[0] + '\n'    
    splited.insert(1, '\t\t\\begin{enumerate}[(1)]\n')
    return ''.join(splited)

def format_blank_to_latex(question, question_type): # 格式化字符串中的空括号和空填空
    text = question.strip()
    if question_type == '单选题' or question_type == '多选题':
        delimiter = r'"\emptychoice"'
        pattern = r'(\\emptychoice)([^ ])'
        text_splited = regex.split(delimiter, question)
        keepstring = regex.findall(delimiter, question)
        keepstring_formated = [r'\varb+' + s  + '+' for s in keepstring]
        for i in range(len(text_splited)):
            s, _ =regex.subn(pattern, r'\1 \2', text_splited[i])
            text_splited[i] = s
        newtext = text_splited[0]
        for i in range(len(keepstring_formated)):
            newtext += (keepstring_formated[i] + text_splited[i+1])
    elif question_type == '填空题':
        delimiter = r'"\\blank"|"\\blank{\d+}"'
        pattern = r'(\\blank)([^ |{])'
        text_splited = regex.split(delimiter, question)
        keepstring = regex.findall(delimiter, question)
        keepstring_formated = [r'\varb+' + s  + '+' for s in keepstring]
        for i in range(len(text_splited)):
            s, _ =regex.subn(pattern, r'\1 \2', text_splited[i])
            s, _ =regex.subn(r'\\blank{(\d+)}', r'\\blank[\1em]', s)
            text_splited[i] = s
        newtext = text_splited[0]
        for i in range(len(keepstring_formated)):
            newtext += (keepstring_formated[i] + text_splited[i+1])
    else:
        return question
    return newtext

def format_enter_to_latex(text): # 将latex环境以外的回车改为\\+回车
    mathenv1 = ['$$', '$', '\\(', '\\[', '\\begin{']
    mathenv2 = ['$$', '$', '\\)', '\\]', '\\end{']
    mathenv1_regex = ['\\$\\$', '\\$', '\\\\\\(', '\\\\\\[', '\\\\begin\{']
    mathenv2_regex = ['\\$\\$', '\\$', '\\\\\\)', '\\\\\\]', '\\\\end\{']
    origin_text = text.strip()
    pattern = '(?>' + mathenv1_regex[0] + '(?>.|\\n)*?' + mathenv2_regex[0] + ')'
    for i in range(1, len(mathenv1_regex)):
        pattern += ('|' + '(?>' + mathenv1_regex[i] + '(?>.|\\n)*?' + mathenv2_regex[i] + ')')
    text_splited = regex.split(pattern, origin_text)
    keepstring = regex.findall(pattern, origin_text)
    newtext = text_splited[0].replace('\n', '\\\\\n')
    for i in range(len(keepstring)):
        newtext += (keepstring[i] + text_splited[i+1].replace('\n', '\\\\\n'))
    for i in range(len(mathenv1)): # 将环境开头前和结尾后的\\删除
        newtext = newtext.replace('\\\\'+mathenv1[i], mathenv1[i])
        newtext = newtext.replace(mathenv2[i]+'\\\\', mathenv2[i])
    newtext, _ = regex.subn(r'(\\end\{.*?\})\\\\', r'\1', newtext)
    return newtext

def find_text_enter(text):
    pass
