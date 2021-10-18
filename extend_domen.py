import os

p_name = input("Введите название проекта: ")
d_name = '    \'' + input("Введите название домена: ") + '\','

SETTINGS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}/settings'
BASE_PATH = os.getcwd()
TEMP1 = 'ALLOWED_HOSTS = [\'*\']'
TEMP2 = 'ALLOWED_HOSTS = ['
TEMP3 = 'ALLOWED_HOSTS = [\'localhost\']'

start_dev = []
start_prod = []

# СОСТАВЛЕНИЕ ЧАСТЕЙ dev.py + домены

with open(SETTINGS_PATH + '/dev.py', 'r') as dev:
    allow_host_dev = dev.readline()
    while 'ALLOWED_HOSTS' not in allow_host_dev:
        start_dev.append(allow_host_dev)
        allow_host_dev = dev.readline()
    finish_dev = dev.readlines()

# СОСТАВЛЕНИЕ ЧАСТЕЙ prod.py + домены

with open(SETTINGS_PATH + '/prod.py', 'r') as prod:
    allow_host_prod = prod.readline()
    while 'ALLOWED_HOSTS' not in allow_host_prod:
        start_prod.append(allow_host_prod)
        allow_host_prod = prod.readline()
    finish_prod = prod.readlines()

# Запись измененного DEV.PY

with open(SETTINGS_PATH + '/dev.py', 'w') as dev:
    if allow_host_dev.strip() == TEMP1:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + '\n' + d_name\
              + '\n]\n' + ''.join(finish_dev))
    elif allow_host_dev.strip() == TEMP2:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + d_name + '\n'\
              + ''.join(finish_dev))

# Запись измененного PROD.PY

with open(SETTINGS_PATH + '/prod.py', 'w') as prod:
    if allow_host_prod.strip() == TEMP3:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n' + d_name\
              + '\n]\n' + ''.join(finish_prod))
    elif allow_host_prod.strip() == TEMP2:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n' + d_name\
              + '\n' + ''.join(finish_prod))
