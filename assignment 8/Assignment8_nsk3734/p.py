def main():
	file=open("./input.txt","r")
	lines=0
	r1_ones=0
	r2_ones=0
	r3_ones=0
	r4_ones=0
	for i in file:
		lines=lines+1
		i=i.replace(" ","")
		print i
		if(i[0]=='1'):
			r1_ones=r1_ones+1
		if(i[1]=='1'):
			r2_ones=r2_ones+1
		if(i[2]=='1'):
			r3_ones=r3_ones+1
		if(i[3]=='1'):
			r4_ones=r4_ones+1
	print "no of records:%d\n"%lines
	print "r1:%d\n"%r1_ones
	print "r2:%d\n"%r2_ones
	print "r3:%d\n"%r3_ones
	print "r4:%d\n"%r4_ones

if __name__=="__main__":
	main()
