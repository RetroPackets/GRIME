from modules.deepsqlite import *
from modules.deephelpers import *

con = connectDB()
createFTStable(con)
populateFTS(con)

deepSearchTitle()
term = input("Enter Search: ")

results = searchFTS(term,con)
print("Found " + str(len(results)) + " Results.")

for i in results:
	string = ""
	for j in i:
		string += j
	print(string)
