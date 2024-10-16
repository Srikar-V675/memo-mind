---
creation: 2024-10-05 11:46
source: "[[graphs]]"
atlas: "[[04-Atlas/DSA]]"
type: literature
dg-publish: true
---
# Graph DFS

## Captures
Just like [[tree depth traversals]], graph DFS also works very similarly and is again a [[Recursion]] problem since at every single step we make the same operation and if we reach the base case (which is all neighbouring nodes are visited) then we backtrack and try to find an other route. 

DFS sticks to one path and follows the structure until it ends and then backtrack to find another path.

> [!tldr]+
> **DFS algorithm is more like a solving a maze, where we pick one path and if we reach a dead end then we back track and check another path. This repeats until we have found the exit or we have run out of paths.**
> 

![[graphs depth first search.png]]

Base case of a DFS [[graphs]] [[Recursion]] is when every single neighbour of a node is visited or there are no outgoing edges. 

Basic steps of DFS in [[graphs]] are:
1. add the node to the top of the [[Stack]].
2. Mark it as visited and check its neighbouring nodes. 
3. Add one of the non-visited neighbouring nodes to the stack and repeat from step-2. If there are no non-visited neighbouring nodes pop it out of the [[Stack]]. 

### Time Complexity
*Very similar to [[graphs breadth first search]] complexity*. Since ultimately we are visiting all the vertices and all its edges at-least once. 
![[graphs breadth first search#Time Complexity]]


> [!important]+
> T**he power of DFS on a graph is that it helps us check if a path exists between `node x` and `node y`. But it doesn't guarantee us the shortest path (could also give us the longest path) but it just tells us if a path exists.** 

## Code 

### [[Matrix]] 
```python
num_rows, num_cols = len(matrix), len(matrix[0])
def get_neighbours(coord): 
	row, col = coord 
	directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
	neighbours = [] 
	for direction in directions: 
		next_row = row + direction[0] 
		next_col = col + direction[1] 
		if 0 <= next_row < num_rows and 0 <= next_col < num_cols:
			neighbours.append((next_row, next_col)) 
	return neighbours

def dfs(node, visited):
	if node in visited: 
		return 
	visited.add(node)
	for neighbour in get_neighbours(node):
		dfs(neighbour, visited)

visited = set()
dfs(starting_node, visited)
```

![[graphs breadth first search#Other Representations]]

### Iterative 
```python
stack = deque([starting_node])
visited = set([starting_node])

while stack:
	node = stack.pop()
	for neighbour in get_neighbours(node):
		if neighbour in visited:
			continue
		visited.add(neighbour)
		stack.append(neighbour)
```

---
## Related Notes
[[graphs]]
[[graphs breadth first search]]
[[Stack]]
[[tree depth traversals]]
[[trees]]
[[graph representations]]
[[Recursion]]

## References(links)
[Deep Dive Through A Graph: DFS Traversal | by Vaidehi Joshi | basecs | Medium](https://medium.com/basecs/deep-dive-through-a-graph-dfs-traversal-8177df5d0f13)