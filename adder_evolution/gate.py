import random

class gate:
    type_and = 1
    type_or = 2
    type_not = 3
    type_xor = 4
    type_left = 5
    type_right = 6
    def __init__(self, type: int):
        if type not in [self.type_and, self.type_or, self.type_not, self.type_xor, self.type_left, self.type_right]:
            raise ValueError("Invalid gate type")
        self.type = type        
    def cal(self, i1: str, i2: str) -> str:
        if self.type == self.type_and:
            if i1 == i2 == "1":
                return "1"
            else:
                return "0"
        if self.type == self.type_or:
            if i1 == i2 == "0":
                return "0"
            else:
                return "1"
        if self.type == self.type_not:
            if i1 == "1":
                return "0"
            return "1"
        if self.type == self.type_xor:
            if i1 == i2 == "0" or i1 == i2 == "1":
                return "0"
            else:
                return "1"
        if self.type == self.type_left:
            if i1 == "1":
                return "1"
            else:
                return "0"
        if self.type == self.type_right:
            if i2 == "1":
                return "1"
            else:
                return "0"
    
    def newRandomGate() -> 'gate':
        return gate(random.choices([gate.type_and, gate.type_or, gate.type_not, gate.type_xor,
            gate.type_left, gate.type_right])[0])
    
    def packJSON(self):
        return self.type
    
    def unpackJSON(d) -> 'gate':
        return gate(d)