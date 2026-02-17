print("enter the value k,m,n repec..")

k= int(input(" k ")) 
m=int(input(" m ")) 
n=int(input(" n ")) 



total=k+m+n
pb_n=n/total
pb_m=m/total
pb_nn=pb_n*(n-1)/(total-1)
pb_mn=pb_n*(m/(total-1))
pb_nm=pb_m*(n/(total-1))
pb_mm=pb_m*(m-1)/(total-1)

print(1-(pb_nn+(pb_mn+pb_nm)*0.5+pb_mm*0.252
))

    
    
