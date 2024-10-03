from sympy import Matrix, pprint

keywords = ['r', 'rr', 'q', 'n', 'inv', 'colspace', 'rowspace']

def parse_matrix():
    matrix = []
    print("Enter matrix:")
    while True:
        k = input().strip()
        if k == "":
            if len(matrix)> 0:
                break
            else:
                continue
        line = k
        
        if line in keywords:
            return matrix, line
        clean_line = ''.join(filter(lambda x: x.isdigit() or x.isspace(), line)).strip()
        if clean_line:
            row = list(map(int, clean_line.split()))
            matrix.append(row)
    return matrix, None

def main():
    while True:

        while True:
            matrix, option = parse_matrix()
            A = Matrix(matrix)

            while True:
                #  
                choice = option if option else input("\nEnter 'r' for echelon form, 'rr' for reduced echelon form, or 'q' to quit:").strip().lower()
                
                
                if choice == 'r':
                    pprint(A.echelon_form())
                elif choice == 'rr':
                    pprint(A.rref(pivots=False))
                elif choice == 'n':
                    pprint(A.nullspace())
                elif choice == 'inv':
                    pprint(A.inv())
                elif choice == 'colspace':
                    pprint(A.columnspace())
                elif choice == 'rowspace':
                    pprint(A.rowspace())
                elif choice == 'q':
                    print("fuck linear")
                    return
                else:
                    print("Invalid input. Please enter something from", keywords)
                
                if choice in keywords:
                    break

if __name__ == "__main__":
    main()
