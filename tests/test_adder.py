import unittest
from adder_evolution.gate import gate
from adder_evolution.adder import adder, connect

class TestAdder(unittest.TestCase):
    
    def test_simple_addition(self):
        # Test simple addition without any gates
        a = adder([], [], [connect(connect.type_input1, 0),
                           connect(connect.type_input1, 1),
                           connect(connect.type_input2, 1)])
        self.assertEqual(a.cal(int("01",2), int("10",2)), int("101",2))
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("010",2))

    def test_addition_with_and_gate(self):
        # Test addition with an AND gate
        a = adder([gate(gate.type_and)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("000",2))
        self.assertEqual(a.cal(int("11",2), int("11",2)), int("111",2))

    def test_addition_with_or_gate(self):
        # Test addition with an OR gate
        a = adder([gate(gate.type_or)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("11",2), int("01",2)), int("101",2))
        self.assertEqual(a.cal(int("00",2), int("01",2)), int("000",2))

    def test_addition_with_not_gate(self):
        # Test addition with a NOT gate
        a = adder([gate(gate.type_not)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("100",2))
        self.assertEqual(a.cal(int("11",2), int("11",2)), int("011",2))

    def test_addition_with_xor_gate(self):
        # Test addition with an XOR gate
        a = adder([gate(gate.type_xor)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("000",2))
        self.assertEqual(a.cal(int("11",2), int("01",2)), int("101",2))
        
    def test_addition_with_left_gate(self):
        # Test addition with an LEFT gate
        a = adder([gate(gate.type_left)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("000",2))
        self.assertEqual(a.cal(int("11",2), int("01",2)), int("101",2))
        
    def test_addition_with_right_gate(self):
        # Test addition with an RIGHT gate
        a = adder([gate(gate.type_right)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,1), connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(int("10",2), int("01",2)), int("000",2))
        self.assertEqual(a.cal(int("11",2), int("01",2)), int("001",2))
        
    def test_addition_with_and_gate_plus_or_gate(self):
        # Test addition with an two gate side by side
        a = adder([gate(gate.type_and), gate(gate.type_or)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)],
                   [connect(connect.type_input1,1), connect(connect.type_input2,0)]],
                  [connect(connect.type_input1,0), connect(connect.type_gate,0), connect(connect.type_gate, 1)])
        self.assertEqual(a.cal(int("00",2), int("11",2)), int("100",2))
        self.assertEqual(a.cal(int("11",2), int("00",2)), int("101",2))
    
    def test_addition_with_and_gate_link_or_gate(self):
        # Test addition with an two gate linked
        a = adder([gate(gate.type_and), gate(gate.type_or)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,1)],
                   [connect(connect.type_gate,0), connect(connect.type_input1,1)]],
                  [connect(connect.type_input1,0), connect(connect.type_gate,0), connect(connect.type_gate, 1)])
        self.assertEqual(a.cal(int("00",2), int("11",2)), int("000",2))
        self.assertEqual(a.cal(int("11",2), int("00",2)), int("101",2))

    def test_empty_connection(self):
        # Test invalid connection that should result in -1
        a = adder([gate(gate.type_and)], [], [])
        self.assertEqual(a.cal(1, 1), 0)

    def test_loop_detection(self):
        # Test loop detection
        a = adder([gate(gate.type_and)], [[connect(connect.type_gate, 0), connect(connect.type_gate, 1)]], [connect(connect.type_gate, 0)])
        self.assertEqual(a.cal(1, 1), -1)
        
    def test_mutate_none(self):
        a = adder([], [], [])
        a.mutate(0.99)
        
    def test_mutate(self):
        a = adder([gate(gate.type_and)],
                  [[connect(connect.type_input1,0), connect(connect.type_input2,0)]],
                  [connect(connect.type_input1,0), connect(connect.type_input2,0), 
                   connect(connect.type_gate, 0)])
        a.mutate(0.99).packJSON()

if __name__ == '__main__':
    unittest.main()