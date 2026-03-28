#!/usr/bin/env python3
"""deadlock_detect - Deadlock detection using wait-for graph."""
import sys
from collections import defaultdict
class DeadlockDetector:
    def __init__(s):s.waits_for=defaultdict(set);s.holds=defaultdict(set)
    def acquire(s,process,resource):s.holds[process].add(resource)
    def wait(s,process,resource):
        holder=s._holder(resource)
        if holder and holder!=process:s.waits_for[process].add(holder)
    def release(s,process,resource):
        s.holds[process].discard(resource)
        s.waits_for.pop(process,None)
        for p in list(s.waits_for):s.waits_for[p].discard(process)
    def _holder(s,resource):
        for p,resources in s.holds.items():
            if resource in resources:return p
        return None
    def detect(s):
        visited=set();path=set()
        def dfs(node):
            visited.add(node);path.add(node)
            for neighbor in s.waits_for.get(node,[]):
                if neighbor in path:return list(path)
                if neighbor not in visited:
                    cycle=dfs(neighbor)
                    if cycle:return cycle
            path.discard(node);return None
        for node in list(s.waits_for):
            if node not in visited:
                cycle=dfs(node)
                if cycle:return cycle
        return None
if __name__=="__main__":
    dd=DeadlockDetector()
    dd.acquire("P1","R1");dd.acquire("P2","R2");dd.acquire("P3","R3")
    dd.wait("P1","R2");dd.wait("P2","R3");dd.wait("P3","R1")
    cycle=dd.detect()
    if cycle:print(f"Deadlock detected! Cycle: {' → '.join(cycle)}")
    else:print("No deadlock")
