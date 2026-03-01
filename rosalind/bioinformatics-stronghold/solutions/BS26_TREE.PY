def complete_the_tree(dataset):
    # Data ko lines mein todte hain
    lines = dataset.strip().split('\n')
    
    # Pehli line mein total nodes (n) diye hain
    total_nodes = int(lines[0].strip())
    
    ## Baaki ki saari lines existing edges hain
    # (Pehli line hata kar jo bacha, unki ginti kar lo)
    existing_edges_list = lines[1:]
    
    # Filter kar lete hain in case koi khali line aa jaye string mein
    valid_edges = [edge for edge in existing_edges_list if edge.strip()]
    number_of_existing_edges = len(valid_edges)
    
    # The Magic Formula: Ek tree mein hamesha (n - 1) edges hoti hain
    # Toh hume kitni aur chahiye? (n - 1) minus jo pehle se hain
    edges_needed = (total_nodes - 1) - number_of_existing_edges
    
    return edges_needed

# --- Main Execution ---
if __name__ == "__main__":
    # Yahan apna Rosalind ka dataset paste karna
    sample_dataset = """
10
1 2
2 8
4 10
5 9
6 10
7 9
"""
    
    result = complete_the_tree(sample_dataset)
    print("Minimum edges required:", result)
