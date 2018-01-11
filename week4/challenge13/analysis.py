import json
import pandas as pd

def analysis(file, user_id):
	times = 0
	minutes = 0
	data = pd.read_json(file)
	userData = data[data['user_id'] == user_id]
	if userData.empty:
		return 0
	times = len(userData)
	minutes = userData.sum()['minutes']
	return times,minutes