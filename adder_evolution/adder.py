from typing import List, Mapping
import random
from adder_evolution.gate import gate

class adder:
    digits_field_name = "digits"
    gates_feild_name = "gates"
    connection_field_name = "connections"
    score_field_name = "score"
    
    def __init__(self, digits: int, gates: List[gate], connections: List[int]):
        self.digits = digits
        self.gates = gates
        # Connection's index is output of adder and inputs of gates
        # For example, digits = 2, gates.len = 3
        # There will be 3 output of adder, and 6 inputs of gates
        # So the len of connections should be 9
        # The value of connections means output of adder or inputs of gates is connected with input of adder or output of gates
        # For example, digits = 2, gates.len = 3
        # There will be 4 input of adder, and 3 outputs of gates
        # So the valid value is [0, 7], 0 means connected with nothing, [1, 4] means connected with inputs of addr, [5, 7] means connected with outputs of gates
        self.connections = connections
        self.score = 0
        
    def dfs(self, cache: List[str], input: str, index: int, history: Mapping[int,bool]) -> str:
        # Index is output of adder or input of gates
        # [0, digits] is output of adder, digits + 1 total
        # [digits + 1, digits + 2 * len(gates)] is input of of gates
        # If it connect to nothing, return 0
        if self.connect_to_nothing(index):
            return "0"
        # If it is already calculated, return cache
        if cache[index] != "":
            return cache[index]
        # Parent is what connect to it
        parent = self.connections[index]
        # If source is input of addr, return input directly
        if parent <= self.digits * 2:
            ret = input[parent-1]
            cache[index] = ret
            return ret
        # If parent is output of gate, cal it recursive
        # First, get index of source gate's input
        # If digits is 4, source is 0, lets calculate each index mean
        # 0 means nothing, 1-4 means input, 5 and 6 means input of first gate
        gate_index = parent - self.digits * 2 - 1
        if gate_index in history:
            return "-1"
        source_index1 = self.digits + 1 + gate_index * 2
        source_index2 = source_index1 + 1
        history[gate_index] = True
        v1 = self.dfs(cache, input, source_index1, history)
        v2 = self.dfs(cache, input, source_index2, history)
        del history[gate_index]
        out = "-1"
        if v1 != "-1" and v2 != "-1":
            out = self.gates[gate_index].cal(v1, v2)
        cache[index] = out
        return out

    def connect_to_nothing(self, index):
        return len(self.connections) < index + 1 or self.connections[index] == 0 or self.connections[index] > self.digits * 2 + len(self.gates)
        
        
    def cal(self, i1: int, i2: int) -> int:
        # Format two input into a string
        input = format(i1, f'0{self.digits}b') + format(i2, f'0{self.digits}b')
        # Prepare list to fill in result
        cache = ["" for _ in range(self.digits + 1 + len(self.gates) * 2)]
        res = ""
        # Iterate through digits+1, to get all result
        for i in range(self.digits + 1):
            r = self.dfs(cache, input, i, {})
            # If return -1, means there is loop, the result is invalid
            if r == "-1":
                return -1
            res += r
        return int(res, 2)
    
    def challenge(self, challengs: List[List[int]]):
        res = 0
        for c in challengs:
            if self.cal(c[0], c[1]) == c[2]:
                res += 1
        self.score = res
        
    def get_score(self) -> int:
        return self.score
    
    def involute(self, rate: float) -> 'adder':
        new_one = adder(self.digits, self.gates.copy(), self.connections.copy())
        
        # Involute gates
        fewer_rate = rate * rate
        base = 1 - 2 * fewer_rate
        delta_gate = random.choices([-1, 0, 1], [fewer_rate, base, fewer_rate])[0]
        
        if delta_gate > 0:
            new_one.gates.append(gate.newRandomGate())
        elif delta_gate < 0 and len(new_one.gates) > 0:
            del new_one.gates[random.randint(0, len(new_one.gates) - 1)]
            
        # Ensure connetions length
        count_connections = len(new_one.connections)
        len_connections = new_one.digits + 2 * len(new_one.gates)
        if count_connections < len_connections:
            new_one.connections += [0] * (len_connections - count_connections)
        elif count_connections > len_connections:
            new_one.connections = new_one.connections[:len_connections]
            
        # Involute connections
        max_val = 2 * new_one.digits + len(new_one.gates)
        involution_rate = rate
        while random.random() < involution_rate:
            involution_rate *= involution_rate
            new_one.connections[random.randint(0, len_connections-1)] = random.randint(0, max_val)
        return new_one
    
    def packJSON(self):
        gates = []
        for g in self.gates:
            gates.append(gate.packJSON(g))
        return {
            self.digits_field_name: self.digits,
            "gate_len": len(self.gates),
            self.gates_feild_name: gates,
            self.connection_field_name: self.connections,
            self.score_field_name: self.score,
        }
    
    def unpackJSON(self, d) -> 'adder':
        digits = d[self.digits_field_name]
        gates = []
        for gate_data in d[self.gates_feild_name]:
            gates.append(gate.unpackJSON(gate_data))
        connections = d[self.connection_field_name]
        a =  adder(digits, gates, connections)
        a.score = d[self.score_field_name]
        return a