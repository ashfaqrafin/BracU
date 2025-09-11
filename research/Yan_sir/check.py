import numpy as np
import random
import json

def generate_sample_graph(num_researchers=50, num_awardees=8, seed=42):
    """
    Generates:
    - A list of researcher IDs ["R0", "R1", ..., "R49"]
    - A random adjacency matrix (50×50) where matrix[i][j] = 1 if Ri cites Rj
    - A dummy dict of award winners { "Rk": "Award Name", ... }
    """
    random.seed(seed)
    np.random.seed(seed)

    researchers = [f"R{i}" for i in range(num_researchers)]
    adj = np.random.randint(0, 2, size=(num_researchers, num_researchers))
    np.fill_diagonal(adj, 0)

    awardees = random.sample(researchers, k=num_awardees)
    awards = {r: random.choice(["Nobel Prize", "Turing Award"]) for r in awardees}

    return researchers, adj, awards

def compute_rank_citation_only(adj_matrix, initial_weights=None):
    """
    Implements Eq. (3): rank_i = Σ_j w_j * (c_{j,i} / c_j)
    where c_{j,i} = adj_matrix[j,i], c_j = sum_k adj_matrix[j,k], w_j = 1.
    """
    N = adj_matrix.shape[0]
    w = np.ones(N) if initial_weights is None else np.array(initial_weights, float).flatten()
    c_out = adj_matrix.sum(axis=1)
    ranks = np.zeros(N, float)
    for j in range(N):
        if c_out[j] > 0:
            ranks += w[j] * (adj_matrix[j, :] / c_out[j])
    return ranks

if __name__ == "__main__":
    # Generate graph and compute ranks
    researchers, adj, awards = generate_sample_graph()
    ranks = compute_rank_citation_only(adj)

    # Build JSON structure
    graph_data = {
        "researchers": researchers,
        "award_winners": [
            {"id": rid, "award": awards[rid]}
            for rid in sorted(awards.keys(), key=lambda x: int(x[1:]))
        ],
        "citations": [
            {"from": f"R{j}", "to": f"R{i}"}
            for j in range(adj.shape[0])
            for i in range(adj.shape[1])
            if adj[j, i] == 1
        ],
        "ranks_eq3": [
            {"id": researchers[i], "rank": float(f"{ranks[i]:.4f}")}
            for i in range(len(researchers))
        ]
    }

    # Save to a separate JSON file
    output_filename = "researcher_graph.json"
    with open(output_filename, "w") as f:
        json.dump(graph_data, f, indent=2)

    print(f"Graph data written to {output_filename}")
