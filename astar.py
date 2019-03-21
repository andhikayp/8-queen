import heapq, copy
import queue
import random

class Grid():
    def __init__(self, n: int, grid: list = []):
        if grid == []:
            grid = [[0] * n for i in range(n)]

        self.n = n
        self.grid = grid
        self.hash = str(self.grid)

    @classmethod
    def random(cls, n: int):
        grid = [[0] * n for i in range(n)]
        for row in grid:
            row[random.randint(0, n-1)] = 1
        return cls(n, grid)

    def __str__(self):
        ss = ''
        for row in self.grid:
            for item in row:
                ss += 'O ' if item == 1 else '+ '

            ss += '\n'

        return ss

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def heuristic(self) -> int:
        her = 0
        grid = self.grid
        n = self.n
        for r, row in enumerate(grid):
            pos = row.index(1)
            her_sum = 0
            for i in range(n):
                # mengecek adakah yang saling serang
                if(grid[i][pos] == 1 and i!=r): her_sum +=1
                if(pos-i>=0 and r-i>=0 and i!=0 and grid[r-i][pos-i] == 1): her_sum+=1
                if(pos+i<n and r+i< n  and i!=0 and grid[r+i][pos+i] == 1): her_sum+=1
                if(pos+i<n and r-i>=0  and i!=0 and grid[r-i][pos+i] == 1): her_sum+=1
                if(pos-i>=0 and r+i<n  and i!=0 and grid[r+i][pos-i] == 1): her_sum+=1
            her += her_sum
        return her

    def move(self, i: int , dir: str):
        # memindahkan berdasarkan left right setiap baris
        state = copy.deepcopy(self.grid)
        pos = state[i].index(1)
        n = len(state)
        if(dir == 'l' and pos-1 >= 0):
            state[i][pos-1], state[i][pos] = state[i][pos], state[i][pos-1]
            return Grid(self.n, state)
        if(dir == 'r' and pos+1 < n):
            state[i][pos+1], state[i][pos] = state[i][pos], state[i][pos+1]
            return Grid(self.n, state)

        return self

# class queen
class QueenProblem():
    # generate kosong n x n
    def __init__(self, n: int):
        self.n = n
        self.grid = Grid.random(n)

    def search_astar(self):
        visited = set()
        parent = {}
        gn = {self.grid.hash: 0}                        # g(n) = step = 1
        fn = {self.grid.hash: self.grid.heuristic()}     # f(n) = heuristic(current) + g(n)

        pq = []                                         #piority queue

        heapq.heappush(pq, (fn[self.grid.hash], self.grid)) #push initial state dan fn
        count = 0
        print(self.grid)
        while pq:
            current = heapq.heappop(pq)[1]
            count+=1
            n = self.n
            # Jika mencapai goal
            if current.heuristic() ==  0:
                print ("SUCCESS at count ", count, '\n')
                path = []
                cr = current.hash
                while cr in parent:
                    path.append(parent[cr][1:])
                    cr = parent[cr][0]
                return path[::-1]                           #pass list of parent dari solusi

            visited.add(current.hash)
            for i in range(n):
                for l in ["l", "r"]:
                    neighbor = current.move(i,l)

                    if neighbor.hash in visited:
                        continue

                    gn_temp = gn[current.hash] + 1      #tambahkan gn
                    fn_temp = gn_temp + neighbor.heuristic()     #akumulasi fn
                    if (neighbor.hash in fn and fn_temp < fn[neighbor.hash]) or (neighbor.hash not in fn):      #apabila belum ada atau fn yang sudah ada kurang dari sekarang
                        if neighbor.hash not in fn:
                            heapq.heappush(pq, (fn_temp, neighbor))
                        parent[neighbor.hash] = [current.hash, neighbor, i, l]
                        gn[neighbor.hash] = gn_temp
                        fn[neighbor.hash] = fn_temp

        return None

    def search_bfs(self):
        visited = set()
        parent = {}
        gn = {self.grid.hash: 0}
        fn = {self.grid.hash: self.grid.heuristic()}

        pq  = queue.Queue()

        pq.put(self.grid)
        count = 0
        print(self.grid)
        while pq:
            current = pq.get()
            count+=1
            n = self.n
            # Jika mencapai goal
            if current.heuristic() ==  0:
                print ("SUCCESS at count ", count, '\n')
                path = []
                cr = current.hash
                while cr in parent:
                    path.append(parent[cr][1:])
                    cr = parent[cr][0]
                return path[::-1]

            visited.add(current.hash)
            for i in range(n):
                for l in ["l", "r"]:
                    neighbor = current.move(i,l)
                    if neighbor.hash not in visited:
                        pq.put(neighbor)
                        visited.add(neighbor.hash)
                        parent[neighbor.hash] = [current.hash, neighbor, i, l]
        return None

def main():
    qq = QueenProblem(8)

    print("A*")
    sol = qq.search_astar()
    for i, grid in enumerate(sol, 1):
        print("STEP #{:03d} ({} {})".format(i, grid[1]+1, grid[2].upper()))
        print(grid[0])

    print("BFS")
    sol = qq.search_bfs()
    for i, grid in enumerate(sol, 1):
        print("STEP #{:03d} ({} {})".format(i, grid[1]+1, grid[2].upper()))
        print(grid[0])

if __name__ == '__main__':
    main()
