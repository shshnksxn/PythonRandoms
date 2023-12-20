#!/usr/bin/python
#Script in python:

#Declare array
List=[1,2,3,4,5]

k=6   # number to match
j=0
for i in List:

	print i
	print j
	b= i + j
	print b
	if (k ==b):
		print "Success"
		print i, j
	else:
		print "failed"
		j=i
	i=i+1
	j=j-1

