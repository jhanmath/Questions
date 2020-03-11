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
    print(string, string_altered)
    total_len = len(string_altered.encode('gb18030'))
    return total_len

def format_question_to_html(question, question_type, number=''): # 问题数据，问题类型，问题编号（默认为空）
    if number == '':
        format_number = number
    else:
        format_number = number + '. '
    if question_type == '单选题':
        questionstring = ('<p>' + format_number + question[0].replace(r'\\', '</br>').replace('\emptychoice','（&emsp;）') 
                                    + '</p><p>A. ' + question[1].replace(r'\\','</br>')
                                    + '</p><p>B. ' + question[2].replace(r'\\','</br>')
                                    + '</p><p>C. ' + question[3].replace(r'\\','</br>')
                                    + '</p><p>D. ' + question[4].replace(r'\\','</br>')
                                    + '</p><p>答案: ' + question[5]
                                    + '</p><p>解析： ' + question[6].replace(r'\\','</br>'))
    if question_type == '多选题':
        answer = ''
        answer_raw = question[5:9]
        for j in range(1, max(answer_raw)+1):
            thisanswer = ''
            for k in range(4):
                if answer_raw[k] == j:
                    thisanswer = thisanswer + chr(k+65)
            answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
        questionstring = ('<p>' + format_number + question[0].replace(r'\\','</br>').replace('\emptychoice','（&emsp;）') 
                                    + '</p><p>A. ' + question[1].replace(r'\\','</br>')
                                    + '</p><p>B. ' + question[2].replace(r'\\','</br>')
                                    + '</p><p>C. ' + question[3].replace(r'\\','</br>')
                                    + '</p><p>D. ' + question[4].replace(r'\\','</br>')
                                    + '</p><p>答案： ' + answer
                                    + '</p><p>解析： ' + question[9].replace(r'\\','</br>'))
    if question_type == '判断题':
        answertext = ['错误', '正确']
        questionstring = ('<p>' + format_number + question[0].replace(r'\\','</br>')
                                    + '</p><p>答案： ' + answertext[question[1]]
                                    + '</p><p>解析： ' + question[2].replace(r'\\','</br>'))
    if question_type == '填空题':
        if question[4] != '':
            answer = '第1空：%s；第2空：%s；第3空：%s；第四空%s' % (question[1].replace(r'\\','</br>'),question[2].replace(r'\\','</br>'),question[3].replace(r'\\','</br>'),question[4].replace(r'\\','</br>'))
        elif question[3] != '':
            answer = '第1空：%s；第2空：%s；第3空：%s' % (question[1].replace(r'\\','</br>'),question[2].replace(r'\\','</br>'),question[3].replace(r'\\','</br>'))
        elif question[2] != '':
            answer = '第1空：%s；第2空：%s' % (question[1].replace(r'\\','</br>'),question[2].replace(r'\\','</br>'))
        else:
            answer = '第1空：%s' % (question[1].replace(r'\\','</br>'))
        questionstring = ('<p>' + format_number + question[0].replace(r'\\','</br>').replace(r'\blank','<span style="text-decoration:underline">&emsp;&emsp;&emsp;&emsp;</span>') 
                                    + '</p><p>答案： ' + answer
                                    + '</p><p>解析： ' + question[5].replace(r'\\','</br>'))
    if question_type == '计算题':
        questionstring = ('<p>' + format_number + question[0].replace(r'\\','</br>')
                                    + '</p><p>解： ' + question[1].replace(r'\\','</br>'))
    if question_type == '证明题':
        questionstring = ('<p>' + format_number + question[0].replace(r'\\','</br>')
                                    + '</p><p>解： ' + question[1].replace(r'\\','</br>'))
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