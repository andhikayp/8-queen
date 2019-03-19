import heapq, copy
import queue
import random

def strfy(ll):
    return "".join(("".join for y in x) for x in ll)

def heuristic(grid) -> int:
    her = 0
    n = len(grid)
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
        # print(r,her_sum)
        her += her_sum
    # print(her)
    return her

def move(grid, i: int , dir: str) -> list(list()):
    # memindahkan berdasarkan left right setiap baris 
    state = copy.deepcopy(grid)
    pos = state[i].index(1)
    n = len(state)
    if(dir == 'l' and pos-1 >= 0):
        state[i][pos-1], state[i][pos] = state[i][pos], state[i][pos-1]
        return state
    if(dir == 'r' and pos+1 < n):
        state[i][pos+1], state[i][pos] = state[i][pos], state[i][pos+1]
        return state
    return state

# class queen
class QuuenProblem():
    # generate kosong n x n 
    def __init__(self, n: int):
        self.n = n
        self.grid = [[0] * n for i in range(n)]
    # generate initial state n x n setiap baris random
    def generate_random(self):
        for row in self.grid:
            row[random.randint(0, self.n-1)] = 1

    def search_astar(self):
        visited = set()
        parent = {}
        gn = {str(self.grid): 0}                        # g(n) = step = 1
        fn = {str(self.grid): heuristic(self.grid)}     # f(n) = heuristic(current) + g(n)

        pq = []                                         #piority queue

        heapq.heappush(pq, (fn[str(self.grid)], self.grid)) #push initial state dan fn
        count = 0
        self.print()
        while pq:
            neighbor = {}                       # set dari tetangga/anak dari current state
            current = heapq.heappop(pq)[1] 
            count+=1
            n = self.n
            # Jika mencapai goal
            if heuristic(current) ==  0:
                print ("SUCCESS at count "+str(count))
                path = []
                while str(current) in parent:
                    path.append(str(current))
                    current = eval(parent[str(current)])
                return path[::-1]                           #pass list of parent dari solusi

            visited.add(str(current))
            pindah = ["l","r"]                  #pindah perbaris berdasarkan left right
            for i in range(n):
                for l in pindah:
                    # print(str(i)+" "+l)
                    neighbor = move(current,i,l)
                    if str(neighbor) in visited:
                        # print(str(i)+" "+str(l)+" isvisited")
                        continue
                    gn_temp = gn[str(current)] + 1      #tambahkan gn
                    # print(neighbor)
                    fn_temp = gn_temp + heuristic(neighbor)     #akumulasi fn
                    if str(neighbor) in fn and fn_temp < fn[str(neighbor)] or str(neighbor) not in fn:      #apabila belum ada atau fn yang sudah ada kurang dari sekarang
                        if str(neighbor) not in fn:
                            heapq.heappush(pq, (fn_temp,neighbor))
                        parent[str(neighbor)] = str(current)
                        gn[str(neighbor)] = gn_temp
                        fn[str(neighbor)] = fn_temp

        return None
    
    def search_bfs(self):
        visited = set()
        parent = {}
        gn = {str(self.grid): 0}
        fn = {str(self.grid): heuristic(self.grid)}

        pq  = queue.Queue() 

        pq.put(self.grid)
        count = 0
        self.print()
        while pq:
            neighbor = []
            current = pq.get()
            count+=1
            n = self.n
            # Jika mencapai goal
            if heuristic(current) ==  0:
                print ("SUCCESS at count "+str(count))
                path = []
                while str(current) in parent:
                    path.append(str(current))
                    current = eval(parent[str(current)])
                return path[::-1]

            visited.add(str(current))
            pindah = ["l","r"]
            # print ("count "+str(count))
            for i in range(n):
                for l in pindah:
                    neighbor = move(current,i,l)
                    if str(neighbor) not in visited:
                        pq.put(neighbor)
                        visited.add(str(neighbor))
                        parent[str(neighbor)] = str(current)
        return None

    def print(self):
        for row in self.grid:
            print(row)



def main():
    qq = QuuenProblem(8)
    qq.generate_random()
    # qq.heuristic()
    # qq.print()
    print("A*")
    sol = qq.search_astar()
    for i in range(len(sol)):
        print("Step "+str(i+1))
        curr = eval(sol[i])
        for row in range(len(curr)):
            print(curr[row])
    print()
    print("BFS")
    sol = qq.search_bfs()
    for i in range(len(sol)):
        print("Step "+str(i+1))
        curr = eval(sol[i])
        for row in range(len(curr)):
            print(curr[row])

if __name__ == '__main__':
    main()