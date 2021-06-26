# -*- coding: utf-8 -*-
"""
Created on Tue July 10 19:49:45 2019

@author: Ramisa

basic fp-tree courtesy: https://github.com/DIYer22/dataMining/blob/master/FP_tree.py

"""

from __future__ import unicode_literals
import time
import random
from decimal import *

start_time = time.time()


def log(d):
    show_len = 40
    if isinstance(d,list):
        for i in d:
            strr = str(i)
            if len(strr) > show_len:
                print strr[:show_len] + '...'
            else:
                print strr
        return
            
    if isinstance(d,dict):
        for i in d:
            strr = str(i)+' = '+str(d[i])
            if len(strr) > show_len:
                print strr[:show_len] + '...'
            else:
                print strr          
        return
    print d


def read_weight(fileName):
        weight_dict = {}
        maxW = -1
        f = open(fileName, "r")
        if f.mode == "r":
                contents = f.readlines()
                for line in contents:
                        tokens = line.split()
                        w = Decimal(tokens[2])
                        w = w+25
                        w = w/10
                        if maxW < w:
                            maxW = w
                        weight_dict.update({int(tokens[0]): w})
                #print(weight_dict)
                print("MaxW is {}".format(maxW))
                return weight_dict, maxW

MAX_L = 22
def p_tree(t,level = 0):
    if level > MAX_L:
        return
    for i in t:
        if  not isinstance(i,int):
            continue
        print level*'| '+'%d :%d'%(i, t[i]['c'])
        p_tree(t[i],level+1)
        

min_sup = 0.01 * 16 * 2
min_conf = 0.5






"""
File preparation start
"""
path = './T10I4D100K.dat'
f = open(path, 'r')
db = f.readlines()
f.close()
#print(db)
dbw = []
for x in db:
    wx = []
    length = len(x)
    x = x.split()
    for itm in x:
        if itm != ' ' and itm!='\n':
            ito = random.randint(2,30)
            itm_ito_tuple = (itm,ito)
            wx.append(itm_ito_tuple)
    dbw.append(wx)


outputfile = "ito_T10I4D100K.dat"
obj = open(outputfile, "w")
for xw in dbw:
    xwstr = ""
    for itm_ito_tuple in xw:
        itm, ito = itm_ito_tuple
        xwstr = xwstr + " " + str(itm)+":"+str(ito)+" "
    obj.write("{}\n".format(xwstr))
obj.close()
"""
File preparation END
"""

"""
File Read start
"""
fileName = "ito_retail.dat"
f = open(fileName, "r")
contents = f.readlines()
dbw = []
db = []
intrafreq_dict = {}
freq_dict = {}
for line in contents:
    #print(line)
    xw =[]
    x = []
    tokens = line.split()
    #print(line)
    #print(tokens)
    for token in tokens:
        #print(token)
        ttk = token.split(':')
        #print(ttk)
        itm_ito_tuple = (int(ttk[0]), int(ttk[1]))
        xw.append(itm_ito_tuple)
        x.append(int(ttk[0]))
        intrf = int(ttk[1])
        item = int(ttk[0])
        if item not in intrafreq_dict:
                   intrafreq_dict[item] =  intrf
                   freq_dict[item] = 1
        else:
                   intrafreq_dict[item] +=  intrf
                   freq_dict[item] += 1

        #print(int(ttk[0]))
        #print("{}:{}".format(ttk[0], int(ttk[0])))
    dbw.append(xw)
    #print(x)
    db.append(x)



for k,v in freq_dict.iteritems():
             intrafreq_dict[k] =  intrafreq_dict[k]/v     

##for xw in dbw:
##    print(xw)


"""
File Read end
"""


"""
Read weight from external weight file
"""
wfileName = 'weight_retail2.dat'
weight_dict, maxW = read_weight(wfileName)

#min_sup = 0.5
#db = [
#[1,3,4],
#[2,3,5],
#[1,2,3,5],
#[2,5]]
#print(weight_dict)


##for k,v in weight_dict.iteritems():
##    print("{},{}".format(k,v))

min_sup *= len(db)

dic = {}  
dicc = {}  
min_f = []  
a_r = []  
for items in db:
   for item in items:
       #print(item)
       dic[item] = 1 if item not in dic else dic[item] + 1


[dic.pop(k) if not dic[k]*intrafreq_dict[k]*weight_dict[k]>= min_sup else None for k in dic.keys()]




root = {}
record = {}
def add_tree(its, tree, count, record, dic):
    its = filter(lambda x: x in dic, its)
    its.sort(lambda x, y:  1 if dic[x] < dic[y] else -1 )
    for it in its:
        if it not in tree:
            tree[it] = {}
            tree[it]['f'] = tree
            tree[it]['s'] = it
            record[it]=[tree[it]] if it not in record else record[it]+[tree[it]]
        tree = tree[it]
        tree['c'] = count if 'c' not in tree else tree['c'] + count

    


for items in db:
    add_tree(items, root, 1, record, dic)


#print 'dic',
#log(dic)

print '\nrecord',log('')

#p_tree(root)

fp_l = dic.items()
fp_l.sort(lambda x, y: 1 if x[1]<y[1] else -1)


def creat_its(t):
    l=[]
    while 1:
        t = t['f']
        if 'f' not in t:
            break
        l += [t['s']]
        
    return l[::-1]

dicc ={}

def is_singl_tree(t):
    def c_n(n, listt, l, b, r):  
        if n == 0: 
            r.append(tuple(l))
            return
        for i in range(b, len(listt)-n+1):
            l += [listt[i]]
            c_n(n-1, listt, l, i+1,r)
            l.pop()
        return 
    
    def combination(its): 
        n = len(its)
        l = []
        if n == 1:
            return [its]
        for lenth in range(1, n+1):
            c_n(lenth, its, [],0,l)
        print 'its',its,l
        return l

        
    l = []
    root = t
    while 1:
        tmp = filter(lambda x:isinstance(x, int), t.keys())
        n = len(tmp)
        if n != 1 and n != 0:
#            print l,p_tree(root)
            return None
        if n == 0 :
            
            if 'f' in t:
#                print 'tmp',l
#                print tmp,root.keys(),l,combination(l)
                return [list(i) for i in combination(l)]
            return None
        l += tmp
        
        t=t[tmp[0]]
        
        
    
    
    
def header_to_db(fp_list, record, intrafreq_dict, weight_dict):
    l = []
#    print 'fp',fp_list
    for it in fp_list[::-1]:
        it = it[0]
        db = []
        for t in record[it]:
            db += [(creat_its(t), t['c'])]
#        print 'db',db
        dic = {}
        for items in db:
           for item in items[0]:
               dic[item] = items[1] if item not in dic else dic[item] + items[1]
        [dic.pop(k) if not dic[k]*weight_dict[k]*intrafreq_dict[k]>= min_sup else None for k in dic.keys()]

        t = {'s':'root'}
        header = {}
        for its in db:
            add_tree(its[0], t, its[1], header, dic)
        r = is_singl_tree(t)
#        print 'it',it,r,dic
        if r != None:  
#            print 'r',r
            l += [i+[it] for i in r]+[[it]]
#            print 'add',[i+[it] for i in r]
            continue
        
        fp_l = dic.items()
        fp_l.sort(lambda x, y: 1 if x[1]<y[1] else -1)

        r = header_to_db(fp_l, header, intrafreq_dict, weight_dict)
        l += [i+[it] for i in r]+[[it]]
    return l



#for it in fp_l[::-1]:
#    f(it[0])
#print(record)
r = header_to_db(fp_l, record, intrafreq_dict, weight_dict)

#print 'resoult',r
end_time = time.time()
timespan = (end_time - start_time)
print("Required time:{} seconds".format(timespan))
print 'frequent itemset', len(r)
#print(r)
 
