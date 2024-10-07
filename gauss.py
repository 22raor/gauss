from sympy import Matrix, pprint
import readline

keywords = ['r', 'rr', 'q', 'nullspace', 'inv', 'colspace', 'rowspace', 'rank', 'orthoproject', 'show']

prev_matrix = None

valid_chars = set("0123456789- ")

def completer(text, state):
    options = [cmd for cmd in keywords if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def parse_matrix(prompt="Enter matrix"):
    """General function to parse both matrices and vectors."""
    matrix = []
    print(f"{prompt} (or 'p' for previous matrix):")
    while True:
        k = input().strip()
        # print(k, int(k))
        k = k.replace("−","-")
        if k == "":
            if len(matrix) > 0:
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
        clean_line = ''.join(filter(lambda x: x in valid_chars, line)).strip()
        if clean_line:
            row = list(map(int, clean_line.split()))
            matrix.append(row)
    return matrix, None


def get_colspace_proj_matrix(A: Matrix) -> Matrix:   
    if not A.rank == A.cols: # if A doesn't have full col rank, reconstruct using basis
        _, pivot_columns = A.rref()
        A = A[:, pivot_columns]
    return A * (A.T * A).inv() * A.T 



def project_onto_space(A, vector, space):
    """Perform orthogonal projection onto the column space or null space."""
    b = Matrix(vector)
    if space == 'colspace':
        P = get_colspace_proj_matrix(A)

    elif space == 'nullspace':
        V_perp = get_colspace_proj_matrix(A.T)
        P = Matrix.eye(V_perp.rows) - V_perp
    print("Projection Matrix")
    pprint(P)
    return P * b


def main():
    global prev_matrix
    while True:
        while True:
            matrix, option = parse_matrix()
            prev_matrix = matrix
            A = Matrix(matrix)

            while True:
                choice = option if option else input(f"\nEnter command from {keywords}: ").strip().lower()
                
                if choice == 'r':
                    pprint(A.echelon_form())
                elif choice == 'show':
                    pprint(A)
                elif choice == 'rr':
                    pprint(A.rref(pivots=False))
                elif choice == 'nullspace':
                    pprint(A.nullspace())
                elif choice == 'inv':
                    pprint(A.inv())
                elif choice == 'colspace':
                    pprint(A.columnspace())
                elif choice == 'rowspace':
                    pprint(A.rowspace())
                elif choice == 'rank':
                    pprint(A.rank())
                elif choice == 'orthoproject':
                    vector, _ = parse_matrix(prompt="Enter vector") 
                    space = input("Project onto 'colspace' or 'nullspace': ").strip().lower()
                    
                    if space not in ['colspace', 'nullspace']:
                        print("Invalid space. Choose 'colspace' or 'nullspace'.")
                    else:
                        result = project_onto_space(A, vector, space)
                        print(f"Orthogonal projection of {vector} onto {space}:")
                        pprint(result)
                
                elif choice == 'q':
                    print("fuck linear")
                    return
                else:
                    print("Invalid input. Please enter something from", keywords)
                
                if choice in keywords:
                    break

if __name__ == "__main__":
    main()
