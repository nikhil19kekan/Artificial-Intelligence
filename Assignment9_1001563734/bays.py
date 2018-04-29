import sys
from math import pow
def calculate(h,cherries,lemons):
	#Accessing variable values having their names in string
	p_h=globals()["p_"+h]
	p_cherry_h=globals()["p_cherry_"+h]
	p_lemon_h=globals()["p_lemon_"+h]
	return (pow(p_cherry_h,cherries)*pow(p_lemon_h,lemons)*p_h)

def function(sample):
	cherries=0
	lemons=0
	numerator=0
	denominator=0
	#calculating number of cherries and lemons from sample
	file.write("Observation Sequence Q:"+sample+"\n")
	file.write("length of Q:%d\n"%len(sample))
	if sample:
		for i in sample:
			if i=='C':
				cherries=cherries+1
			elif i=='L':
				lemons=lemons+1
	#calculate for h1
	numerator=calculate("h1",cherries,lemons)
	denominator=numerator+calculate("h2",cherries,lemons)+calculate("h3",cherries,lemons)+calculate("h4",cherries,lemons)+calculate("h5",cherries,lemons)
	file.write("p(h1|Q)=%.3f\n"%(numerator/denominator))
	var1=float(numerator)/float(denominator)
	#calculate for h2
	numerator=calculate("h2",cherries,lemons)
	denominator=numerator+calculate("h1",cherries,lemons)+calculate("h3",cherries,lemons)+calculate("h4",cherries,lemons)+calculate("h5",cherries,lemons)
	file.write("p(h2|Q)=%.3f\n"%(numerator/denominator))
	var2=float(numerator)/float(denominator)
	#calculate for h3
	numerator=calculate("h3",cherries,lemons)
	denominator=numerator+calculate("h2",cherries,lemons)+calculate("h1",cherries,lemons)+calculate("h4",cherries,lemons)+calculate("h5",cherries,lemons)
	file.write("p(h3|Q)=%.3f\n"%(numerator/denominator))
	var3=float(numerator)/float(denominator)
	#calculate for h4
	numerator=calculate("h4",cherries,lemons)
	denominator=numerator+calculate("h2",cherries,lemons)+calculate("h3",cherries,lemons)+calculate("h1",cherries,lemons)+calculate("h5",cherries,lemons)
	file.write("p(h4|Q)=%.3f\n"%(numerator/denominator))
	var4=float(numerator)/float(denominator)
	#calculate for h5
	numerator=calculate("h5",cherries,lemons)
	denominator=numerator+calculate("h2",cherries,lemons)+calculate("h3",cherries,lemons)+calculate("h4",cherries,lemons)+calculate("h1",cherries,lemons)
	file.write("p(h5|Q)=%.3f\n"%(numerator/denominator))
	var5=float(numerator)/float(denominator)
	temp1=var1*globals()['p_cherry_h1']+var2*globals()['p_cherry_h2']+var3*globals()['p_cherry_h3']+var4*globals()['p_cherry_h4']+var5*globals()['p_cherry_h5']
	temp2=var1*globals()['p_lemon_h1']+var2*globals()['p_lemon_h2']+var3*globals()['p_lemon_h3']+var4*globals()['p_lemon_h4']+var5*globals()['p_lemon_h5']
	file.write("Probability that the next candy we pick will be C, given Q: %.3f\n"%temp1)
	file.write("Probability that the next candy we pick will be L, given Q: %.3f\n"%temp2)
def main():
	temp=""
	if(sys.argv[1]):
		sample=str(sys.argv[1])
	else:
		sample=""
	function(temp)
	for i in sample:
		temp=temp+i
		function(temp)
	file.close()
if __name__=="__main__":
	#probabilities given of each bag along with  % of cherries of lemons in it.	
	p_h1=0.1
	p_h2=0.2
	p_h3=0.4
	p_h4=0.2
	p_h5=0.1

	p_cherry_h1=1.0
	p_cherry_h2=0.75
	p_cherry_h3=0.5
	p_cherry_h4=0.25
	p_cherry_h5=0.0
	p_lemon_h1=0.0
	p_lemon_h2=0.25
	p_lemon_h3=0.5
	p_lemon_h4=0.75
	p_lemon_h5=1.0

	file=open("./result.txt","w")
	main()
