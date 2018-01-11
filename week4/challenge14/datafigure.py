import json
import pandas as pd
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
	data = pd.read_json("user_study.json")
	userData = data[['user_id','minutes']].groupby('user_id').sum()
	

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	ax.set_title("StudyData")
	ax.set_xlabel("User ID")
	ax.set_ylabel("Study Time")

	ax.plot(userData['minutes'])

	fig.show()

