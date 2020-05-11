# -*- coding: utf-8 -*-

from PyQt5.QtCore import QDir
import regex
from random import shuffle
from datetime import datetime
import random
import latex
import database as mydb

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

 # 将题目转化为html，参数为问题数据，问题类型，问题编号（默认为空），是否从数据库读取，type=0表示同时输出问题和答案，1表示只有问题，2表示只有答案
def format_questiondata_to_html(question, question_type, number='', fromdatabase=0, output_type=0):
    if number == '':
        format_number = number
    else:
        format_number = number + '. '
    if question_type == '单选题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '单选题', fromdatabase)
                                        + '</p><p>A. ' + format_enter_to_html(question[1])
                                        + '</p><p>B. ' + format_enter_to_html(question[2]) + '</p>')
            if question[3] != '':
                questionstring += ('<p>C. ' + format_enter_to_html(question[3]) + '</p>')
            if question[4] != '':
                questionstring += ('<p>D. ' + format_enter_to_html(question[4]) + '</p>')
        if output_type == 0 or output_type == 2:
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('答案: ' + question[5]
                            + '</p><p>解析： ' + format_subquestion_to_html(question[6], fromdatabase) + '</p>')
    elif question_type == '多选题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '多选题', fromdatabase)
                                        + '</p><p>A. ' + format_enter_to_html(question[1])
                                        + '</p><p>B. ' + format_enter_to_html(question[2]) + '</p>')
            if question[3] != '':
                questionstring += ('<p>C. ' + format_enter_to_html(question[3]) + '</p>')
            if question[4] != '':
                questionstring += ('<p>D. ' + format_enter_to_html(question[4]) + '</p>')
        if output_type == 0 or output_type == 2:
            answer = ''
            answer_raw = question[5:9]
            for j in range(1, max(answer_raw)+1):
                thisanswer = ''
                for k in range(4):
                    if answer_raw[k] == j:
                        thisanswer = thisanswer + chr(k+65)
                answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('答案： ' + answer
                                + '</p><p>解析： ' + format_subquestion_to_html(question[9], fromdatabase) + '</p>')
    elif question_type == '判断题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '判断题', fromdatabase) + '</p>')
        if output_type == 0 or output_type == 2:
            answertext = ['错误', '正确']
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('答案： ' + answertext[question[1]]
                                + '</p><p>解析： ' + format_subquestion_to_html(question[2], fromdatabase) + '</p>')
    elif question_type == '填空题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '填空题', fromdatabase) + '</p>')
        if output_type == 0 or output_type == 2:
            if question[4] != '':
                answer = '第1空：%s；第2空：%s；第3空：%s；第四空%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]),format_enter_to_html(question[3]),format_enter_to_html(question[4]))
            elif question[3] != '':
                answer = '第1空：%s；第2空：%s；第3空：%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]),format_enter_to_html(question[3]))
            elif question[2] != '':
                answer = '第1空：%s；第2空：%s' % (format_enter_to_html(question[1]),format_enter_to_html(question[2]))
            else:
                answer = '第1空：%s' % (format_enter_to_html(question[1]))
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('答案： ' + answer
                            + '</p><p>解析： ' + format_subquestion_to_html(question[5], fromdatabase) + '</p>')
    elif question_type == '计算题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '计算题', fromdatabase) + '</p>')
        if output_type == 0 or output_type == 2:
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('解： ' + format_subquestion_to_html(question[1], fromdatabase) + '</p>')
    elif question_type == '证明题':
        questionstring = ''
        if output_type == 0 or output_type == 1:
            questionstring += ('<p>' + format_number + format_question_to_html(question[0], '证明题', fromdatabase) + '</p>')
        if output_type == 0 or output_type == 2:
            questionstring += '<p>'
            if output_type == 2:
                questionstring += format_number
            questionstring += ('证明： ' + format_subquestion_to_html(question[1], fromdatabase) + '</p>')
    return questionstring


# path = QDir.current().filePath(r'MathJax-3.0.1/es5/tex-mml-chtml.js') 
# mathjax = QUrl.fromLocalFile(path).toString()
def gethtml(width, contents=''):
    mathjax = QDir.currentPath() + r'/MathJax-3.0.5/es5/tex-mml-chtml.js'
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
    <meta charset="UTF-8">
    </head>
    <body>
    '''
    pageSourceFoot = r'''
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
    text, _ = regex.subn( r'\\blank\[(\d+)em\]', r'\\blank{\1}', text)
    return text

def format_question_to_html(question, question_type, fromdatabase = 0): # 将题干转化为html
    text = question.strip()
    if fromdatabase == 1:
        text = transform_latex_to_plaintext(text)
    newtext = format_blank_to_html(text, question_type)
    newtext = format_subquestion_to_html(newtext)
    return newtext

def format_oint_to_html(text): # 数学环境内的特殊字符处理
    mathenv1_regex = ['\\$', '\\\\\\(', '\\$\\$', '\\\\\\[', '\\\\begin\{equation']
    mathenv2_regex = ['\\$', '\\\\\\)', '\\$\\$', '\\\\\\]', '\\\\end\{equation']
    newtext = text.strip()
    for i in range(2):
        pattern = '(?>' + mathenv1_regex[i] + '(?>.|\\n)*?' + mathenv2_regex[i] + ')'
        text_outside = regex.split(pattern, newtext) # 数学环境之外的字符
        text_in_mathenv = regex.findall(pattern, newtext) # 数学环境之内的字符
        for j in range(len(text_in_mathenv)):
            text_in_mathenv[j] = text_in_mathenv[j].replace(r'\oiint',r'\subset\!\!\!\!\!\supset\kern-1.55em\iint').replace(r'\oiiint',r'\subset\!\!\!\!\!\supset\kern-1.75em\iiint')
        newtext = text_outside[0]
        for j in range(len(text_in_mathenv)):
            newtext += (text_in_mathenv[j] + text_outside[j+1])
    for i in range(2,5):
        pattern = '(?>' + mathenv1_regex[i] + '(?>.|\\n)*?' + mathenv2_regex[i] + ')'
        text_outside = regex.split(pattern, newtext) # 数学环境之外的字符
        text_in_mathenv = regex.findall(pattern, newtext) # 数学环境之内的字符
        for j in range(len(text_in_mathenv)):
            text_in_mathenv[j] = text_in_mathenv[j].replace(r'\oiint',r'\subset\!\!\!\!\!\supset\kern-1.8em\iint').replace(r'\oiiint',r'\subset\!\!\!\supset\kern-2.3em\iiint')
        newtext = text_outside[0]
        for j in range(len(text_in_mathenv)):
            newtext += (text_in_mathenv[j] + text_outside[j+1])
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
    return format_oint_to_html(newtext)

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
        delimiter = r'"\\blank"|"\\blank\{\d+\}"'
        pattern = r'\\blank\{(\d+)\}'
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
                s = s.replace(r'\blank{' + j + '}', blank)
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

def export_to_latex(schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,options={'follow':True,'white':False, 'solution':True, 'randomchoice': False},schoice_choiceseq=[],mchoice_choiceseq=[]):
    if options['random']:
        shuffle(schoiceid)
        shuffle(mchoiceid)
        shuffle(tofid)
        shuffle(calculationid)
        shuffle(blankid)
        shuffle(proofid)
    num_proof = len(proofid)
    num_calculation = len(calculationid)
    num_blank = len(blankid)
    num_tof = len(tofid)
    num_mchoice = len(mchoiceid)
    num_schoice = len(schoiceid)

    try:
        filename = ('questions[%s]' % datetime.now().strftime('%Y-%m-%dT%H-%M-%S'))
        filepath = ('%s/exports/%s.tex' % (QDir.currentPath(), filename))
        f = open(filepath, 'w', encoding='utf-8')
        f.writelines(latex.docclass)
        if (not options['follow']) and (options['white']):
            f.writelines(latex.preamble.replace('\\usetag{sol}','\\usetag{nosol}'))
        else:
            f.writelines(latex.preamble)
        f.writelines(options['title'])
        f.writelines(latex.begindocument)
        if options['randomchoice']:
            sequence_type = 1 # 重新随机生成排列选项
            schoice_choiceseq_new = []
            mchoice_choiceseq_new = []
        else:
            if schoice_choiceseq == [] and mchoice_choiceseq == []:
                sequence_type = 0 # 不随机排列选项
                schoice_choiceseq_new = []
                mchoice_choiceseq_new = []
            else:
                sequence_type = 2 # 使用导入的随机排列选项，不需要重新生成
                schoice_choiceseq_new = schoice_choiceseq
                mchoice_choiceseq_new = mchoice_choiceseq
        # 写入单选题
        if num_schoice>0:
            f.writelines('\\section{单项选择题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_schoice):
                thisquestion = mydb.get_schoice_by_id(schoiceid[i])
                num_of_choices = 2
                while num_of_choices <4 and thisquestion[num_of_choices+1] != '':
                    num_of_choices += 1

                if sequence_type == 1: # 重新随机生成排列选项
                    sequence = generate_random_choice(num_of_choices)
                    schoice_choiceseq_new.append(sequence)
                elif sequence_type == 2: # 采用已有排列
                    sequence = schoice_choiceseq[i]
                elif sequence_type == 0:
                    schoice_choiceseq_new.append(j for j in range(1,num_of_choices+1))
                if sequence_type == 1 or sequence_type == 2:    
                    thisquestion = make_choices_random(thisquestion, sequence, '单选题')
                
                f.writelines('\t\\item ')
                write_schoice_question(f, thisquestion)
                if options['follow']:
                    f.writelines('\t\t\\tagged{sol}{答案：')
                    write_schoice_solution(f, thisquestion)
                    f.writelines('\t\t}')
            f.writelines('\\end{enumerate}\n')
        # 写入多选题
        if num_mchoice>0:
            f.writelines('\\section{多项选择题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_mchoice):
                thisquestion = mydb.get_mchoice_by_id(mchoiceid[i])
                num_of_choices = 2
                while num_of_choices <4 and thisquestion[num_of_choices+1] != '':
                    num_of_choices += 1

                if sequence_type == 1: # 生成选项排列
                    sequence = generate_random_choice(num_of_choices)
                    mchoice_choiceseq_new.append(sequence)
                elif sequence_type == 2: # 采用已有排列
                    sequence = mchoice_choiceseq[i]
                elif sequence_type == 0:
                    mchoice_choiceseq_new.append(j for j in range(1,num_of_choices+1))
                if sequence_type == 1 or sequence_type == 2:
                    thisquestion = make_choices_random(thisquestion, sequence, '多选题')
                    
                f.writelines('\t\\item ')
                write_schoice_question(f, thisquestion)
                if options['follow']:
                    f.writelines('\t\t\\tagged{sol}{答案：')
                    write_mchoice_solution(f, thisquestion)
                    f.writelines('\t\t}')
            f.writelines('\\end{enumerate}\n')
        # 写入判断题
        if num_tof>0:
            f.writelines('\\section{判断题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_tof):
                thisquestion = mydb.get_tof_by_id(tofid[i])
                f.writelines('\t\\item ')
                write_tof_question(f, thisquestion)
                if options['follow']:
                    f.writelines('\t\t\\tagged{sol}{\\\\答案：')
                    write_tof_solution(f, thisquestion)
                    f.writelines('\t\t}\n')
            f.writelines('\\end{enumerate}\n')
        # 写入填空题
        if num_blank>0:
            f.writelines('\\section{填空题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_blank):
                thisquestion = mydb.get_blank_by_id(blankid[i])
                f.writelines('\t\\item ')
                write_blank_question(f, thisquestion)
                if options['follow']:
                    # if thisquestion[0][-1] != '}':
                    #     f.writelines('\\\\')
                    f.writelines('\t\t\\tagged{sol}{\\\\答案：')
                    write_blank_solution(f, thisquestion)
                    f.writelines('\t\t}')
                else:
                    f.writelines('\n')
            f.writelines('\\end{enumerate}\n')
        # 写入计算题
        if num_calculation>0:
            f.writelines('\\section{计算题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_calculation):
                thisquestion = mydb.get_calculation_by_id(calculationid[i])
                f.writelines('\t\\item ')
                write_calculation_question(f, thisquestion)
                if options['follow']:
                    f.writelines('\t\t\\tagged{sol}{')
                    if thisquestion[0][-1] != '}':
                        f.writelines('\\\\')
                    f.writelines('\n')
                    write_calculation_soltuion(f, thisquestion)
                    f.writelines('\t\t}')
                if options['white']:
                    f.writelines('\\tagged{nosol}{\\vspace{4.8cm}}\n')
                else:
                    f.writelines('\n')
            f.writelines('\\end{enumerate}\n')
        # 写入证明题
        if num_proof>0:
            f.writelines('\\section{证明题}\n')
            f.writelines('\\begin{enumerate}\n')
            for i in range(num_proof):
                thisquestion = mydb.get_proof_by_id(proofid[i])
                f.writelines('\t\\item ')
                write_proof_question(f, thisquestion)
                if options['follow']:
                    f.writelines('\t\t\\tagged{sol}{')
                    if thisquestion[0][-1] != '}':
                        f.writelines('\\\\')
                    f.writelines('\n')
                    write_proof_soltuion(f, thisquestion)
                    f.writelines('\t\t}')
                if options['white']:
                    f.writelines('\\tagged{nosol}{\\vspace{4cm}}\n')
                else:
                    f.writelines('\n')
            f.writelines('\\end{enumerate}\n')

        # 单独写入解答
        if options['solution'] and (not options['follow']):
            f.writelines('\\tagged{sol}{\n')
            # 单选题解答
            if num_schoice>0:
                f.writelines('\\section{单项选择题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_schoice):
                    thisquestion = mydb.get_schoice_by_id(schoiceid[i])
                    if sequence_type == 1 or sequence_type == 2:
                        sequence = schoice_choiceseq_new[i]
                        thisquestion = make_choices_random(thisquestion, sequence, '单选题')
                    f.writelines('\t\\item ')
                    write_schoice_solution(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            # 多选题解答
            if num_mchoice>0:
                f.writelines('\\section{多项选择题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_mchoice):
                    thisquestion = mydb.get_mchoice_by_id(mchoiceid[i])
                    if sequence_type == 1 or sequence_type == 2:
                        sequence = mchoice_choiceseq_new[i]
                        thisquestion = make_choices_random(thisquestion, sequence, '多选题')
                    f.writelines('\t\\item ')
                    write_schoice_solution(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            # 判断题解答
            if num_tof>0:
                f.writelines('\\section{判断题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_tof):
                    thisquestion = mydb.get_tof_by_id(tofid[i])
                    f.writelines('\t\\item ')
                    write_tof_solution(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            # 填空题解答
            if num_blank>0:
                f.writelines('\\section{填空题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_blank):
                    thisquestion = mydb.get_blank_by_id(blankid[i])
                    f.writelines('\t\\item ')
                    write_blank_solution(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            # 计算题解答
            if num_calculation>0:
                f.writelines('\\section{计算题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_calculation):
                    thisquestion = mydb.get_calculation_by_id(calculationid[i])
                    f.writelines('\t\\item ')
                    write_calculation_soltuion(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            # 证明题解答
            if num_proof>0:
                f.writelines('\\section{证明题解答}\n')
                f.writelines('\\begin{enumerate}\n')
                for i in range(num_proof):
                    thisquestion = mydb.get_proof_by_id(proofid[i])
                    f.writelines('\t\\item ')
                    write_proof_soltuion(f, thisquestion)
                f.writelines('\\end{enumerate}\n')
            f.writelines('}')
        f.writelines(latex.enddocument)
        f.close()
        id_file_result = export_questionid(filename,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,schoice_choiceseq_new,mchoice_choiceseq_new)
        return 1, filename
    except Exception as e:
        return 0, e

def write_schoice_question(f, schoice):
    f.writelines('%s\n' % (schoice[0]))
    maxlen = max(mathlength(schoice[1]), mathlength(schoice[2]), mathlength(schoice[3]), mathlength(schoice[4]))
    para = 4
    if maxlen > 30:
        para = 1
    elif maxlen > 12:
        para = 2
    f.writelines('\t\t\\begin{choice}(%d)\n' % (para))
    f.writelines('\t\t\t\\choice %s\n' % (schoice[1]))
    f.writelines('\t\t\t\\choice %s\n' % (schoice[2]))
    if schoice[3] != '':
        f.writelines('\t\t\t\\choice %s\n' % (schoice[3]))
    if schoice[4] != '':
        f.writelines('\t\t\t\\choice %s\n' % (schoice[4]))
    f.writelines('\t\t\\end{choice}\n')

def write_schoice_solution(f, schoice):
    if schoice[6] != '':
        f.writelines('%s\\\\\n' % (schoice[5]))
        f.writelines('\t\t解析：%s\n' % (schoice[6]))
    else:
        f.writelines('\%s\n' % (schoice[5]))

def write_mchoice_question(f, mchoice):
    f.writelines('%s\n' % (mchoice[0]))
    maxlen = max(mathlength(mchoice[1]), mathlength(mchoice[2]), mathlength(mchoice[3]), mathlength(mchoice[4]))
    para = 4
    if maxlen > 30:
        para = 1
    elif maxlen > 12:
        para = 2
    f.writelines('\t\t\\begin{choice}(4)\n')
    f.writelines('\t\t\t\\choice %s\n' % (mchoice[1]))
    f.writelines('\t\t\t\\choice %s\n' % (mchoice[2]))
    if schoice[i][3] != '':
        f.writelines('\t\t\t\\choice %s\n' % (schoice[i][3]))
    if schoice[i][4] != '':
        f.writelines('\t\t\t\\choice %s\n' % (schoice[i][4]))
    f.writelines('\t\t\\end{choice}\n')

def write_mchoice_solution(f, mchoice):
    answer = ''
    answer_raw = mchoice[5:9]
    for j in range(1, max(answer_raw)+1):
        thisanswer = ''
        for k in range(4):
            if answer_raw[k] == j:
                thisanswer = thisanswer + chr(k+65)
        answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
    if mchoice[9] != '':
        f.writelines('%s\\\\\n' % (answer))
        f.writelines('\t\t解析：%s\n' % (mchoice[9]))
    else:
        f.writelines('%s\n' % (answer))

def write_tof_question(f, tof):
    f.writelines('%s \\hfill\\emptychoice\n' % (tof[0]))

def write_tof_solution(f, tof):
    answer = ['错误', '正确']
    if tof[2] != '':
        f.writelines('%s\\\\\n' % (answer[tof[1]]))
        f.writelines('\t\t解析：%s\n' % (tof[2]))
    else:
        f.writelines('%s\n' % (answer[tof[1]]))

def write_blank_question(f, blank):
    f.writelines('%s' % (blank[0]))

def write_blank_solution(f, blank):
    if blank[4] != '':
        f.writelines('第1空：\\underline{%s}；第2空：\\underline{%s}；第3空：\\underline{%s}；第4空：\\underline{%s}' % (blank[1],blank[2],blank[3],blank[4]))
    elif blank[3] != '':
        f.writelines('第1空：\\underline{%s}；第2空：\\underline{%s}；第3空：\\underline{%s}' % (blank[1],blank[2],blank[3]))
    elif blank[2] != '':
        f.writelines('第1空：\\underline{%s}；第2空：\\underline{%s}' % (blank[1],blank[2]))
    else:
        f.writelines('\\underline{%s}' % (blank[1]))
    if blank[5] != '':
        f.writelines('\\\\\n\t\t解析：%s\n' % (blank[5]))
    else:
        f.writelines('\n')

def write_calculation_question(f, calculation):
    f.writelines('%s' % (calculation[0]))

def write_calculation_soltuion(f, calculation):
    if calculation[1] == '':
        f.writelines('解：略\n')
    else:
        f.writelines('解：%s\n' % (calculation[1]))

def write_proof_question(f, proof):
    f.writelines('%s' % (proof[0]))

def write_proof_soltuion(f, proof):
    if proof[1] != '':
        f.writelines('证明：%s\n' % (proof[1]))
    else:
        f.writelines('证明：略\n')

def export_to_html(schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,options):
    if options['random']:
        shuffle(schoiceid)
        shuffle(mchoiceid)
        shuffle(tofid)
        shuffle(calculationid)
        shuffle(blankid)
        shuffle(proofid)
    num_proof = len(proofid)
    num_calculation = len(calculationid)
    num_blank = len(blankid)
    num_tof = len(tofid)
    num_mchoice = len(mchoiceid)
    num_schoice = len(schoiceid)

    try:
        filename = ('questions[%s]' % datetime.now().strftime('%Y-%m-%dT%H-%M-%S'))
        filepath = ('%s/exports/%s.html' % (QDir.currentPath(), filename))
        pageSourceContent, schoice_choiceseq, mchoice_choiceseq = generate_html_body(schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,options)
        html_source = gethtml(100, pageSourceContent)
        html_source = regex.sub(
            r'<script type="text\/javascript" id="MathJax-script" async src=".*"><\/script>',
            '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>\n<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
            html_source
        )
        html_source = regex.sub(
            r'width: .*px;\n',
            '',
            html_source
        )
        f = open(filepath, 'w', encoding='utf-8')
        f.writelines(html_source)
        f.close()
        id_file_result = export_questionid(filename,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,schoice_choiceseq,mchoice_choiceseq)
        return 1, filename
    except Exception as e:
        return 0, e

def export_questionid(filename,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,schoice_choiceseq,mchoice_choiceseq):
    try:
        filepath = ('%s/exports/%s(id).txt' % (QDir.currentPath(), filename))
        f = open(filepath, 'w', encoding='utf-8')
        f.writelines('[schoice]\n')
        for i in range(len(schoiceid)):
            f.writelines('%d,' % (schoiceid[i]))
            f.writelines('%s\n' % (','.join([str(j) for j in schoice_choiceseq[i]])))
        f.writelines('[mchoice]\n')
        for i in range(len(mchoiceid)):
            f.writelines('%d,' % (mchoiceid[i]))
            f.writelines('%s\n' % (','.join([str(j) for j in mchoice_choiceseq[i]])))
        f.writelines('[tof]\n')
        for i in tofid:
            f.writelines('%d\n' % (i))
        f.writelines('[blank]\n')
        for i in blankid:
            f.writelines('%d\n' % (i))
        f.writelines('[calculation]\n')
        for i in calculationid:
            f.writelines('%d\n' % (i))
        f.writelines('[proof]\n')
        for i in proofid:
            f.writelines('%d\n' % (i))
        f.close()
        return 1
    except Exception as e:
        print(e)
        return 0

def generate_html_body(schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,options={'follow':True,'white':False, 'solution':True, 'randomchoice': False, 'title': ''},schoice_choiceseq=[],mchoice_choiceseq=[]):
    num_schoice = len(schoiceid)
    num_mchoice = len(mchoiceid)
    num_tof = len(tofid)
    num_blank = len(blankid)
    num_calculation = len(calculationid)
    num_proof = len(proofid)
    pageSourceContent = ''
    if options['title']:
        pageSourceContent += ('<h1 style="text-align:center">' + options['title'] + '</h1>')
    chinese_num = ['一','二','三','四','五','六','七','八','九','十','十一','十二']
    sec = -1
    if options['randomchoice']:
        sequence_type = 1 # 重新随机生成排列选项
        schoice_choiceseq_new = []
        mchoice_choiceseq_new = []
    else:
        if schoice_choiceseq == [] and mchoice_choiceseq == []:
            sequence_type = 0 # 不随机排列选项
            schoice_choiceseq_new = []
            mchoice_choiceseq_new = []
        else:
            sequence_type = 2 # 使用导入的随机排列选项，不需要重新生成
            schoice_choiceseq_new = schoice_choiceseq
            mchoice_choiceseq_new = mchoice_choiceseq
    # 写入单选题
    if num_schoice>0:
        sec += 1
        pageSourceContent += ('<h2>%s、单选题</h2>' % (chinese_num[sec]))
        for i in range(num_schoice):
            thisquestion = mydb.get_schoice_by_id(schoiceid[i])
            num_of_choices = 2
            while num_of_choices <4 and thisquestion[num_of_choices+1] != '':
                num_of_choices += 1

            if sequence_type == 1: # 重新随机生成排列选项
                sequence = generate_random_choice(num_of_choices)
                schoice_choiceseq_new.append(sequence)
            elif sequence_type == 2: # 采用已有排列
                sequence = schoice_choiceseq[i]
            elif sequence_type == 0:
                schoice_choiceseq_new.append(j for j in range(1,num_of_choices+1))
            if sequence_type == 1 or sequence_type == 2:    
                thisquestion = make_choices_random(thisquestion, sequence, '单选题')
            
            pageSourceContent += format_questiondata_to_html(thisquestion, '单选题', str(i+1), fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '单选题', fromdatabase=1,output_type=2)
    # 写入多选题
    if num_mchoice>0:
        sec += 1
        pageSourceContent += ('<h2>%s、多选题</h2>' % (chinese_num[sec]))
        for i in range(num_mchoice):
            thisquestion = mydb.get_mchoice_by_id(mchoiceid[i])
            num_of_choices = 2
            while num_of_choices <4 and thisquestion[num_of_choices+1] != '':
                num_of_choices += 1

            if sequence_type == 1: # 生成选项排列
                sequence = generate_random_choice(num_of_choices)
                mchoice_choiceseq_new.append(sequence)
            elif sequence_type == 2: # 采用已有排列
                sequence = mchoice_choiceseq[i]
            elif sequence_type == 0:
                mchoice_choiceseq_new.append(j for j in range(1,num_of_choices+1))
            if sequence_type == 1 or sequence_type == 2:
                thisquestion = make_choices_random(thisquestion, sequence, '多选题')

            pageSourceContent += format_questiondata_to_html(thisquestion, '多选题', str(i+1), fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '多选题', fromdatabase=1,output_type=2)
    # 写入判断题
    if num_tof>0:
        sec += 1
        pageSourceContent += ('<h2>%s、判断题</h2>' % (chinese_num[sec]))
        for i in range(num_tof):
            thisquestion = mydb.get_tof_by_id(tofid[i])
            pageSourceContent += format_questiondata_to_html(thisquestion, '判断题', str(i+1), fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '判断题', fromdatabase=1,output_type=2)
    # 写入填空题
    if num_blank>0:
        sec += 1
        pageSourceContent += ('<h2>%s、填空题</h2>' % (chinese_num[sec]))
        for i in range(num_blank):
            thisquestion = mydb.get_blank_by_id(blankid[i])
            pageSourceContent += format_questiondata_to_html(thisquestion, '填空题', str(i+1), fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '填空题', fromdatabase=1,output_type=2)
    # 写入计算题
    if num_calculation>0:
        sec += 1
        pageSourceContent += ('<h2>%s、计算题</h2>' % (chinese_num[sec]))
        for i in range(num_calculation):
            thisquestion = mydb.get_calculation_by_id(calculationid[i])
            pageSourceContent += format_questiondata_to_html(thisquestion, '计算题', str(i+1), fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '计算题', fromdatabase=1,output_type=2)
            if options['white']:
                pageSourceContent += ''.join(['</br>' for i in range(8)])
    # 写入证明题
    if num_proof>0:
        sec += 1
        pageSourceContent += ('<h2>%s、计算题</h2>' % (chinese_num[sec]))
        for i in range(num_proof):
            thisquestion = mydb.get_proof_by_id(proofid[i])
            pageSourceContent += format_questiondata_to_html(thisquestion, '证明题', fromdatabase=1,output_type=1)
            if options['follow']:
                pageSourceContent += format_questiondata_to_html(thisquestion, '证明题', str(i+1), fromdatabase=1,output_type=2)
            if options['white']:
                pageSourceContent += ''.join(['</br>' for i in range(8)])

    # 单独写入解答
    if options['solution'] and (not options['follow']):
        # 写入单选题
        if num_schoice>0:
            sec += 1
            pageSourceContent += ('<h2>%s、单选题解答</h2>' % (chinese_num[sec]))
            for i in range(num_schoice):
                thisquestion = mydb.get_schoice_by_id(schoiceid[i])
                if sequence_type == 1 or sequence_type == 2:
                    sequence = schoice_choiceseq_new[i]
                    thisquestion = make_choices_random(thisquestion, sequence, '单选题')
                pageSourceContent += format_questiondata_to_html(thisquestion, '单选题', str(i+1), fromdatabase=1,output_type=2)
        # 写入多选题
        if num_mchoice>0:
            sec += 1
            pageSourceContent += ('<h2>%s、多选题解答</h2>' % (chinese_num[sec]))
            for i in range(num_mchoice):
                thisquestion = mydb.get_mchoice_by_id(mchoiceid[i])
                if sequence_type == 1 or sequence_type == 2:
                    sequence = mchoice_choiceseq_new[i]
                    thisquestion = make_choices_random(thisquestion, sequence, '多选题')
                pageSourceContent += format_questiondata_to_html(thisquestion, '多选题', str(i+1), fromdatabase=1,output_type=2)
        # 写入判断题
        if num_tof>0:
            sec += 1
            pageSourceContent += ('<h2>%s、判断题解答</h2>' % (chinese_num[sec]))
            for i in range(num_tof):
                thisquestion = mydb.get_tof_by_id(tofid[i])
                pageSourceContent += format_questiondata_to_html(thisquestion, '判断题', str(i+1), fromdatabase=1,output_type=2)
        # 写入填空题
        if num_blank>0:
            sec += 1
            pageSourceContent += ('<h2>%s、填空题解答</h2>' % (chinese_num[sec]))
            for i in range(num_blank):
                thisquestion = mydb.get_blank_by_id(blankid[i])
                pageSourceContent += format_questiondata_to_html(thisquestion, '填空题', str(i+1), fromdatabase=1,output_type=2)
        # 写入计算题
        if num_calculation>0:
            sec += 1
            pageSourceContent += ('<h2>%s、计算题解答</h2>' % (chinese_num[sec]))
            for i in range(num_calculation):
                thisquestion = mydb.get_calculation_by_id(calculationid[i])
                pageSourceContent += format_questiondata_to_html(thisquestion, '计算题', str(i+1), fromdatabase=1,output_type=2)
        # 写入证明题
        if num_proof>0:
            sec += 1
            pageSourceContent += ('<h2>%s、计算题解答</h2>' % (chinese_num[sec]))
            for i in range(num_proof):
                thisquestion = mydb.get_proof_by_id(proofid[i])
                pageSourceContent += format_questiondata_to_html(thisquestion, '证明题', str(i+1), fromdatabase=1,output_type=2)

    return pageSourceContent, schoice_choiceseq_new, mchoice_choiceseq_new

def generate_random_choice(num):
    choice = [i for i in range(1,num+1)]
    random.shuffle(choice)
    return choice

def make_choices_random(question, sequence, question_type):
    # 根据sequence改变选项位置，例如: [4,1,2,3]表示把原来的第4个选项放在第1个，原来的第1个选项放第2个，依次类推
    thisquestion = question
    num_of_choices = len(sequence)
    if question_type == '单选题':
        choices = thisquestion[1:num_of_choices+1]
        for j in range(num_of_choices):
            thisquestion[1+j] = choices[sequence[j]-1]
        answer = thisquestion[5]
        thisquestion[5]=chr(sequence.index(ord(answer)-64)+1 + 64)
    elif question_type == '多选题':
        choices = thisquestion[1:num_of_choices+1]
        for j in range(num_of_choices):
            thisquestion[1+j] = choices[sequence[j]-1]
        answer = thisquestion[5:5+num_of_choices]
        for j in range(num_of_choices):
            thisquestion[j+5]=answer[sequence[j]-1]
    return thisquestion

def generate_ordered_choice(num):
    choice_seq = [[1,2,3,4] for i in range(num)]
    return choice_seq