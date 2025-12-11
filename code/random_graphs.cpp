#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <iomanip>
#include <chrono>
#include <cmath>

using namespace std;
mt19937 gen;

// Generate random graph using adjacency list representation
vector<vector<int>> generateRandomGraph(int n, double p) {
    vector<vector<int>> adj(n);
    uniform_real_distribution<> dis(0.0, 1.0);
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (dis(gen) < p) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }
        }
    }
    return adj;
}

// Generate random graph using adjacency matrix representation
vector<vector<int>> generateRandomMatrix(int n, double p) {
    vector<vector<int>> matrix(n, vector<int>(n, 0));
    uniform_real_distribution<> dis(0.0, 1.0);
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (dis(gen) < p) {
                matrix[i][j] = matrix[j][i] = 1;
            }
        }
    }
    return matrix;
}

// Property 1: Has at least one edge
// O(n) - scans adjacency list until finding an edge
bool hasEdge(const vector<vector<int>>& adj) {
    for (size_t i = 0; i < adj.size(); i++) {
        if (!adj[i].empty()) return true;
    }
    return false;
}

// DFS helper for connectivity
void dfs(const vector<vector<int>>& adj, int u, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs(adj, v, visited);
    }
}

// Graph is connected
// O(n + m) using DFS
bool isConnected(const vector<vector<int>>& adj) {
    int n = adj.size();
    if (n == 0) return true;
    
    vector<bool> visited(n, false);
    dfs(adj, 0, visited);
    
    for (bool v : visited) {
        if (!v) return false;
    }
    return true;
}

// Contains a triangle (K3 subgraph)
// O(n³) - checks all C(n,3) = n(n-1)(n-2)/6 triplets
bool hasK3(const vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (!matrix[i][j]) continue; // Optimization: skip if no edge i-j
            for (int k = j + 1; k < n; k++) {
                if (matrix[i][j] && matrix[j][k] && matrix[k][i])
                    return true;
            }
        }
    }
    return false;
}

// Contains a K4 subgraph
// O(n⁴) - checks all C(n,4) = n(n-1)(n-2)(n-3)/24 4-tuples
bool hasK4(const vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (!matrix[i][j]) continue;
            for (int k = j + 1; k < n; k++) {
                if (!matrix[i][k] || !matrix[j][k]) continue;
                for (int l = k + 1; l < n; l++) {
                    if (matrix[i][j] && matrix[i][k] && matrix[i][l] &&
                        matrix[j][k] && matrix[j][l] && matrix[k][l]) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

// Backtracking helper for Hamiltonian cycle
// NP-complete problem - O(n!) worst case
bool hamiltonHelper(int u, int start, vector<bool>& visited,
                    const vector<vector<int>>& adj, int count, int n) {
    if (count == n) {
        for (int v : adj[u]) {
            if (v == start) return true;
        }
        return false;
    }
    
    for (int v : adj[u]) {
        if (!visited[v]) {
            visited[v] = true;
            if (hamiltonHelper(v, start, visited, adj, count + 1, n))
                return true;
            visited[v] = false;
        }
    }
    return false;
}

// Property 5: Has a Hamilton cycle
// Uses backtracking - practical only for small n (≤ 20)
bool isHamiltonian(const vector<vector<int>>& adj) {
    int n = adj.size();
    if (n == 0) return false;
    if (n == 1) return true; // Single vertex has trivial cycle
    if (n == 2) {
        // Need edge between both vertices
        return !adj[0].empty() && !adj[1].empty();
    }
    
    vector<bool> visited(n, false);
    visited[0] = true;
    return hamiltonHelper(0, 0, visited, adj, 1, n);
}

// Run experiment for a given property
void runExperiment(const string& propertyName, int n, int trials,
                   bool (*testFunc)(const vector<vector<int>>&),
                   bool useMatrix, ofstream& outFile) {
    
    cout << "Testing " << propertyName << " with n = " << n << endl;
    
    // Test various values of p
    vector<double> pValues;
    for (double p = 0.0; p <= 1.0; p += 0.02) {
        pValues.push_back(p);
    }
    
    outFile << "# " << propertyName << " n=" << n << " trials=" << trials << endl;
    outFile << "p,probability" << endl;
    
    for (double p : pValues) {
        int successCount = 0;
        for (int t = 0; t < trials; t++) {
            if (useMatrix) {
                auto graph = generateRandomMatrix(n, p);
                if (testFunc(graph)) successCount++;
            } else {
                auto graph = generateRandomGraph(n, p);
                if (testFunc(graph)) successCount++;
            }
        }
        double probability = (double)successCount / trials;
        outFile << fixed << setprecision(4) << p << "," << probability << endl;
    }
    outFile << endl;
}

// Wrapper functions for consistent interface
bool hasEdgeWrapper(const vector<vector<int>>& adj) { return hasEdge(adj); }
bool isConnectedWrapper(const vector<vector<int>>& adj) { return isConnected(adj); }
bool hasK3Wrapper(const vector<vector<int>>& matrix) { return hasK3(matrix); }
bool hasK4Wrapper(const vector<vector<int>>& matrix) { return hasK4(matrix); }
bool isHamiltonianWrapper(const vector<vector<int>>& adj) { return isHamiltonian(adj); }

int main() {
    // Seed random generator
    random_device rd;
    gen.seed(rd());
    
    int trials = 500; // Number of trials per (n, p) pair
    
    ofstream outFile("experiment_results.csv");
    
    cout << "=== Random Graphs Threshold Experiment ===" << endl;
    cout << "Running " << trials << " trials per data point" << endl << endl;
    
    // Experiment 1: Has Edge
    // Threshold: p = 1/C(n,2) = 2/(n(n-1)) ≈ 2/n² for large n
    cout << "\n--- Experiment 1: Has Edge ---" << endl;
    for (int n : {10, 50, 100, 500}) {
        runExperiment("HasEdge", n, trials, hasEdgeWrapper, false, outFile);
    }
    
    // Experiment 2: Has Triangle (K3)
    // Threshold: p = 1/n (sharp threshold)
    cout << "\n--- Experiment 2: Has Triangle (K3) ---" << endl;
    for (int n : {20, 50, 100, 200}) {
        runExperiment("HasK3", n, trials, hasK3Wrapper, true, outFile);
    }
    
    // Experiment 3: Is Connected
    // Threshold: p = ln(n)/n (sharp threshold by Erdős-Rényi)
    cout << "\n--- Experiment 3: Is Connected ---" << endl;
    for (int n : {20, 50, 100, 200}) {
        runExperiment("IsConnected", n, trials, isConnectedWrapper, false, outFile);
    }
    
    // Experiment 4: Has K4
    // Threshold: p = n^(-2/3)
    cout << "\n--- Experiment 4: Has K4 ---" << endl;
    for (int n : {20, 50, 100}) {
        runExperiment("HasK4", n, trials, hasK4Wrapper, true, outFile);
    }
    
    // Experiment 5: Is Hamiltonian
    // Threshold: p = ln(n)/n (same as connectivity, roughly)
    // Only small n due to NP-completeness
    cout << "\n--- Experiment 5: Is Hamiltonian ---" << endl;
    for (int n : {8, 10, 12, 15}) {
        runExperiment("IsHamiltonian", n, trials, isHamiltonianWrapper, false, outFile);
    }

    outFile.close();
    cout << "\nResults saved to experiment_results.csv" << endl;
    
    return 0;
}
