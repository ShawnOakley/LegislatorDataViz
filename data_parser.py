import json
import pandas as pd
import re

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

abbrs = list(set(abbrs))
print abbrs

leg_state_hash = {}
states = pop_wealth_df['State']

for state in states:
	if leg_state_hash.get(state) is None:
		leg_state_hash[state] = []
		

print len(leg_state_hash)


