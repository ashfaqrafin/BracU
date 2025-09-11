import numpy as np
import random

def generate_sample_graph(num_researchers=50, num_awardees=8, seed=42):
    """
    Generates:
    - A list of researcher IDs ["R0", "R1", ..., "R49"]
    - A random adjacency matrix (50×50) where matrix[i][j] = 1 if R_i cites R_j
    - A dummy list of award winners (Nobel Prize or Turing Award)
    """
    random.seed(seed)
    np.random.seed(seed)

    # 1. Create researcher identifiers
    researchers = [f"R{i}" for i in range(num_researchers)]

    # 2. Build a random citation adjacency matrix
    #    matrix[i][j] == 1 means researcher i cites researcher j
    adj_matrix = np.random.randint(0, 2, size=(num_researchers, num_researchers))
    # remove self-citations
    np.fill_diagonal(adj_matrix, 0)

    # 3. Pick a dummy subset of researchers as award winners
    awardees = random.sample(researchers, k=num_awardees)
    awards = {}
    for r in awardees:
        awards[r] = random.choice(["Nobel Prize", "Turing Award"])

    return researchers, adj_matrix, awards

if __name__ == "__main__":
    researchers, mat, award_dict = generate_sample_graph()

    # Print out the components
    print("Researchers (50):")
    print(researchers)
    print("\nAdjacency Matrix (50×50):")
    # Represent as 0/1 matrix rows
    for row in mat:
        print(" ".join(str(x) for x in row))
    print("\nDummy Award Winners:")
    for r, award in award_dict.items():
        print(f"  - {r}: {award}")
