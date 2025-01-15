from typing import Dict, List
from collections import namedtuple
from copy import deepcopy

Vulnerability = namedtuple(
    "Vulnerability",
    "vulnerability source sink unsanitized_flows sanitized_flows")
UNTAINTED = 1
TAINTED = 2


class Cursor:

    def __init__(self, name: str, previous=None):
        self.name = name
        if previous is not None:
            self.state = previous.state
            self.visited = deepcopy(previous.visited)
            self.sanitizers = deepcopy(previous.sanitizers)
            self.sink = previous.sink
        else:
            self.state = UNTAINTED
            self.visited = dict()
            self.sanitizers = set()
            self.sink = name


def merge_vulnerabilities(vulns: List):
    # <source, sink> : { "unsanitized": <bool>, "sanitized": set()}
    output = dict()
    for vuln in vulns:
        if (vuln.source, vuln.sink) in output:
            entry = output[(vuln.source, vuln.sink)]
            entry["unsanitized"] = "yes" if entry[
                "unsanitized"] == "yes" or vuln.unsanitized_flows == "yes" else "no"
            flows = set()
            flows.add(vuln.sanitized_flows)
            entry["sanitized"] = entry["sanitized"].union(flows)
        else:
            flows = set()
            flows.add(vuln.sanitized_flows)
            output[(vuln.source, vuln.sink)] = {
                "vulnerability": vuln.vulnerability,
                "unsanitized": vuln.unsanitized_flows,
                "sanitized": flows
            }

    vulns.clear()
    vulns.extend(
        Vulnerability(value["vulnerability"], key[0], key[1],
                      value["unsanitized"],
                      list(filter(lambda t: len(t) > 0, value["sanitized"])))
        for (key, value) in output.items())


def find_vulnerabilities(pattern: Dict, states: List[Dict], depth=2):

    def find_vulnerability(graph: Dict):
        is_scalar = lambda x: "__SCALAR__" in x
        is_function = lambda x: x[0] != '$'
        is_variable = lambda x: not is_scalar(x) and not is_function(x)
        vulns = set()
        sources = set(pattern["sources"])
        sanitizers = set(pattern["sanitizers"])
        uninitialized = set(filter(lambda n: "__UNINITIALIZED__" in graph[n], graph.keys()))
        relevant = set(pattern["sources"]).union(pattern["sanitizers"]).union(uninitialized).union(pattern["sinks"])
        visited = dict()

        # for node in pattern["sinks"]:
        #     visited[node] = visited.get(node, set((node,)))

        # queue = [Cursor(node) for node in pattern["sinks"]] 
        for sink in pattern["sinks"]:
            queue = [Cursor(sink)]
            visited = dict()
            visited[sink] = visited.get(sink, set((sink,)))
            while queue != []:
                current = queue.pop()
                neighbors = graph.get(current.name, set())
                if current.name in relevant:
                    visited[current.name].add(current.name)
                if "__UNINITIALIZED__" in neighbors and is_variable(
                        current.name) and current.name != sink:
                    # not declarated
                    vulns.add(
                        Vulnerability(
                            pattern["vulnerability"], current.name, current.sink,
                            "yes" if len(current.sanitizers) == 0 else "no",
                            tuple(current.sanitizers)))
                if current.name in sources:
                    # add to list of vulns
                    vulns.add(
                        Vulnerability(
                            pattern["vulnerability"], current.name, current.sink,
                            "yes" if len(current.sanitizers) == 0 else "no",
                            tuple(current.sanitizers)))
                elif current.name in sanitizers:
                    current.sanitizers.add(current.name)

                neighbors = list(map(lambda x: Cursor(x, current), neighbors))
                for n in neighbors:
                    if pattern["implicit"] == "no" and "__anon__" in n.name:
                        continue
                    if "__SCALAR__" in n.name:
                        continue
                    if n.name == "__UNINITIALIZED__":
                        continue
                    n.visited[current.name] = n.visited.get(current.name,
                                                            0) + 1

                    if visited.get(n.name) != visited.get(current.name):
                        visited[n.name] = visited.get(n.name, set()).union(
                            visited[current.name])
                        queue.append(n)
                    elif n.name in relevant and n.visited.get(n.name, 0) <= depth:
                        queue.append(n)
        return vulns

    vulnerabilities = []
    for graph in states:
        if pattern["implicit"] == "no":
            g = dict()
            for k in graph:
                if "__anon__" in k:
                    pass
                else:
                    g[k] = deepcopy(graph[k])
            for (k, v) in g.items():
                g[k] = set(filter(lambda x: "__anon__" not in x, v))
        else:
            g = graph
        vulnerabilities.extend(find_vulnerability(g))
        # aaa = find_vulnerability(pattern, graph)
        x = 12

    merge_vulnerabilities(vulnerabilities)
    return vulnerabilities
