#include <bits/stdc++.h>
using namespace std;
#define endl '\n'


/* Task-1 start here */
/* int maxDegMat(vector<vector<int>>& adjMat) { */
/*     int maxDeg = 0; */
/*     int vertex = -1; */
/*     int n = adjMat.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int deg = 0; */
/*         for (int j = 0; j < n; ++j) { */
/*             if (adjMat[i][j] == 1) { */
/*                 deg++; */
/*             } */
/*         } */
/*         if (deg > maxDeg) { */
/*             maxDeg = deg; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return maxDeg; */
/* } */
/**/
/* int maxDegLst(vector<vector<int>>& adjLst) { */
/*     int maxDeg = 0; */
/*     int vertex = -1; */
/*     int n = adjLst.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int deg = adjLst[i].size(); */
/*         if (deg > maxDeg) { */
/*             maxDeg = deg; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return maxDeg; */
/* } */
/**/
/* signed main(void) { */
/*     vector<vector<int>> adjMat = { */
/*         {0, 1, 1, 0, 0, 1, 0}, */
/*         {1, 0, 1, 1, 0, 0, 0}, */
/*         {1, 1, 0, 1, 1, 0, 0}, */
/*         {0, 1, 1, 0, 1, 1, 0}, */
/*         {0, 0, 1, 1, 0, 1, 1}, */
/*         {1, 0, 0, 1, 1, 0, 1}, */
/*         {0, 0, 0, 0, 1, 1, 0} */
/*     }; */
/**/
/*     vector<vector<int>> adjLst = { */
/*         {1, 2, 5}, */
/*         {0, 2, 3}, */
/*         {0, 1, 3, 4}, */
/*         {1, 2, 4, 5}, */
/*         {2, 3, 5, 6}, */
/*         {0, 3, 4, 6}, */
/*         {4, 5} */
/*     }; */
/**/
/*     cout << "Max degree (Adjacency Matrix): " << maxDegMat(adjMat) << endl; */
/*     cout << "Max degree (Adjacency List): " << maxDegLst(adjLst) << endl; */
/**/
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */
/* int maxM(vector<vector<int>>& mat) { */
/*     int maxSum = 0, vertex = -1, n = mat.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int sum = 0; */
/*         for (int j = 0; j < n; ++j) { */
/*             sum += mat[i][j]; */
/*         } */
/*         if (sum > maxSum) { */
/*             maxSum = sum; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return vertex; */
/* } */
/**/
/* int maxL(vector<vector<pair<int, int>>>& list) { */
/*     int maxSum = 0, vertex = -1, n = list.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int sum = 0; */
/*         for (auto& edge : list[i]) { */
/*             sum += edge.second; */
/*         } */
/*         if (sum > maxSum) { */
/*             maxSum = sum; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return vertex; */
/* } */
/**/
/* int main() { */
/*     vector<vector<int>> adjMatrix = { */
/*         {0, 2, 3, 0, 0, 1, 0}, */
/*         {2, 0, 4, 5, 0, 0, 0}, */
/*         {3, 4, 0, 6, 7, 0, 0}, */
/*         {0, 5, 6, 0, 8, 9, 0}, */
/*         {0, 0, 7, 8, 0, 10, 11}, */
/*         {1, 0, 0, 9, 10, 0, 12}, */
/*         {0, 0, 0, 0, 11, 12, 0} */
/*     }; */
/**/
/*     vector<vector<pair<int, int>>> adjList = { */
/*         {{1, 2}, {2, 3}, {5, 1}}, */
/*         {{0, 2}, {2, 4}, {3, 5}}, */
/*         {{0, 3}, {1, 4}, {3, 6}, {4, 7}}, */
/*         {{1, 5}, {2, 6}, {4, 8}, {5, 9}}, */
/*         {{2, 7}, {3, 8}, {5, 10}, {6, 11}}, */
/*         {{0, 1}, {3, 9}, {4, 10}, {6, 12}}, */
/*         {{4, 11}, {5, 12}} */
/*     }; */
/**/
/*     cout << "Vertex with max weight sum (Adjacency Matrix): " << maxM(adjMatrix) << endl; */
/*     cout << "Vertex with max weight sum (Adjacency List): " << maxL(adjList) << endl; */
/**/
/*     return 0; */
/* } */
/* Task-2 end here */

/* Task-3 start here */

/* int maxDegM(vector<vector<int>>& mat) { */
/*     int maxDeg = 0, vertex = -1, n = mat.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int deg = 0; */
/*         for (int j = 0; j < n; ++j) { */
/*             if (mat[i][j] != 0) { */
/*                 deg++; */
/*             } */
/*         } */
/*         if (deg > maxDeg) { */
/*             maxDeg = deg; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return maxDeg; */
/* } */
/**/
/* int maxDegL(vector<vector<pair<int, int>>>& list) { */
/*     int maxDeg = 0, vertex = -1, n = list.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int deg = list[i].size(); */
/*         if (deg > maxDeg) { */
/*             maxDeg = deg; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return maxDeg; */
/* } */
/**/
/* int maxSumM(vector<vector<int>>& mat) { */
/*     int maxSum = 0, vertex = -1, n = mat.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int sum = 0; */
/*         for (int j = 0; j < n; ++j) { */
/*             sum += mat[i][j]; */
/*         } */
/*         if (sum > maxSum) { */
/*             maxSum = sum; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return vertex; */
/* } */
/**/
/* int maxSumL(vector<vector<pair<int, int>>>& list) { */
/*     int maxSum = 0, vertex = -1, n = list.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int sum = 0; */
/*         for (auto& edge : list[i]) { */
/*             sum += edge.second; */
/*         } */
/*         if (sum > maxSum) { */
/*             maxSum = sum; */
/*             vertex = i; */
/*         } */
/*     } */
/*     return vertex; */
/* } */
/* int main() { */
/*     vector<vector<int>> adjMatrix = { */
/*         {0, 2, 3, 0, 0, 1, 0}, */
/*         {0, 0, 4, 5, 0, 0, 0}, */
/*         {0, 0, 0, 6, 7, 0, 0}, */
/*         {0, 0, 0, 0, 8, 9, 0}, */
/*         {0, 0, 0, 0, 0, 10, 11}, */
/*         {0, 0, 0, 0, 0, 0, 12}, */
/*         {0, 0, 0, 0, 0, 0, 0} */
/*     }; */
/**/
/*     vector<vector<pair<int, int>>> adjList = { */
/*         {{1, 2}, {2, 3}, {5, 1}}, */
/*         {{2, 4}, {3, 5}}, */
/*         {{3, 6}, {4, 7}}, */
/*         {{4, 8}, {5, 9}}, */
/*         {{5, 10}, {6, 11}}, */
/*         {{6, 12}}, */
/*         {} */
/*     }; */
/**/
/*     cout << "Max out-degree (Adjacency Matrix): " << maxDegM(adjMatrix) << endl; */
/*     cout << "Max out-degree (Adjacency List): " << maxDegL(adjList) << endl; */
/*     cout << "Vertex with max outgoing weight sum (Adjacency Matrix): " << maxSumM(adjMatrix) << endl; */
/*     cout << "Vertex with max outgoing weight sum (Adjacency List): " << maxSumL(adjList) << endl; */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */


/* Task-4 start here */
vector<vector<int>> toUndirMat(vector<vector<int>>& mat) {
    int n = mat.size();
    vector<vector<int>> undirMat(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != 0) {
                undirMat[i][j] = mat[i][j];
                undirMat[j][i] = mat[i][j];
            }
        }
    }
    return undirMat;
}

vector<vector<pair<int, int>>> toUndirList(vector<vector<pair<int, int>>>& list) {
    int n = list.size();
    vector<vector<pair<int, int>>> undirList(n);
    for (int i = 0; i < n; ++i) {
        for (auto& edge : list[i]) {
            int j = edge.first;
            int w = edge.second;
            undirList[i].push_back({j, w});
            undirList[j].push_back({i, w});
        }
    }
    return undirList;
}
int main() {
    vector<vector<int>> adjMatrix = {
        {0, 2, 3, 0, 0, 1, 0},
        {0, 0, 4, 5, 0, 0, 0},
        {0, 0, 0, 6, 7, 0, 0},
        {0, 0, 0, 0, 8, 9, 0},
        {0, 0, 0, 0, 0, 10, 11},
        {0, 0, 0, 0, 0, 0, 12},
        {0, 0, 0, 0, 0, 0, 0}
    };

    vector<vector<pair<int, int>>> adjList = {
        {{1, 2}, {2, 3}, {5, 1}},
        {{2, 4}, {3, 5}},
        {{3, 6}, {4, 7}},
        {{4, 8}, {5, 9}},
        {{5, 10}, {6, 11}},
        {{6, 12}},
        {}
    };

    vector<vector<int>> undirMat = toUndirMat(adjMatrix);
    vector<vector<pair<int, int>>> undirList = toUndirList(adjList);

    cout << "Undirected Adjacency Matrix:" << endl;
    for (const auto& row : undirMat) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }

    cout << "Undirected Adjacency List:" << endl;
    for (int i = 0; i < undirList.size(); ++i) {
        cout << i << ": ";
        for (const auto& edge : undirList[i]) {
            cout << "(" << edge.first << ", " << edge.second << ") ";
        }
        cout << endl;
    }

    return 0;
}
/* Task-4 end here */

