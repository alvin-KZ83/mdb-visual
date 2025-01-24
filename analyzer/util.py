dict_id = ['or','ir','pk','pc','n','b','s']

joy = {
    'or' : [],
    'ir' : [],
    'pk' : [],
    'pc' : [],
    'n' : [],
    'b' : [],
    's' : [],
}
sad = {
    'or' : [],
    'ir' : [],
    'pk' : [],
    'pc' : [],
    'n' : [],
    'b' : [],
    's' : [],
}
anger = {
    'or' : [],
    'ir' : [],
    'pk' : [],
    'pc' : [],
    'n' : [],
    'b' : [],
    's' : [],
}
fear = {
    'or' : [],
    'ir' : [],
    'pk' : [],
    'pc' : [],
    'n' : [],
    'b' : [],
    's' : [],
}
dsgst = {
    'or' : [],
    'ir' : [],
    'pk' : [],
    'pc' : [],
    'n' : [],
    'b' : [],
    's' : [],
}

L = [joy, sad, anger, fear, dsgst]

def read_data():
    with open('./analyzer/mdb.csv') as mdb_data:
        raw = mdb_data.readlines()
        raw.pop(0)
        for line in raw:
            datas = line.split(',')
            datas.pop(0)
            for i in range(len(L)):
                # L[i] current emotion
                data = datas[i].split('+')
                for j in range(len(data)):
                    entry = data[j] if (j < 2) else float(data[j])
                    L[i][dict_id[j]].append(entry)
    return L