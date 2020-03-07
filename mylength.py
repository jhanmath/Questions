# -*- coding: utf-8 -*-

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