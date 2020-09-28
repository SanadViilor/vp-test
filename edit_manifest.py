import json



def json2dict(filename):
   with open(filename, 'r') as inputf:
       fuck = inputf.readlines()
      
       json_array = []
   for item in fuck:
       entry = json.loads(item)
       json_array.append(entry)
   return json_array
        

def dictarr2json(dictarray, filename):
    with open(filename, 'w', encoding='utf8') as fout:
        for i in dictarray:
            i['text'] = i['text'].replace('\n', '').replace('?', '').replace('!', '').replace('\"', '').replace(',', '').replace(':', '').replace('\'', '').replace(';', '').replace('-', '').replace('„', '').replace('”', '').replace('»', '').replace('«', '').replace('…', '').replace('“', '').replace('‹', '').replace('›', '').replace('’', '').replace('–', '').replace('´', '')#.replace('ʻ', '')
            json.dump(i, fout, ensure_ascii=False)
            fout.write('\n')

def is_it_good(string, alphabet):
    for char in string:
        if char not in alphabet:
            return False
    return True




if __name__ == '__main__':
    idictarr = json2dict('train_man.json')
    alphabet='aáäbcdeéfghijklmnoöpqrsßtuüvwxyz '

    idictarr = [i for i in idictarr if is_it_good(i['text'], alphabet) == True]
#    k = 1
#    noil = 0 
#    for i in idictarr:
#        ac = 0
#        for j in i['text']:
#            if j not in alphabet:
#                print('Found a(n) ' + j + ' in line ' + str(k))
#                if ac == 0:
#                    noil = noil + 1
#                    ac = 1
#        k = k + 1
#    print('Number of irregular lines: ' + str(noil))

    dictarr2json(idictarr, 'train_man_r.json')
   
        
        
    





