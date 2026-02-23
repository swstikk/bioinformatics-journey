def parse_fasta(fasta_data):
    """
    Purana FASTA parser: Data ko {ID: DNA_String} dictionary mein convert karta hai.
    """
    dna_dict = {}
    current_id = ""
    
    lines = fasta_data.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(">"):
            current_id = line[1:]
            dna_dict[current_id] = ""
        else:
            dna_dict[current_id] += line
            
    return dna_dict

def find_overlap_graphs(dna_dict, k=3):
    """
    Har string ko baaki sab strings se compare karega k=3 length ke overlap ke liye.
    """
    # Dono loops lagayenge (Har string ko har string se bhidana hai)
    for id1, seq1 in dna_dict.items():
        for id2, seq2 in dna_dict.items():
            
            # Rule 1: String khud se match nahi karni chahiye (s != t)
            if id1 != id2:
                
                # Rule 2: Pehli string ka aakhiri 3 letters (Suffix) 
                # Dusri string ke shuru ke 3 letters (Prefix) ke barabar hona chahiye
                suffix = seq1[-k:]
                prefix = seq2[:k]
                
                if suffix == prefix:
                    # Agar match hua, toh ID print kar do
                    print(f"{id1} {id2}")

# --- Main Execution ---
if __name__ == "__main__":
    # Yahan apna Rosalind ka downloaded dataset paste kar dena
    dataset = """
>Rosalind_0498
AAATAAA
>Rosalind_2391
AAATTTT
>Rosalind_2323
TTTTCCC
>Rosalind_0442
AAATCCC
>Rosalind_5013
GGGTGGG
"""
    
    # Pehle data ko dictionary mein todenge
    parsed_data = parse_fasta(dataset)
    
    # Fir graph edges nikalenge
    find_overlap_graphs(parsed_data, k=3)
