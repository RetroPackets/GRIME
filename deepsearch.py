from modules.deepsqlite import *
from modules.deephelpers import *

con = connectDB()
createFTStable(con)
populateFTS(con)

deepSearchTitle()
term = input("Enter Search: ")

results = searchFTS(term,con)
print(f"Found {len(results)} Results.")

for i in results:
	string = "".join(i)
	print(string)
