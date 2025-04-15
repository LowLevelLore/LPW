import random
from typing import List, Tuple, Optional

def generate_maze(rows: int, cols: int, use_predefined: bool = False) -> List[List[int]] | List[List[str]]:
    if use_predefined:
        maze = [
                [0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
                [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
    else:
        maze = [[random.choices([0, 1], weights=[0.7, 0.3], k=1)[0] for _ in range(cols)] for _ in range(rows)]
        maze[0][0] = 0  # Start point
        maze[rows - 1][cols - 1] = 0  # End point
    return maze

def print_maze(maze: List[List[int]] | List[List[str]]) -> None:
    for row in maze:
        print(" ".join(map(str, row)))

def find_path(maze: List[List[int]] | List[List[str]]) -> Optional[List[Tuple[int, int]]]:
    rows, cols = len(maze), len(maze[0])
    start, end = (0, 0), (rows - 1, cols - 1)
    path = []
    visited = set()

    def dfs(x: int, y: int) -> bool:
        if (x, y) == end:
            path.append((x, y))
            return True
        
        if (x < 0 or x >= rows or y < 0 or y >= cols or
                maze[x][y] == 1 or (x, y) in visited):
            return False
        
        visited.add((x, y))
        path.append((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  
            if dfs(x + dx, y + dy):
                return True

        path.pop()
        return False

    if dfs(*start):
        return path
    return None

def main() -> None:
    rows, cols = 10, 10  
    maze = generate_maze(rows, cols, False)

    print("Generated Maze:")
    print_maze(maze)

    print("\nFinding path...")
    path = find_path(maze)

    if path:
        print("PATH:")
        for coords in path:
            maze[coords[0]][coords[1]] = "#"
        print_maze(maze)
    else:
        print("No path exists.")

if __name__ == "__main__":
    main()
