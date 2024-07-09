import unittest
from adder_evolution.gate import gate

class TestGate(unittest.TestCase):

    def test_and_gate(self):
        g = gate(gate.type_and)
        self.assertEqual(g.cal("1", "1"), "1")
        self.assertEqual(g.cal("1", "0"), "0")
        self.assertEqual(g.cal("0", "1"), "0")
        self.assertEqual(g.cal("0", "0"), "0")

    def test_or_gate(self):
        g = gate(gate.type_or)
        self.assertEqual(g.cal("1", "1"), "1")
        self.assertEqual(g.cal("1", "0"), "1")
        self.assertEqual(g.cal("0", "1"), "1")
        self.assertEqual(g.cal("0", "0"), "0")

    def test_not_gate(self):
        g = gate(gate.type_not)
        self.assertEqual(g.cal("1", "0"), "0")
        self.assertEqual(g.cal("0", "0"), "1")

    def test_xor_gate(self):
        g = gate(gate.type_xor)
        self.assertEqual(g.cal("1", "1"), "0")
        self.assertEqual(g.cal("1", "0"), "1")
        self.assertEqual(g.cal("0", "1"), "1")
        self.assertEqual(g.cal("0", "0"), "0")

    def test_invalid_gate_type(self):
        with self.assertRaises(ValueError):
            g = gate(5)
            g.cal("1", "1")

if __name__ == '__main__':
    unittest.main()