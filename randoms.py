import random
import csv

file1 = open("1lines.csv", "r", encoding="utf8")
one_lines = list(csv.reader(file1, delimiter="$"))
file1.close()

file2= open("4liases.csv", "r", encoding= "utf8")
aliases= list(csv.reader(file2, delimiter= "$"))
file2.close()

def one_line():
	result1= random.choice(one_lines)
	return "".join(result1)

def aliase():
	result2= random.choice(aliases)
	return "".join(result2)