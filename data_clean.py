import csv
import os
import re

if __name__ == '__main__':
    sname = os.listdir('jijin')
    dict = {}
    dict['name']=[]
    for i in range(500):
        dict['X'+str(i+1)]=[]

    for f in sname:
        csv_reader = csv.reader(open('jijin/'+f))
        xt = re.findall(r'[^()]+', f)[1]
        name = 'X' + str(xt)
        if name == 'X001401':
            continue
        ls = []
        isPer = False
        for row in csv_reader:
            try:
                ft = row[1]
                if re.match(r'.*%$', ft):
                    print(ft)
                    isPer = True
                    continue
            except Exception as e:
                pass
            ls.append(row[1])
        if len(ls) < 500 | isPer:
            continue
        ls = ls[-500:]
        dict['name'].append(name)
        for i in range(500):
            dict['X'+str(i+1)].append(ls[i])
    with open('jijin/big_data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dict['name'])
        for i in range(500):
            writer.writerow(dict['X'+str(i+1)])
