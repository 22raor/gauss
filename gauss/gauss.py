from sympy import Matrix, pprint
import readline

keywords = ['r', 'mult', 'transpose', 'null', 'result','rr', 'q','av', 'atb', 'nullspace', 'inv', 'ata', 'colspace', 'rowspace', 'rank', 'orthoproject', 'show']

prev_matrix = None
prev_result = None

valid_chars = set("0123456789- /.")

def completer(text, state):
    options = [cmd for cmd in keywords if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def parse_matrix(prompt="Enter matrix", cache_prev = True):
    """General function to parse both matrices and vectors."""
    global prev_matrix, prev_result
    
    matrix = []
    print(f"{prompt} (Use 'p' for last entered, or any command to use previous result):")
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
        elif k == 'null':
            return None, None
        elif k == 'q':
            print("ok bye")
            return [[1]], 'q'
        elif k == 'result':
            return prev_result, None
        elif len(matrix) == 0 and k in keywords:
            if prev_result:
                return prev_result, k
            else:
                print("u didn't calculate a matrix dumbass")
                continue


            
        line = k
        
        if line in keywords:
            if cache_prev:
                prev_matrix = matrix
            return matrix, line
        clean_line = ''.join(filter(lambda x: x in valid_chars, line)).strip()
        if clean_line:
            row = list(map(eval, clean_line.split()))
            matrix.append(row)
    if cache_prev:
        prev_matrix = matrix
    return matrix, None


def get_colspace_proj_matrix(A: Matrix) -> Matrix:   
    if not A.rank == A.cols: # if A doesn't have full col rank, reconstruct using basis
        _, pivot_columns = A.rref()
        A = A[:, pivot_columns]
    return A * (A.T * A).inv() * A.T 



def project_onto_space(A, vector, space):
    """Perform orthogonal projection onto the column space or null space."""
    if vector:
        b = Matrix(vector)
    if space == 'colspace':
        P = get_colspace_proj_matrix(A)

    elif space == 'nullspace':
        V_perp = get_colspace_proj_matrix(A.T)
        P = Matrix.eye(V_perp.rows) - V_perp
    print("Projection Matrix")
    pprint(P)
    if vector:
        return P * b
    else:
        return None


def main():
    global prev_matrix, prev_result
    while True:
        while True:
            matrix, option = parse_matrix()
            # prev_matrix = matrix
            
            if type(matrix) == list:
                A = Matrix(matrix)
            else:
                A = matrix

            while True:
                choice = option if option else input(f"\nEnter command from {keywords}: ").strip().lower()
                
                if choice == 'r':
                    prev_result = A.echelon_form()
                    pprint(prev_result)
                elif choice == 'show':
                    pprint(A)
                elif choice == 'rr':
                    prev_result = A.rref(pivots=False)
                    pprint(prev_result)
                elif choice == 'nullspace':
                    pprint(A.nullspace())
                elif choice == 'inv':
                    prev_result = A.inv()
                    pprint(prev_result)
                elif choice == 'colspace':
                    pprint(A.columnspace())
                elif choice == 'rowspace':
                    pprint(A.rowspace())
                elif choice == 'transpose':
                    prev_result = A.T
                    pprint(prev_result)
                elif choice == 'ata':
                    prev_result = A.T * A
                    pprint(prev_result)
                elif choice == 'rank':
                    pprint(A.rank())
                elif choice == 'mult':
                    B, _ = parse_matrix(prompt="Enter matrix")
                    prev_result = A * Matrix(B)
                    pprint(prev_result)
                elif choice == 'atb':
                    b, _ = parse_matrix(prompt="Enter vector")
                    prev_result = A.T * Matrix(b)
                    pprint(prev_result)
                elif choice == 'av':
                    v, _ = parse_matrix(prompt="Enter vector")
                    prev_result = A * Matrix(v)
                    pprint(prev_result)
                elif choice == 'orthoproject':
                    vector, _ = parse_matrix(prompt="Enter vector") 
                    space = input("Project onto 'colspace' or 'nullspace': ").strip().lower()
                    
                    if space not in ['colspace', 'nullspace']:
                        print("Invalid space. Choose 'colspace' or 'nullspace'.")
                    else:
                        result = project_onto_space(A, vector, space)
                        if vector:
                            print(f"Orthogonal projection of {vector} onto {space}:")
                            pprint(result)
                
                elif choice == 'q':
                    print("cya")
                    return
                else:
                    print("Invalid input. Please enter something from", keywords)
                
                if choice in keywords:
                    break

if __name__ == "__main__":
    main()
