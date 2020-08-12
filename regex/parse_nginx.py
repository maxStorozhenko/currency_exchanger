import re
import csv

PATH = './nginx.log'

regex = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\[(?P<date>.*)\].*  \"(?P<method>.*)\ /' \
                   '(?P<path>.*) HTTP.*\d{3} \d{1,4}')


with open(PATH) as file:
    with open('nginx_logs.csv', 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',')
        for index, line in enumerate(file):
            res = regex.search(line)
            if res is not None:
                res = res.groupdict()

                ip = res['ip']
                date = res['date']
                method = res['method']
                path = '/' + res['path']
                data_writer.writerow([ip, date, method, path])
