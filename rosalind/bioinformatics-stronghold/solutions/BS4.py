def count_rabbits(n, k):
    # Base case: 1st aur 2nd month mein sirf 1 pair hota hai
    if n == 1 or n == 2:
        return 1
    
    # Initializing values for month 1 and month 2
    month_minus_2 = 1 # F(n-2)
    month_minus_1 = 1 # F(n-1)
    
    # Loop from month 3 up to n
    for i in range(3, n + 1):
        # Formula: Current = Previous_Month + (2_Months_Ago * Offsprings)
        current_month = month_minus_1 + (month_minus_2 * k)
        
        # Update values for next iteration
        month_minus_2 = month_minus_1
        month_minus_1 = current_month
        
    return current_month

# --- Main execution ---
if __name__ == "__main__":
    # Sample Dataset se test kar sakte ho (5 months, 3 offsprings)
    n_input = 36
    k_input = 4
    
    # Agar Rosalind ki file se read karna hai to ye uncomment kar le:
    # input_str = input("Enter n and k (e.g., 5 3): ")
    # n_input, k_input = map(int, input_str.split())

    result = count_rabbits(n_input, k_input)
    print(f"Total rabbit pairs: {result}")