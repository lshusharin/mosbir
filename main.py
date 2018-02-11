# coding=utf-8
import os
import json
import sys

if __name__=="__main__":
    # print os.path.join(os.path.abspath(), '..', "d")
    dir_list = os.listdir(unicode(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', "d"))))

    root = unicode(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', "d")))
    parsed = {}
    print len(dir_list)
    parsed = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        8: {},
    }
    i=1
    j= 0
    for file in dir_list:
        if j>44:
            j= 0
            i+=1
        name= file
        j+=1
        # print name

        # print unicode(os.path.abspath(os.path.join(root, file)))

        with open(unicode(os.path.abspath(os.path.join(root, file)))) as file:
            array = [row.strip() for row in file]
        array = array[1:]

        parsed[i][name[:-4]] = {}
        prev_day_in_entry= '20170100'
        for entry in array:
            line = entry.split(";")

            if int(prev_day_in_entry) < int(line[2]):
                parsed[i][name[:-4]][line[2]] = {}

            prev_day_in_entry = line[2]
            parsed[i][name[:-4]][line[2]][line[3]] = line[4:]

            # append(entry.split(";")[1:])
        print len(parsed[1])
        print len(parsed[2])
        print len(parsed[3])
        print len(parsed[4])
    with open('res1.json', 'w') as f:
        f.write(json.dumps(parsed[1], sort_keys= True))
    with open('res2.json', 'w') as f:
        f.write(json.dumps(parsed[2], sort_keys= True))
    with open('res3.json', 'w') as f:
        f.write(json.dumps(parsed[3], sort_keys= True))
    with open('res4.json', 'w') as f:
        f.write(json.dumps(parsed[4], sort_keys= True))
    with open('res5.json', 'w') as f:
        f.write(json.dumps(parsed[5], sort_keys= True))
    with open('res6.json', 'w') as f:
        f.write(json.dumps(parsed[6], sort_keys= True))
    with open('res7.json', 'w') as f:
        f.write(json.dumps(parsed[7], sort_keys= True))
    with open('res8.json', 'w') as f:
        f.write(json.dumps(parsed[8], sort_keys= True))