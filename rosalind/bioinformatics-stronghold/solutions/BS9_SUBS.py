dna="atatatata"
mot="at"
for i in range(len(dna)):
    sdna=dna[i:]
    if dna[i : i + len(mot)] == mot:      
      print(i+1, end=" ")

