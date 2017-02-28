names = [ "Suhani Abdullah", "KENDRA ABELLANEDA", "Sunny Aggarwal", "JIMI AJAYI", 
"Yvette Ankunda", "Daksh Bhatia", "Sabrina Cherny", "Aditya Chopra", "Natalie Chow", 
"Jennifer Dai", "Akshat Das", "KARAN DHILLON", "Charles Ding", "ANTHONY DIPRINZIO", 
"Liam Ehrlich", "Jon Epstein", "Brennan Fahselt", "ARNAV Gautam", "Mudit Goyal",
"Tyler Heintz", "Adithya Iyengar", "Brian Jue", "Sung Kang", "Parisa Khorram",
"Daniela Kim", "Jennifer Kirby", "Ronen Ke", "Rishi Kolady", "Nikhil Krishnan",
"Anushri Kumar", "Katarina Lee", "FEDERICO LI", "Therese Liwanag", "Riley Shore Mangubat",
"Sergey Mann", "DARYUS MEDORA", "Brian Mickle", "Brian Nguyen", "Nelli Petikyan",
"Sanjay Raavi", "Rohit Rajkumar", "Alexander Rakeman", "Evan Sheng", "ROBERT SPRAGG",
"Chase Sturgill", "Iris Sun", "KESHAV THVAR", "Nicole Tsai", "Jessie Wang",
"William Wang", "Thomas Warloe", "Serena Wu", "Kenny Yoo", "Sunny Zhang", "Zhe Zhang" ]

counter = 2
print("{")
for name in names:
	for i in range(1, 4):
		print("\"" + name.lower() + " " + str(i) + "\" : " + str(counter) + ",")
		counter = counter + 1
print("}")
