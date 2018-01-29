#!/usr/bin/python
import sys

#this function reads those line from file where theres a path from sourceCity
def readFileLine(sourceCity):
	f=open("C:\Users\Nikhil\PycharmProjects\AI1\AI-ass1\input1.txt","r")
	list=[]
	for line in f:
		if (sourceCity in line):
			parts=line.split()
			if(parts[0]==sourceCity):
				list.append(line)
			else:
				list.append(parts[1]+" "+parts[0]+" "+parts[2])
		else:
			continue
	f.close()
	return list

#this function is just to help sorting the fringe
def getDistance(line):
	return int(line.split()[-1])

#this function is to add paths from specified city into the fringe
def addInFringe(source,cumuD):
	for l in readFileLine(source):
		cumu=int(cumuD)+int(l.split()[2])
		fringe.append(l.split()[0]+" "+ l.split()[1]+" "+ l.split()[2]+" "+ str(cumu))
	return fringe

def backTrack(fringe):	
	backList=[]
	source=fringe[-1].split()[0]
	dest=fringe[-1].split()[1]
	cost=int(fringe[-1].split()[2])
	cumuCost=int(fringe[-1].split()[3])
	backList.append(source+" to "+dest+", "+str(cost)+" km\n")
	for l in sorted(fringe,key=getDistance,reverse=True):
		if(int(l.split()[-1])==(cumuCost-cost) and l.split()[1]==source):
			source=l.split()[0]
			dest=l.split()[1]
			cost=int(l.split()[2])
			cumuCost=int(l.split()[-1])
			backList.append(source+" to "+dest+", "+str(cost)+" km\n")
		else:
			continue
	return backList[:len(backList)-1]
	
#This function includes actual algorithmic steps		
def algorithm(sourceCity,goal,fringe,closedSet,index):
	while(index<len(fringe)):		
		node=fringe[index]
		index=index+1
		source=node.split()[0]
		destination=node.split()[1]
		if(destination==goal):
			print("distance:"+node.split()[-1]+" km\n")
			break
		if (destination!=goal and destination not in closedSet):
			addInFringe(destination,node.split()[-1])
			closedSet.append(destination)
			fringe[index:]=sorted(fringe[index:],key=getDistance)
	else:
		print("distance: infinity\nroute:none\n")
		return ""
	return backTrack(fringe[:index])
#main
source=sys.argv[1]
goal=sys.argv[2]
closedSet=[]
index=0
optimalPathLength=0
optimalPath=[]
fringe=[source+" "+source+" "+str(0)+" "+str(0)]
for l in reversed(algorithm(source,goal,fringe,closedSet,index)):
	print(l)