import json
import pandas as pd
import re
import unicodedata

with open('pop_wealth_2010.json', 'r') as f:
     read_data = f.read()
     f.closed
# print read_data

pop_wealth_df = pd.read_json(read_data)
pop_wealth_df.columns = ['State', 'Per Capita Net Wealth']
pop_wealth = json.loads(read_data)

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

print regex

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
abbrs[a] = 'Wy'

a = abbrs.index('Wash')
abbrs[a] = 'Wis'

a = abbrs.index('Vt')
abbrs[a] = 'Wash'

a = abbrs.index('VI')
abbrs[a] = 'Vt'

leg_state_dict = dict(zip(abbrs, state_strings))
print leg_state_dict
print len(leg_state_dict)




