import os, re

p_name = input("Введите название проекта: ")
d_name2 = input("Введите название домена: ")

SETTINGS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}/settings'
NGINX_PATH = '/etc/nginx/sites-enabled'
BASE_PATH = os.getcwd()
TEMP1 = 'ALLOWED_HOSTS = [\'*\']'
TEMP2 = 'ALLOWED_HOSTS = ['
TEMP3 = 'ALLOWED_HOSTS = [\'localhost\']'
text = f"# Впишите ниже необходимые домены для установки в {p_name}-проект"

start_dev = []
start_prod = []
dev_result = []
prod_result = []
start_path = []
results = []

os.system('touch ' + BASE_PATH + f'/domens/{p_name}_domens_app.txt')

with open(BASE_PATH + f'/domens/{p_name}_domens_app.txt', 'w') as dom:
    dom.write(text)

os.system('nano ' + BASE_PATH + f'/domens/{p_name}_domens_app.txt')

with open(BASE_PATH + f'/domens/{p_name}_domens_app.txt', 'r') as domens:
	domens = domens.readlines()

with open(BASE_PATH + f'/domens/{p_name}_domens_app.txt', 'w') as domens_w:
	domens_w.writelines(domens[1:])

with open(BASE_PATH + f'/domens/{p_name}_domens_app.txt', 'r') as domens_txt:
    domens = domens_txt.readlines()

# СОСТАВЛЕНИЕ ЧАСТЕЙ dev.py + домены

with open(SETTINGS_PATH + '/dev.py', 'r') as dev:
    allow_host_dev = dev.readline()
    while 'ALLOWED_HOSTS' not in allow_host_dev:
        start_dev.append(allow_host_dev)
        allow_host_dev = dev.readline()
    finish__dev = dev.readlines()
    for domen in domens:
        domen = domen.strip()
        dev_result.append('    \'' + domen + '\',')

# СОСТАВЛЕНИЕ ЧАСТЕЙ prod.py + домены

with open(SETTINGS_PATH + '/prod.py', 'r') as prod:
    allow_host_prod = prod.readline()
    while 'ALLOWED_HOSTS' not in allow_host_prod:
        start_prod.append(allow_host_prod)
        allow_host_prod = prod.readline()
    finish_prod = prod.readlines()
    for domen in domens:
        domen = domen.strip()
        prod_result.append('    \'' + domen + '\',')

# Запись измененного DEV.PY

with open(SETTINGS_PATH + '/dev.py', 'w') as dev:
    if allow_host_dev.strip() == TEMP1:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + '\n'.join(dev_result)\
              + '\n]\n' + ''.join(finish__dev))
    elif allow_host_dev.strip() == TEMP2:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + '\n'.join(dev_result)\
              + '\n' + ''.join(finish__dev))

# Запись измененного PROD.PY

with open(SETTINGS_PATH + '/prod.py', 'w') as prod:
    if allow_host_prod.strip() == TEMP3:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n'.join(prod_result)\
              + '\n]\n' + ''.join(finish_prod))
    elif allow_host_prod.strip() == TEMP2:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n'.join(prod_result)\
              + '\n' + ''.join(finish_prod))

os.system('systemctl stop nginx.service')

with open(NGINX_PATH + r'/default', 'r') as conf_file:
    domens = domens.readlines()
    finish_row = conf_file.readline()
    while finish_row != '# block_base_conf_finish\n':
        start_path.append(finish_row)
        finish_row = conf_file.readline()
    finish_path = conf_file.readlines()

    with open(BASE_PATH + r'/templates/template.txt', 'r') as nginx_temp:
        nginx_temp = nginx_temp.read()
        for domen in domens:
            domen = domen.strip()
            result = re.sub(r'project_name', p_name, nginx_temp)
            result2 = re.sub(r'name_host', domen, result)
            results.append(result2 + '\n')

with open(NGINX_PATH + r'/default', 'w') as conf_file:
    conf_file.write(''.join(start_path) + ''.join(results)\
                     + '\n' + finish_row + ''.join(finish_path))


os.system('systemctl start nginx.service')


