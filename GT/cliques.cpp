#include <bits/stdc++.h>
using namespace std;

class Graph
{
    vector<vector<int>> adjMatrix;
    int n;

    bool isAdjacentToAll(int v, const vector<int> &clique)
    {
        for (int u : clique)
        {
            if (adjMatrix[u][v] == 0)
                return false;
        }
        return true;
    }

    int maxCliqueUtil(vector<int> &clique, int start)
    {
        int maxSize = clique.size();
        for (int v = start; v < n; v++)
        {
            if (isAdjacentToAll(v, clique))
            {
                clique.push_back(v);
                maxSize = max(maxSize, maxCliqueUtil(clique, v + 1));
                clique.pop_back();
            }
        }
        return maxSize;
    }

public:
    Graph(const vector<pair<int, int>> &edges, int verticesCount) : n(verticesCount)
    {
        adjMatrix.resize(n, vector<int>(n, 0));
        for (auto &e : edges)
        {
            int u = e.first, v = e.second;
            adjMatrix[u][v] = 1;
            adjMatrix[v][u] = 1;
        }
    }

    int maxClique()
    {
        vector<int> currentClique;
        return maxCliqueUtil(currentClique, 0);
    }
};

int main()
{
    int verticesCount = 10;
    vector<pair<int, int>> edges = {
        {0, 1}, {0, 4}, {0, 5}, {1, 2}, {1, 6}, {2, 3}, {2, 7}, {3, 4}, {3, 8}, {4, 9}, {5, 7}, {5, 8}, {6, 8}, {6, 9}, {7, 9}};

    Graph g(edges, verticesCount);
    cout << "Maximum Clique Size: " << g.maxClique() << endl;
    return 0;
}
