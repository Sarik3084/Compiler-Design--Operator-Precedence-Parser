#oplst = {'*','/','-','+','%','&','|',')','('}
precedence=dict()
assoc=dict()
rhsidentifiers=[]
production = dict()
usedopt=[]
line=0
	
def Isnonterminal(a):

	if(a>='A' and a<='Z'):
		return 1
	else:
		return 0
		
def Notnull(a):

	if(a!="^"):
		return 1
	else:
		return 0
			
def Isoperator(a):

	if  not (a.isalpha() or a.isdigit()) :
		return 1
	else:
		return 0
		
def Isunaryopt(a):
	
    if a=='!' or a=='~':
    	return 1
    else:
    	return 0
    				
def convert(exp):

	l=len(exp)
	exp1=list(exp)
	for i in range(l):
		if(exp1[i].isalpha() or exp1[i].isdigit()):
			exp1[i]='i'
	exp=''.join(exp1)
	return exp			


opl=[]
#Scanning opprec.txt file and fixing precedence and association of operators
fp1=open("opprec.txt","r")
while True:
	read = fp1.readline()
	read=read.strip()
	if(read==''):
		break	
	opl=read.split(' ')
	#print opl
	#print len(opl)
	
	if not(Isoperator(opl[0]) or opl[1].isdigit() or (opl[2]=='R' or opl[2]=='L')):
		print 'Error in precedence file'
	usedopt.append(opl[0])	
	precedence[opl[0]]=opl[1]
	assoc[opl[0]]=opl[2]	
	
usedopt.append('i')
usedopt.append('$')				
											
usedopt =list(set(usedopt))
#has completed operator list till this 



#checking grammar which is in f.txt file :: it should be operator grammar

fp = open("f.txt","r")

while True:

	read=fp.readline()

	if(read==''):
		break

	line+=1

	if '->' in read:

		a,b=read.split('->')
		a=a.strip()
		b=b.strip()

		#print 'a=',a,'\nb=',b,'\n'

		if(Isnonterminal(a)):

			if(Notnull(b)):    #RHS should not include null in production

				if(len(b)==1):

					if(Isnonterminal(b) or b=='i'):
						rhsidentifiers.append(b)
						pass

					else:

						print('Error :: in Production a line',line)
						exit(0)
						
				elif(len(b)==2):
				
					if(Isoperator(b[0]) and Isnonterminal(b[1])):						
							if   not b[0] in usedopt:
								print 'Error in production in line=',line
								exit(0) 
					else:
						print('Error :: in Production a line',line)
						exit(0)			
								
				elif(len(b)==3):
							
					if(b[0]=='(' and b[1].isalpha() and b[2]==')'):						
							usedopt.append(b[0])	
							usedopt.append(b[2])
							
						
					elif( b[0].isalpha() and Isoperator(b[1]) and b[2].isalpha() ):
						  if   not b[1] in usedopt:
								print 'Error in production in line=',line
								exit(0)
							
					else:

						print('Error :: Production is incorrect at line=',line)
						exit(0)

				if b in production.keys():	

					print('Error :: NO same RHS is allowed for alternative LHS, line=',line)
					exit(0)		

				else:

					production[b]=a			

			else:

				print('Error :: Null in production at line=',line)
				exit(0)				
				
		else:

			print('Error :: LHS should be Non-Terminal in production at line=',line)
			exit(0)
	else:

		print('Error :: -> should be present in production at line=',line)			
		exit(0)


#end of grammar checking------------------------------------------------------------




#creating parser table --------------------------------------------------------------->			

#print usedopt

ptable = dict()

for j in range(len(usedopt)):

		temp = dict()
		
		#print 'first=',usedopt[j]
		
		for i in range(len(usedopt)):
		
			#print 'second=',usedopt[i]
			
			if(usedopt[i]=='$' and usedopt[j]=='$'):
				temp['$'] = 'accept'
				
			elif(usedopt[i]=='i' and usedopt[j]=='i'):
				temp['i']='nd'
			elif(usedopt[i]=='(' and Isoperator(usedopt[j])):
				temp['(']='s'	
			elif(usedopt[i]==')' and Isoperator(usedopt[j]) and usedopt[j]!='('):
				temp[')']='r'	
			elif(precedence[usedopt[i]]>precedence[usedopt[j]]):
				temp[usedopt[i]]='s'
				
			elif(precedence[usedopt[i]]<precedence[usedopt[j]]):
				temp[usedopt[i]]='r'
				
			else:
				if(assoc[usedopt[i]]=='R'):
					temp[usedopt[i]]='s'
					
				else:
					temp[usedopt[i]]='r'
					
			#print 'val=',temp[usedopt[i]]	
				
		ptable[usedopt[j]]=temp	
#print 'usedopt---:',usedopt

print '\nParse Table\n'
print '\t','\t'.join(map(str,usedopt))
for i in range(len(usedopt)):
	if usedopt[i] in ptable.keys():
		xdict=ptable[usedopt[i]]
		#print xdict
		keylst=[]
		for key in xdict.keys():
			keylst.append(xdict[key])
		print usedopt[i],'\t','\t'.join(map(str,keylst))
		#	print xdict[j]
#end of parse table creation and printing----------------------------------------------		
#processing or parsing user input ---------------------------------------------------		
while True:
	
	
	exp=raw_input(' Enter expression :: or (q to quit) ::')
	if(exp=='q'):
		exit(0)
	#print 'y',exp
	exp=exp.strip()
	#convert expression 
	exp=convert(exp)
	#print exp

	'''check expression
	if(checkexp(exp)!=1):
		print('Error :: Enter correct Expression')
		exit(0)
	'''

	#buf=[]
		
	exp+='$'
	#print exp
	stk="$"
	i=0
	j=0
	print('\tStack\t\tExp\t\tAction\t')
	print '\t',stk,'\t\t',exp,'\t\t'

	while i<len(exp):
		
			l = len(stk)
			j=l-1
			if Isnonterminal(stk[j]):
				j=j-1
			
			t=stk[j]
			t2=exp[i]
			
			#print 't=',t
			#print 't2=',t2
			if Isnonterminal(t):
				print 'Error :: There should be operator between two terminals.'
				break
			    
			if t2 not in usedopt:
				print 'Wrong operator is used'
				break
				 
			if(ptable[t][t2]=='r'):
				#print 'stk=',stk[l-1]
			 
				if t=='i':
					var1=production[stk[j]]
					#buf.append(var1)
					
					stk=stk[:-1]
					stk+=var1
				
				elif j<l-1 and stk[j+1] in rhsidentifiers:
					var1=production[stk[j+1]]
					#while production[var1]
					#buf.append(var1)
					#print 'var=',var1
					stk=stk[:-1]
					stk+=var1
				
				elif j<l-1 and Isunaryopt(stk[j]) and (stk[j+1] in rhsidentifiers or stk[j+1]=='E')and stk[l-2:] in production:
				
					var1=production[stk[l-2:]]
					#if len(buf)>0:
					#	buf.pop()
					#else:
						#print 'error buffer is empty'
						#buf.append(var1)
					stk=stk[:-2]
					stk+=var1
						
						
				elif  j<l-1 and l>=3 and Isoperator(stk[j]) and (stk[j+1] in rhsidentifiers or stk[j+1]=='E') and (stk[j+1] in rhsidentifiers or stk[j+1]=='E') and stk[l-3:] in production :
						#print 'yes'
						var1=production[stk[l-3:]]
						#if len(buf)>1:
						#	buf.pop()
						#	buf.pop()
						#else:
						#	print 'error buffer size is less than one'
						#buf.append(var1)
						stk=stk[:-3]
						stk+=var1
							
				elif t==')': 
					
					if  l>=3 and (stk[l-2] in rhsidentifiers or stk[l-2]=='E') and stk[l-3]=='(':
						if stk[l-3:] not in production:
							print( 'Error:: not present in production')
							break
						 
						var1=production[stk[l-3:]]
						#if len(buf)>1:
						#	buf.pop()
						#	buf.pop()
						#else:
						#	print 'error buffer size is less than one'
						#buf.append(var1)
						stk=stk[:-3]
						stk+=var1
					#if l>=4 and  (stk[l-2] in rhsidentifiers or stk[l-2]=='E') and stk[l-4]=='(' and Isunaryopt(stk[l-3]):	
											
				else:
					print 'Error-----------'
					break
							
				
				'''
				while (ptable[stk[j]][t2]=='r'):
					stk=stk[:-1]
					j-=1
				'''
				print '\t',stk,'\t\t',exp[i:],'\t\tReduced'
				
			elif(ptable[t][t2]=='s'):
		
				stk+=exp[i]
				i+=1
			
				print '\t',stk,'\t\t',exp[i:],'\t\tShifted'
			
			elif(ptable[t][t2]=='nd'):
		
				print('Error :: not correct exp corresponding to the production')
				break
			
			elif(ptable[t][t2]=='accept'):			
			
				print('\nBravo :: Expression is correct! ')
				break
			
			else:
		
				print('Error')
				break	
#end of parsing of user input--------------------------------------------------------			
