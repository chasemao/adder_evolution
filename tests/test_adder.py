import unittest
from adder_evolution.gate import gate
from adder_evolution.adder import adder

class TestAdder(unittest.TestCase):

    def test_simple_addition(self):
        # Test simple addition without any gates
        g = []
        connections = [1, 2, 3]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("01",2), int("10",2)), int("011",2))
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("100",2))

    def test_addition_with_and_gate(self):
        # Test addition with an AND gate
        g = [gate(gate.type_and)]
        connections = [1, 2, 5, 2, 3]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("100",2))
        self.assertEqual(a.cal(int("11",2), int("11",2)), int("111",2))

    def test_addition_with_or_gate(self):
        # Test addition with an OR gate
        g = [gate(gate.type_or)]
        connections = [1, 2, 5, 2, 3]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("100",2))
        self.assertEqual(a.cal(int("10",2), int("11",2)), int("101",2))

    def test_addition_with_not_gate(self):
        # Test addition with a NOT gate
        g = [gate(gate.type_not)]
        connections = [1, 2, 5, 2, 3]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("101",2))
        self.assertEqual(a.cal(int("11",2), int("11",2)), int("110",2))

    def test_addition_with_xor_gate(self):
        # Test addition with an XOR gate
        g = [gate(gate.type_xor)]
        connections = [1, 2, 5, 2, 3]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("100",2))
        self.assertEqual(a.cal(int("11",2), int("01",2)), int("111",2))
        
    def test_addition_with_and_gate_plus_or_gate(self):
        # Test addition with an XOR gate
        g = [gate(gate.type_and), gate(gate.type_or)]
        connections = [1, 5, 6, 1, 2, 3, 4]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("101",2))
        self.assertEqual(a.cal(int("11",2), int("00",2)), int("110",2))
    
    def test_addition_with_and_gate_link_or_gate(self):
        # Test addition with an XOR gate
        g = [gate(gate.type_and), gate(gate.type_or)]
        connections = [1, 5, 6, 2, 3, 5, 4]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(int("01",2), int("10",2)), int("011",2))
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("101",2))

    def test_empty_connection(self):
        # Test invalid connection that should result in -1
        g = [gate(gate.type_and)]
        connections = []
        a = adder(2, g, connections)
        self.assertEqual(a.cal(1, 1), 0)

    def test_loop_detection(self):
        # Test loop detection
        g = [gate(gate.type_and)]
        connections = [1, 2, 5, 1, 5]
        a = adder(2, g, connections)
        self.assertEqual(a.cal(1, 1), -1)
        
    def test_involute_none(self):
        a = adder(2, [], [])
        a.involute(0.1)
        
    def test_involute(self):
        a = adder(2, [gate(gate.type_and)], [1, 2, 3, 4])
        a.involute(0.2)

if __name__ == '__main__':
    unittest.main()