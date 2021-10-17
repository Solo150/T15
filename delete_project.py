import sys

"""
    Сменить путь до файла в соответствии с ОС
"""

with open('domens\\' + sys.argv[1] + '_domens.txt', 'r') as domens:
    domens = domens.readlines()
    for domen in domens:
        print('# ' + sys.argv[1] + '1' + domen.strip() + '1')

with open(sys.argv[1] + '_domens.txt', 'r') as conf_file:
    pass