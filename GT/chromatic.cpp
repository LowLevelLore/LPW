#include <cassert>
#include <iostream>
#include <set>
#include <unordered_map>
#include <vector>
#include <algorithm>

class Graph
{
private:
    std::set<int> m_vertices;
    std::unordered_map<int, std::set<int>> m_edges;
    int m_numEdges = 0;
    int m_numVertices = 0;

    // Helper method for chromatic number backtracking.
    void backtrackColoring(const std::vector<int> &vertices,
                           int idx,
                           std::unordered_map<int, int> &coloring,
                           int currentMax,
                           int &best) const
    {
        if (idx == vertices.size())
        {
            best = std::min(best, currentMax);
            return;
        }

        // Prune search if current max already exceeds the best found.
        if (currentMax >= best)
            return;

        int vertex = vertices[idx];
        // Try colors in the range [1, currentMax+1]
        for (int color = 1; color <= currentMax + 1; color++)
        {
            bool valid = true;
            // Check that no neighbor is colored with the same color.
            if (m_edges.find(vertex) != m_edges.end())
            {
                for (int neighbor : m_edges.at(vertex))
                {
                    if (coloring.find(neighbor) != coloring.end() && coloring.at(neighbor) == color)
                    {
                        valid = false;
                        break;
                    }
                }
            }
            if (valid)
            {
                coloring[vertex] = color;
                int newMax = std::max(currentMax, color);
                backtrackColoring(vertices, idx + 1, coloring, newMax, best);
                coloring.erase(vertex);
            }
        }
    }

public:
    Graph(std::unordered_map<int, std::set<int>> edges) noexcept
        : m_edges(edges)
    {
        for (const auto &elem : m_edges)
        {
            m_vertices.insert(elem.first);
        }
        for (const auto &list : m_edges)
        {
            for (int node : list.second)
            {
                m_vertices.insert(node);
                if (node != list.first)
                    m_numEdges++;
            }
        }
        m_numEdges /= 2;
        m_numVertices = m_vertices.size();
        assert(m_vertices.size() == m_numVertices);
    }

    Graph(const Graph &obj)
        : m_edges(obj.m_edges), m_vertices(obj.m_vertices),
          m_numEdges(obj.m_numEdges), m_numVertices(obj.m_numVertices)
    {
        assert(m_vertices.size() == m_numVertices);
    }

    ~Graph() {}

    bool operator==(const Graph &g) const
    {
        if (this->m_numEdges == g.m_numEdges and
            this->m_numVertices == g.m_numVertices)
        {
            if (this->m_edges == g.m_edges and
                this->m_vertices == g.m_vertices)
            {
                return true;
            }
        }
        return false;
    }

    // Existing methods (e.g., checkPlanar, removeSelfLoopsAndParallelEdges, etc.)
    bool checkPlanar()
    {
        while (true)
        {
            bool found = false;
            removeSelfLoopsAndParallelEdges();
            std::set<int> currentVertices = m_vertices;
            for (int vertex : currentVertices)
            {
                if (m_edges[vertex].size() == 2)
                {
                    auto it = m_edges[vertex].begin();
                    int first = *it;
                    int second = *(++it);
                    dissolveVertex(vertex, first, second);
                    found = true;
                }
            }
            if (!found)
                break;
            printGraph();
        }
        std::cout << m_numEdges << ", " << m_numVertices << std::endl;
        if (m_numEdges == 1)
        {
            return true;
        }
        else if (m_numVertices == 4 && m_numEdges == 6)
        {
            return true;
        }
        else if (m_numVertices >= 5 && m_numEdges >= 7)
        {
            Graph k5({{1, {2, 3, 4, 5}},
                      {2, {1, 3, 4, 5}},
                      {3, {1, 2, 4, 5}},
                      {4, {1, 2, 3, 5}},
                      {5, {1, 2, 3, 4}}});

            Graph k33({{1, {4, 5, 6}},
                       {2, {4, 5, 6}},
                       {3, {4, 5, 6}},
                       {4, {1, 2, 3}},
                       {5, {1, 2, 3}},
                       {6, {1, 2, 3}}});

            if (m_numEdges <= 3 * m_numVertices - 6)
            {
                if (k5.isSubsetOf(*this) or k33.isSubsetOf(*this))
                {
                    return false;
                }
                else
                {
                    // Check homeomorphic to k33 and k5 and if it is return
                    // false. Else return true. -> Ma'am said not to do so
                    std::cout << "This might be false positive" << std::endl;
                    return true;
                }
            }
            else
            {
                return false;
            }
        }
        else
        {
            return true;
        }
    }

    void removeSelfLoopsAndParallelEdges()
    {
        for (auto &[vertex, neighbors] : m_edges)
        {
            if (neighbors.count(vertex))
            {
                neighbors.erase(vertex);
            }

            for (auto it = neighbors.begin(); it != neighbors.end();)
            {
                int neighbor = *it;
                if (m_edges[neighbor].count(vertex) > 1)
                {
                    m_edges[neighbor].erase(vertex);
                    it = neighbors.erase(it);
                    m_numEdges--;
                }
                else
                {
                    ++it;
                }
            }
        }
    }

    void dissolveVertex(int vertex, int n1, int n2)
    {
        std::cout << "Dissolving: " << vertex << std::endl;
        m_edges[n1].erase(vertex);
        m_edges[n2].erase(vertex);
        m_edges[n1].insert(n2);
        m_edges[n2].insert(n1);
        m_edges.erase(vertex);
        m_vertices.erase(vertex);
        m_numEdges--;
        m_numVertices--;
    }

    bool isSubsetOf(const Graph &superSet) const
    {
        if (m_vertices.size() > superSet.m_vertices.size())
            return false;

        for (int vertex : m_vertices)
        {
            if (superSet.m_vertices.find(vertex) == superSet.m_vertices.end())
                return false;
        }

        for (const auto &[vertex, neighbors] : m_edges)
        {
            if (superSet.m_edges.find(vertex) == superSet.m_edges.end())
                return false;

            for (int neighbor : neighbors)
            {
                if (superSet.m_edges.at(vertex).find(neighbor) ==
                    superSet.m_edges.at(vertex).end())
                    return false;
            }
        }
        return true;
    }

    void printGraph()
    {
        std::cout << "Vertices: ";
        for (int vertex : m_vertices)
        {
            std::cout << vertex << ", ";
        }
        std::cout << "\b\b\n\n";

        std::cout << "Edges: " << std::endl;
        for (const auto &[vertex, neighbors] : m_edges)
        {
            std::cout << vertex << " -> ";
            for (int conn : neighbors)
            {
                std::cout << conn << ", ";
            }
            std::cout << "\b\b" << std::endl;
        }
    }

    // Public method to compute the chromatic number of the graph.
    int chromaticNumber() const
    {
        // Convert vertices from set to vector for indexing.
        std::vector<int> vertices(m_vertices.begin(), m_vertices.end());
        // It might be useful to sort vertices by degree to potentially speed up coloring.
        std::sort(vertices.begin(), vertices.end(),
                  [this](int a, int b)
                  {
                      return m_edges.at(a).size() > m_edges.at(b).size();
                  });
        int best = vertices.size(); // worst-case: all vertices need distinct colors.
        std::unordered_map<int, int> coloring;
        backtrackColoring(vertices, 0, coloring, 0, best);
        return best;
    }
};

int main()
{
    // Existing test cases for planar checks.
    std::cout << "Test Case 1: Single Edge" << std::endl;
    Graph singleEdge({{1, {2}}, {2, {1}}});
    std::cout << "Planar? " << (singleEdge.checkPlanar() ? "Yes" : "No")
              << std::endl
              << std::endl;

    std::cout << "Test Case 2: K4 Graph" << std::endl;
    Graph k4({{1, {2, 3, 4}}, {2, {1, 3, 4}}, {3, {1, 2, 4}}, {4, {1, 2, 3}}});
    std::cout << "Planar? " << (k4.checkPlanar() ? "Yes" : "No") << std::endl
              << std::endl;

    std::cout << "Test Case 3: Peterson's Graph" << std::endl;
    Graph peterson({{1, {2, 5, 6}},
                    {2, {1, 3, 7}},
                    {3, {2, 4, 8}},
                    {4, {3, 5, 9}},
                    {5, {1, 4, 10}},
                    {6, {1, 8, 9}},
                    {7, {2, 10, 9}},
                    {8, {3, 6, 10}},
                    {9, {4, 7, 6}},
                    {10, {5, 8, 7}}});
    std::cout << "Planar? " << (peterson.checkPlanar() ? "Yes" : "No")
              << std::endl
              << std::endl;

    std::cout << "Test Case 4: K5 Graph (Non-Planar)" << std::endl;
    Graph k5({{1, {2, 3, 4, 5}},
              {2, {1, 3, 4, 5}},
              {3, {1, 2, 4, 5}},
              {4, {1, 2, 3, 5}},
              {5, {1, 2, 3, 4}}});
    std::cout << "Planar? " << (k5.checkPlanar() ? "Yes" : "No") << std::endl
              << std::endl;

    std::cout << "Test Case 5: K3,3 Graph (Non-Planar)" << std::endl;
    Graph k33({{1, {4, 5, 6}},
               {2, {4, 5, 6}},
               {3, {4, 5, 6}},
               {4, {1, 2, 3}},
               {5, {1, 2, 3}},
               {6, {1, 2, 3}}});
    std::cout << "Planar? " << (k33.checkPlanar() ? "Yes" : "No") << std::endl
              << std::endl;

    // Test chromatic number computation on a few examples.
    std::cout << "Chromatic Number Test Cases:" << std::endl;

    // For a simple graph (edge): The chromatic number is 2.
    std::cout << "Single Edge Graph Chromatic Number: " << singleEdge.chromaticNumber() << std::endl;

    // For a complete graph on 4 vertices (K4): The chromatic number is 4.
    std::cout << "K4 Graph Chromatic Number: " << k4.chromaticNumber() << std::endl;

    // For the Peterson graph, the chromatic number is 3.
    std::cout << "Peterson Graph Chromatic Number: " << peterson.chromaticNumber() << std::endl;

    return 0;
}
