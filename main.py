import numpy as np
import pandas as pd

df = pd.read_csv("GEODATASOURCE-COUNTRY-BORDERS.CSV")
num_countries = len(df["country_name"].unique())

last_id = 0
id_to_country = {}
name_to_id = {}
name_to_code = {}
code_to_name = {}
for name in df["country_name"].unique():
    this_id = last_id
    last_id += 1
    
    id_to_country[this_id] = {"name": name, "code": df[df["country_name"] == name]["country_code"].unique()[0]}
    name_to_id[name] = this_id
    name_to_code[name] = id_to_country[this_id]["code"]
    code_to_name[id_to_country[this_id]["code"]] = name
    
    if name == "Namibia":
        id_to_country[this_id]["code"] = "NA"

adj_matrix = np.zeros([num_countries, num_countries])

for idx in df.index:
    ts_country = df.loc[idx, "country_name"]
    ts_border = df.loc[idx, "country_border_name"]
    if type(ts_border) != type("string"):
        continue
    
    adj_matrix[name_to_id[ts_country]][name_to_id[ts_border]] = 1

evals, evecs = np.linalg.eigh(adj_matrix)
def adj_power(evals, evecs, k):
    return np.abs(evecs @ np.diag(evals ** k) @ evecs.T).round()

def find_longest_possible_path(evals, evecs):
    last_mat = adj_power(evals, evecs, 0)
    last_pow = 0
    last_zero = (last_mat == 0).sum()
    while True:
        this_pow = last_pow + 1
        this_mat = adj_power(evals, evecs, this_pow)
        this_zero = (this_mat == 0).sum()
        if last_zero == this_zero:
            return last_pow
        
        last_mat = this_mat
        last_pow = this_pow
        last_zero = this_zero
        
max_search = find_longest_possible_path(evals, evecs)

def find_shortest_path(id1, id2, evals=evals, evecs=evecs, max_search=max_search):
    for k in range(max_search):
        if adj_power(evals, evecs, k)[id1][id2] > 0:
            return k
    return -1
        

import numpy as np
import pandas as pd

df = pd.read_csv("GEODATASOURCE-COUNTRY-BORDERS.CSV")
num_countries = len(df["country_name"].unique())

last_id = 0
id_to_country = {}
name_to_id = {}
name_to_code = {}
code_to_name = {}
for name in df["country_name"].unique():
    this_id = last_id
    last_id += 1
    
    id_to_country[this_id] = {"name": name, "code": df[df["country_name"] == name]["country_code"].unique()[0]}
    name_to_id[name] = this_id
    name_to_code[name] = id_to_country[this_id]["code"]
    code_to_name[id_to_country[this_id]["code"]] = name
    
    if name == "Namibia":
        id_to_country[this_id]["code"] = "NA"

adj_matrix = np.zeros([num_countries, num_countries])

for idx in df.index:
    ts_country = df.loc[idx, "country_name"]
    ts_border = df.loc[idx, "country_border_name"]
    if type(ts_border) != type("string"):
        continue
    
    adj_matrix[name_to_id[ts_country]][name_to_id[ts_border]] = 1

evals, evecs = np.linalg.eigh(adj_matrix)
def adj_power(evals, evecs, k):
    return np.abs(evecs @ np.diag(evals ** k) @ evecs.T).round()

def find_longest_possible_path(evals, evecs):
    last_mat = adj_power(evals, evecs, 0)
    last_pow = 0
    last_zero = (last_mat == 0).sum()
    while True:
        this_pow = last_pow + 1
        this_mat = adj_power(evals, evecs, this_pow)
        this_zero = (this_mat == 0).sum()
        if last_zero == this_zero:
            return last_pow
        
        last_mat = this_mat
        last_pow = this_pow
        last_zero = this_zero
        
max_search = find_longest_possible_path(evals, evecs)

def find_shortest_path(id1, id2, evals=evals, evecs=evecs, max_search=max_search):
    for k in range(max_search):
        if adj_power(evals, evecs, k)[id1][id2] > 0:
            return k
    return -1
        

country1 = name_to_id[input("First Country : ")]
country2 = name_to_id[input("Second Country : ")] 

print(find_shortest_path(country1, country2) - 1) # subtract 1 bc don't count start and end
