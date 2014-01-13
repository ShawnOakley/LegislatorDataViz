# -*- coding: utf-8 -*- 
import json
import pandas as pd
import re
import unicodedata
import numpy as np
import scipy.sparse as sparse

with open('pop_wealth_2010.json', 'r') as f:
     read_data = f.read()
     f.closed
# print read_data

pop_wealth_df = pd.read_json(read_data)
pop_wealth_df.columns = ['State', 'Per Capita Net Wealth']
pop_wealth = json.loads(read_data)

print pop_wealth_df['State']

with open('crp_data_2010.json', 'r') as f:
     read_data = f.read()
     f.closed

leg_wealth = json.loads(read_data)['records']
# leg_wealth_df = pd.read_json(leg_wealth)
# leg_wealth_df.columns = ['State', 'Legislator Net Wealth']
# print leg_wealth


# # print leg_wealth_df
# print pop_wealth_df

regex = re.compile("\([R|D]-(.+)\)")

names = []

for entry in leg_wealth:
	names.append(entry['Name'])

abbrs = []

for name in names:
	hit = regex.search(name)
	if hit is not None:
		abbrs.append(hit.group(0)[3:-1])

states = pop_wealth_df['State']
state_strings = map(str, states.values)
state_strings.sort()

abbrs = list(set(abbrs))
abbrs = map(str, abbrs)
abbrs.sort()
abbrs.remove('DC')
abbrs.remove('AS')
state_strings.remove('District of Columbia')
abbrs.remove('Guam')

# Cleans up data for dict, maps abbreviation for creation in dict

a, b = abbrs.index('Mass'), abbrs.index('Md')
abbrs[b], abbrs[a] = abbrs[a], abbrs[b]

a, b = abbrs.index('NC'), abbrs.index('Neb')
abbrs[b], abbrs[a] = abbrs[a], abbrs[b]

a, b = abbrs.index('Nev'), abbrs.index('ND')
abbrs[b], abbrs[a] = abbrs[a], abbrs[b]

a = abbrs.index('Wis')
abbrs[a] = 'Wyo'

a = abbrs.index('Wash')
abbrs[a] = 'Wis'

a = abbrs.index('Vt')
abbrs[a] = 'Wash'

a = abbrs.index('VI')
abbrs[a] = 'Vt'

leg_state_dict = dict(zip(abbrs, state_strings))
# print leg_state_dict
# print len(leg_state_dict)

# print leg_wealth

# for entry in pop_wealth:
# 	entry['Leg_Wealth'] = []

leg_wealth_hash = {state:0 for state in state_strings}
leg_number_hash = {state:0 for state in state_strings}

print leg_wealth_hash
print leg_number_hash

pop_wealth_df['Leg_Wealth'] = [0 for i in xrange(len(pop_wealth_df))]
pop_wealth_df['Leg_Number'] = [0 for i in xrange(len(pop_wealth_df))]

for entry in leg_wealth:
	hit = regex.search(entry['Name'])
	if hit is not None:
		if hit.group(0)[3:-1] == 'Guam' or  hit.group(0)[3:-1] == 'DC' or  hit.group(0)[3:-1] == 'VI'  or  hit.group(0)[3:-1] == 'AS':
			pass
		else:
			leg_wealth_hash[leg_state_dict[hit.group(0)[3:-1]]] += float(entry['AvgValue'])
			# leg_wealth_hash[leg_state_dict[hit.group(0)[3:-1]]] += float(entry['MaxValue'])
			leg_number_hash[leg_state_dict[hit.group(0)[3:-1]]] += 1

# print leg_wealth_hash
# print leg_number_hash

leg_average_hash = {state:0 for state in state_strings}

for state in state_strings:
	leg_average_hash[state] = leg_wealth_hash[state]/leg_number_hash[state]

# print leg_average_hash

comp_hash = {state:0 for state in state_strings}
print pop_wealth

for state in state_strings:
	for entry in pop_wealth:
		if str(entry['State']) == state:
			if entry["Wealth"] != 0:
				comp_hash[state] = leg_average_hash[state] / entry['Wealth']

with open('comp.json', 'w') as outfile:
	json.dump(comp_hash, outfile)