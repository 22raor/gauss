from sympy import Matrix, pprint

keywords = ['r', 'rr', 'q', 'n', 'inv', 'colspace', 'rowspace', 'rank']

prev_matrix = None


def parse_matrix():
    matrix = []
    print("Enter matrix (or 'p' for previous matrix):")
    while True:
        k = input().strip()
        if k == "":
            if len(matrix)> 0:
                break
            else:
                continue
        elif k == 'p':
            if prev_matrix:
                return prev_matrix, None
            else:
                print("u never entered a matrix dumbass")
                continue
        elif k == 'q':
            print("ok bye")
            return [[1]], 'q'
            
        line = k
        
        if line in keywords:
            return matrix, line
        clean_line = ''.join(filter(lambda x: x.isdigit() or x.isspace(), line)).strip()
        if clean_line:
            row = list(map(int, clean_line.split()))
            matrix.append(row)
    return matrix, None

def main():
    global prev_matrix
    while True:

        while True:
            matrix, option = parse_matrix()
            prev_matrix = matrix
            A = Matrix(matrix)

            while True:
                #  
                choice = option if option else input(f"\nEnter command from {keywords}").strip().lower()
                
                
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
                elif choice == 'rank':
                    pprint(A.rank())
                # elif choice == 'lu':
                #     pprint(A.LUdecomposition())
                #     print("got rid of fractoins")
                #     pprint(A.LUdecompositionFF())
                elif choice == 'q':
                    print("fuck linear")
                    return
                else:
                    print("Invalid input. Please enter something from", keywords)
                
                if choice in keywords:
                    break

if __name__ == "__main__":
    main()
