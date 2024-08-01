#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <algorithm>

using namespace std;

// Directions for moving in 4 possible directions (up, down, left, right)
const vector<pair<int, int>> directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

vector<vector<int>> bfsShortestPath(vector<vector<int>>& grid, vector<vector<int>>& taxi_stands, pair<int, int> passenger) {
    int m = grid.size();
    int n = grid[0].size();
    
    queue<pair<int, int>> q;
    vector<vector<bool>> visited(m, vector<bool>(n, false));
    vector<vector<pair<int, int>>> parent(m, vector<pair<int, int>>(n, {-1, -1}));
    
    // Start BFS from the passenger's location
    q.push(passenger);
    visited[passenger.first][passenger.second] = true;
    
    while (!q.empty()) {
        auto current = q.front();
        q.pop();
        
        // Check if the current position is a taxi stand
        if (grid[current.first][current.second] == 2) {
            // Reconstruct path from taxi stand to passenger
            vector<vector<int>> path;
            while (current != passenger) {
                path.push_back({current.first, current.second});
                current = parent[current.first][current.second];
            }
            path.push_back({passenger.first, passenger.second});
            reverse(path.begin(), path.end());
            return path;
        }
        
        // Explore neighbors
        for (const auto& dir : directions) {
            int newX = current.first + dir.first;
            int newY = current.second + dir.second;
            
            // Check bounds and if the path is clear (road and not visited)
            if (newX >= 0 && newX < m && newY >= 0 && newY < n && !visited[newX][newY] && grid[newX][newY] != 1) {
                visited[newX][newY] = true;
                parent[newX][newY] = current;
                q.push({newX, newY});
            }
        }
    }
    
    // Return empty path if no taxi is reachable
    return {};
}

vector<vector<int>> findShortestPath(vector<vector<int>>& grid, vector<vector<int>>& taxi_stands, pair<int, int> passenger) {
    int m = grid.size();
    int n = grid[0].size();
    
    // Mark taxi stands in the grid as special point (value 2)
    for (const auto& taxi : taxi_stands) {
        grid[taxi[0]][taxi[1]] = 2;
    }
    
    return bfsShortestPath(grid, taxi_stands, passenger);
}

int main() {
    vector<vector<int>> grid = {
        {0, 1, 0, 0, 0},
        {0, 0, 1, 0, 0},
        {1, 0, 0, 1, 0},
        {0, 0, 0, 0, 0},
        {0, 1, 1, 0, 0}
    };
    
    vector<vector<int>> taxi_stands = {{0, 0}, {3, 4}};
    pair<int, int> passenger = {4, 4};
    
    vector<vector<int>> path = findShortestPath(grid, taxi_stands, passenger);
    
    if (!path.empty()) {
        cout << "Shortest path from taxi to passenger:" << endl;
        for (const auto& pos : path) {
            cout << "(" << pos[0] << ", " << pos[1] << ") ";
        }
        cout << endl;
    } else {
        cout << "No taxi is reachable from the passenger's location." << endl;
    }
    
    return 0;
}