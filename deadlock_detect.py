#!/usr/bin/env python3
"""Deadlock detection using wait-for graph."""
import sys
from collections import defaultdict
def detect_deadlock(wait_for):
    def dfs(node,visited,stack):
        visited.add(node);stack.add(node)
        for neighbor in wait_for.get(node,[]):
            if neighbor not in visited:
                cycle=dfs(neighbor,visited,stack)
                if cycle is not None: return [node]+cycle
            elif neighbor in stack:
                return [node,neighbor]
        stack.remove(node);return None
    visited=set()
    for node in wait_for:
        if node not in visited:
            cycle=dfs(node,visited,set())
            if cycle: return cycle
    return None
def bankers(available,max_need,allocation):
    n=len(allocation);m=len(available)
    need=[[max_need[i][j]-allocation[i][j] for j in range(m)] for i in range(n)]
    work=list(available);finish=[False]*n;safe=[]
    for _ in range(n):
        for i in range(n):
            if not finish[i] and all(need[i][j]<=work[j] for j in range(m)):
                for j in range(m): work[j]+=allocation[i][j]
                finish[i]=True;safe.append(i)
                break
    return safe if all(finish) else None
def main():
    print("Wait-for graph deadlock detection:")
    wf={"P1":["P2"],"P2":["P3"],"P3":["P1"]}
    cycle=detect_deadlock(wf)
    print(f"  {wf} → {'Deadlock: '+str(cycle) if cycle else 'No deadlock'}")
    wf2={"P1":["P2"],"P2":["P3"],"P3":[]}
    cycle2=detect_deadlock(wf2)
    print(f"  {wf2} → {'Deadlock: '+str(cycle2) if cycle2 else 'No deadlock'}")
    print("\nBanker's algorithm:")
    avail=[3,3,2]
    max_n=[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
    alloc=[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
    safe=bankers(avail,max_n,alloc)
    print(f"  Safe sequence: {safe}" if safe else "  UNSAFE state!")
if __name__=="__main__": main()
