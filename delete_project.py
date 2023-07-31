import sys, os

patterns = []
conf_default = '/etc/nginx/sites-enabled/default'
with open('domens/' + sys.argv[1] + '_domens.txt', 'r') as domens:
    domens = domens.readlines()
    for domen in domens:
        pattern1 =  sys.argv[1] + '1' + domen.strip() + '1'
        pattern2 =  sys.argv[1] + '2' + domen.strip() + '2'
        patterns.append([pattern1, pattern2])

for pattern in patterns:
    os.system(f'sed -i \"/{pattern[0]}/, /{pattern[1]}/d\" {conf_default}')
