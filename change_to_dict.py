with open('1.txt',encoding='utf-8')as f:
    with open('need.txt', 'a')as f1:
        for i in f.readlines():
            needed=i.split(':',1)
            f1.write('"{}":"{}"'.format(needed[0],needed[1].strip())+','+'\n')
