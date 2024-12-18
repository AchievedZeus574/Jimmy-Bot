import random
import csv

file1 = open("1lines.tsv", "r", encoding="utf8")
one_lines = list(csv.reader(file1, delimiter="\n"))
file1.close()

file2= open("4liases.csv", "r", encoding= "utf8")
aliases= list(csv.reader(file2, delimiter= "$"))
file2.close()

foods= [":grapes:", ":watermelon:", ":banana:", ":apple:", ":cheese:", ":hamburger:",":fries:", ":pizza:", ":bacon:", ":pretzel:", ":beans:", ":sandwich:", ":taco:", ":salt:", ":doughnut:", ":lobster:", ":shrimp:"]

def one_line():
	result1= random.choice(one_lines)
	return "".join(result1)

def aliase():
	result2= random.choice(aliases)
	return "".join(result2)

def hunger(numb: int= 1):
	result3= ""
	for i in range(numb):
		result3= result3+ foods[random.randint(0, len(foods)-1)]+ " "
	return result3

def thirst(num: int= 1):
	result4= ""
	for i in range(num):
		result4= result4+ ":droplet: "
	return result4