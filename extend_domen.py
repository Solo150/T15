import os, sys, re

p_name = input("Введите название проекта: ")
d_name2 = input("Введите название домена: ")
d_name = '    \'' + d_name2 + '\','

SETTINGS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}/settings'
NGINX_PATH = '/etc/nginx/sites-enabled'
BASE_PATH = os.getcwd()
TEMP1 = 'ALLOWED_HOSTS = [\'*\']'
TEMP2 = 'ALLOWED_HOSTS = ['
TEMP3 = 'ALLOWED_HOSTS = [\'localhost\']'

start_dev = []
start_prod = []
results = []
start_path = []

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
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + d_name\
              + '\n]\n' + ''.join(finish_dev))
    elif allow_host_dev.strip() == TEMP2:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + d_name + '\n'\
              + ''.join(finish_dev))

# Запись измененного PROD.PY

with open(SETTINGS_PATH + '/prod.py', 'w') as prod:
    if allow_host_prod.strip() == TEMP3:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + d_name\
              + '\n]\n' + ''.join(finish_prod))
    elif allow_host_prod.strip() == TEMP2:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + d_name\
              + '\n' + ''.join(finish_prod))


os.system('systemctl stop nginx.service')

with open(NGINX_PATH + r'/default', 'r') as conf_file:
    finish_row = conf_file.readline()
    while finish_row != '# block_base_conf_finish\n':
        start_path.append(finish_row)
        finish_row = conf_file.readline()
    finish_path = conf_file.readlines()

with open(BASE_PATH + r'/templates/template.txt', 'r') as nginx_temp:
    nginx_temp = nginx_temp.read()
    result = re.sub(r'project_name', p_name, nginx_temp)
    result2 = re.sub(r'name_host', d_name2, result)

with open(NGINX_PATH + r'/default', 'w') as conf_file:
    conf_file.write(''.join(start_path) + result2\
                     + '\n' + finish_row + ''.join(finish_path))

os.system('systemctl start nginx.service')
