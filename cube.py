import random
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from magiccube.cube import Cube
from magiccube.cube_move import CubeMove, CubeMoveType

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())

    def get_possible_moves(self):
        return [CubeMove(move_type) for move_type in CubeMoveType]

    def select_child(self):
        return max(self.children, key=lambda c: c.uct_value())

    def expand(self):
        move = random.choice([m for m in self.get_possible_moves() if m not in [c.move for c in self.children]])
        new_state = Cube(self.state.size)
        new_state.set(str(self.state))
        new_state.rotate([move])
        child = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.value += result

    def uct_value(self, c=1.414):
        if self.visits == 0:
            return float('inf')
        return self.value / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def mcts_search(cube_state, iterations, max_depth):
    root = MCTSNode(cube_state)
    for _ in range(iterations):
        node = root
        depth = 0
        
        # Selection
        while node.is_fully_expanded() and not node.state.is_done() and depth < max_depth:
            node = node.select_child()
            depth += 1

        # Expansion
        if not node.state.is_done() and depth < max_depth:
            node = node.expand()

        # Simulation
        state = Cube(node.state.size)
        state.set(str(node.state))
        while not state.is_done() and depth < max_depth:
            move = random.choice(node.get_possible_moves())
            state.rotate([move])
            depth += 1

        # Backpropagation
        result = 1 if state.is_done() else 0
        while node:
            node.update(result)
            node = node.parent

    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move, best_child.visits

def solve_cube_parallel(cube, num_processes, iterations_per_move, max_depth, max_moves):
    moves = []
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for _ in range(max_moves):
            if cube.is_done():
                break

            futures = [executor.submit(mcts_search, cube, iterations_per_move, max_depth) 
                       for _ in range(num_processes)]
            
            best_move, _ = max(as_completed(futures), key=lambda f: f.result()[1]).result()
            cube.rotate([best_move])
            moves.append(best_move)

    return moves

def main():
    cube_size = 3  
    scramble_moves = 20
    num_processes = 4
    iterations_per_move = 1000
    max_depth = 20
    max_moves = 100

    cube = Cube(cube_size)
    cube.scramble(scramble_moves)
    print("Scrambled cube:")
    print(cube)

    start_time = time.time()
    solution = solve_cube_parallel(cube, num_processes, iterations_per_move, max_depth, max_moves)
    end_time = time.time()

    print(f"\nSolution found in {len(solution)} moves:")
    print(" ".join(str(move) for move in solution))
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")

    print("\nSolved cube:")
    print(cube)

if __name__ == "__main__":
    main()