from typing import List, Mapping
import random
import uuid
import copy
import os
from adder_evolution.gate import gate
import pygraphviz as pgv

class connect:
    type_none = 0
    type_input1 = 1
    type_input2 = 2
    type_gate = 3
    type_output = 4
    
    type_field_name = "type"
    index_field_name = "index"
    
    def __init__(self, type: int, index: int):
        self.type = type
        self.index = index
        
    def get_type(self) -> int:
        return self.type
    
    def get_index(self) -> int:
        return self.index
    
    def set_index(self, index: int):
        self.index = index
        
    def packJSON(self):
        return {
            connect.type_field_name: self.type,
            connect.index_field_name: self.index,
        }
        
    def unpackJSON(d) -> "connect":
        return connect(d[connect.type_field_name], d[connect.index_field_name])
        
        
    def __hash__(self):
        return hash((self.type, self.index))

    def __eq__(self, other):
        if isinstance(other, connect):
            return (self.type, self.index) == (other.type, other.index)
        return False

class adder:
    gates_feild_name = "gates"
    gate_connection_field_name = "gate_connections"
    output_connection_field_name = "output_connections"
    score_field_name = "score"
    generation_field_name = "generation"
    name_field_name = "name"
    parent_field_name = "parent"
    
    def __init__(self, gates: List[gate], gate_connections: List[List[connect]],
                 output_connections: List[connect]):
        self.gates = gates
        self.gate_connections = gate_connections
        self.output_connections = output_connections
        self.score = 0
        self.name = str(uuid.uuid4())
        self.parent = ""
        self.generation = 0
        
    def dfs(self, input1: str, input2: str, conn: connect, history: Mapping[int,bool]) -> str:
        if self.connect_to_nothing(len(input1), len(input2), conn):
            return "0"
        elif conn.get_type() == connect.type_input1:
            return input1[-1 * conn.get_index() - 1]
        elif conn.get_type() == connect.type_input2:
            return input2[-1 * conn.get_index() - 1]
        elif conn.get_type() == connect.type_gate:
            index = conn.get_index()
            if index in history:
                return "-1"
            history[index] = True
            i1_conn = self.gate_connections[index][0]
            i2_conn = self.gate_connections[index][1]
            v1 = self.dfs(input1, input2, i1_conn, history)
            v2 = self.dfs(input1, input2, i2_conn, history)
            del history[index]
            out = "-1"
            if v1 != "-1" and v2 != "-1":
                out = self.gates[index].cal(v1, v2)
            return out

    def connect_to_nothing(self, input1_len: int, input2_len: int, conn: connect) -> bool:
        index = conn.get_index()
        if conn.get_type() == connect.type_none:
            return True
        elif conn.get_type() == connect.type_input1:
            if index < 0 or index >= input1_len:
                return True
        elif conn.get_type() == connect.type_input2:
            if index < 0 or index >= input2_len:
                return True
        elif conn.get_type() == connect.type_gate:
            if index < 0 or index >= len(self.gates):
                return True
        return False
        
        
    def cal(self, i1: int, i2: int) -> int:
        # Format two input into a string
        if len(self.output_connections) == 0:
            return 0
        input1 = format(i1, f'0b')
        input2 = format(i2, f'0b')
        
        res = ""
        # Iterate through output
        for conn in self.output_connections:
            r = self.dfs(input1, input2, conn, {})
            if r == "-1":
                return -1
            res = r + res
        return int(res, 2)
    
    def challenge(self, challengs: List[List[int]]):
        res = 0
        for c in challengs:
            if self.cal(c[0], c[1]) == c[2]:
                res += 1
        self.score = res
        
    def get_score(self) -> int:
        return self.score
    
    def count_gates(self) -> int:
        return len(self.gates)
    
    def get_generation(self) -> int:
        return self.generation
    
    def mutate(self, rate: float) -> 'adder':
        new_one = adder(self.gates.copy(), copy.deepcopy(self.gate_connections), copy.deepcopy(self.output_connections))
        new_one.parent = self.name
        new_one.generation = self.generation + 1
        
        # Mutate
        while random.random() < rate:
            if rate >= 0.99:
                rate = 0.99
            rate *= rate
            r = random.random()
            # Add gate
            if r < 0.1:
                new_one.gates.append(gate.newRandomGate())
                new_one.gate_connections.append([self.new_random_connect(), self.new_random_connect()])
            # Del gate
            elif r < 0.2:
                if len(new_one.gates) > 0:
                    del_index = random.randint(0, len(new_one.gates) - 1)
                    del new_one.gates[del_index]
                    del new_one.gate_connections[del_index]
                    for conn_pair in new_one.gate_connections:
                        if conn_pair[0].get_type() == connect.type_gate:
                            i0 = conn_pair[0].get_index()
                            if i0 >= del_index:
                                conn_pair[0].set_index(i0-1)
                        if conn_pair[1].get_type() == connect.type_gate:
                            i1 = conn_pair[1].get_index()
                            if i1 >= del_index:
                                conn_pair[1].set_index(i1-1)
                    for conn in new_one.output_connections:
                        if conn.get_type() == connect.type_gate:
                            i = conn.get_index()
                            if i >= del_index:
                                conn.set_index(i-1)
            # Alter gate type
            elif r < 0.3:
                if len(new_one.gates) > 0:
                    alter_index = random.randint(0, len(new_one.gates) - 1)
                    new_one.gates[alter_index] = gate.newRandomGate()
            # Alter connection of gates
            elif r < 0.8:
                if len(new_one.gate_connections) > 0:
                    alter_index = random.randint(0, len(new_one.gate_connections) - 1)
                    left_right = random.randint(0,1)
                    new_one.gate_connections[alter_index][left_right] = self.new_random_connect()
            else:
                if len(new_one.output_connections) > 0:
                    alter_index = random.randint(0, len(new_one.output_connections) - 1)
                    new_one.output_connections[alter_index] = self.new_random_connect()
        
        return new_one
    
    def packJSON(self):
        gates = []
        gate_connections = []
        output_connections = []
        for g in self.gates:
            gates.append(g.packJSON())
        for c in self.gate_connections:
            gate_connections.append([c[0].packJSON(), c[1].packJSON()])
        for c in self.output_connections:
            output_connections.append(c.packJSON())
        return {
            self.name_field_name: self.name,
            self.parent_field_name: self.parent,
            self.generation_field_name: self.generation,
            self.score_field_name: self.score,
            "gate_len": len(self.gates),
            self.gates_feild_name: gates,
            self.gate_connection_field_name: gate_connections,
            self.output_connection_field_name: output_connections,
        }
    
    def unpackJSON(d) -> 'adder':
        gates = []
        gate_connections = []
        output_connections = []
        for gate_data in d[adder.gates_feild_name]:
            gates.append(gate.unpackJSON(gate_data))
        for conn_data in d[adder.gate_connection_field_name]:
            gate_connections.append([connect.unpackJSON(conn_data[0]), connect.unpackJSON(conn_data[1])])
        for conn_data in d[adder.output_connection_field_name]:
            output_connections.append(connect.unpackJSON(conn_data))
        a =  adder(gates, gate_connections, output_connections)
        a.score = d[adder.score_field_name]
        a.generation = d[adder.generation_field_name]
        a.name = d[adder.name_field_name]
        a.parent = d[adder.parent_field_name]
        return a
    
    def draw(self, output_path: str=""):
        G = pgv.AGraph(directed=True)
        output_len = len(self.output_connections)
        for i in range(output_len-1):
            G.add_node(self.get_node_name(connect.type_input1, i), color="red")
        for i in range(output_len-1):
            G.add_node(self.get_node_name(connect.type_input2, i), color="orange")
        for i in range(len(self.gates)):
            G.add_node(self.get_node_name(connect.type_gate, i), color="blue")
        for i in range(output_len):
            G.add_node(self.get_node_name(connect.type_output, i), color="green")
        for i, conn_pair in enumerate(self.gate_connections):
            for ci, conn in enumerate(conn_pair):
                if self.connect_to_nothing(output_len-1, output_len-1, conn):
                    continue
                label = "left"
                if ci == 1:
                    label = "right"
                G.add_edge(self.get_node_name(conn.get_type(), conn.get_index()), self.get_node_name(connect.type_gate, i), label=label)
        for i in range(output_len):
            conn = self.output_connections[i]
            if self.connect_to_nothing(output_len-1, output_len-1, conn):
                    continue
            G.add_edge(self.get_node_name(conn.get_type(), conn.get_index()), self.get_node_name(connect.type_output, i))
        G.layout("dot")
        if output_path == "":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(current_dir, '../save')
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, f"[{self.generation}]{self.name}.png")
        G.draw(file_path)
        
        
    def get_node_name(self, type: int, index: int):
        if type == connect.type_input1:
            return f"input1[{index}]"
        elif type == connect.type_input2:
            return f"input2[{index}]"
        elif type == connect.type_gate:
            return f"gate[{index}]({self.gates[index].get_type_desc()})"
        elif type == connect.type_output:
            return f"output[{index}]"
        else:
            return "unknown"
        
    def ensure_digits(self, digits: int):
        dest = digits + 1
        if len(self.output_connections) >= dest:
            self.output_connections = self.output_connections[:dest]
        else:
            for _ in range(dest - len(self.output_connections)):
                self.output_connections.append(self.new_random_connect())
                
    def new_random_connect(self) -> connect:
        gate_len = len(self.gates)
        output_len = len(self.output_connections)
        n = random.random()
        if n < 0.25:
            return connect(connect.type_none, 0)
        elif n < 0.5:
            return connect(connect.type_input1, random.randint(0, max(0,output_len-1)))
        elif n < 0.75:
            return connect(connect.type_input2, random.randint(0, max(0,output_len-1)))
        else:
            return connect(connect.type_gate, random.randint(0, max(0,gate_len-1)))