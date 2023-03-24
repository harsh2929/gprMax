import sys
import unittest
from contextlib import contextmanager
from io import StringIO
from gprMax.input_cmd_funcs import *


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestInputCmdFuncs(unittest.TestCase):
    @staticmethod
    def assert_output(out, expected_out):
        """Helper function to compare output and expected output."""
        output = out.getvalue().strip()
        assert output == expected_out, f"Output does not match expected output:\n{output}\n{expected_out}"

    def test_rx(self):
        with captured_output() as (out, _):
            rx(0, 0, 0)
        self.assert_output(out, "#rx: 0 0 0")

    def test_rx_with_id(self):
        with captured_output() as (out, _):
            rx(0, 1, 2, "id")
        self.assert_output(out, "#rx: 0 1 2 id")

    def test_rx_with_id_and_polarisation(self):
        with captured_output() as (out, _):
            rx(2, 1, 0, "id", ["Ex"], polarisation="y")
        self.assert_output(out, "#rx: 2 1 0 id Ex")

    def test_rx_with_id_and_multiple_polarisations(self):
        with captured_output() as (out, _):
            rx(2, 1, 0, "id", ["Ex", "Ez"])
        self.assert_output(out, "#rx: 2 1 0 id Ex Ez")

    def test_rx_with_rotation_exception(self):
        with self.assertRaises(ValueError):
            rx(2, 1, 0, "id", ["Ex", "Ez"], polarisation="x", rotate90origin=(1, 1))  # no dxdy given

    def test_rx_with_rotation_success(self):
        with captured_output() as (out, _):
            rx(2, 1, 0, "id", ["Ex", "Ez"], polarisation="x", rotate90origin=(1, 1), dxdy=(0, 0))
        self.assert_output(out, "#rx: 1 2 0 id Ex Ez")  # note: x, y swapped

    def test_src_steps(self):
        with captured_output() as (out, _):
            src_steps()
        self.assert_output(out, "#src_steps: 0 0 0")

    def test_src_steps_with_values(self):
        with captured_output() as (out, _):
            src_steps(42, 43, 44.2)
        self.assert_output(out, "#src_steps: 42 43 44.2")

    def test_rx_steps(self):
        with captured_output() as (out, _):
            rx_steps()
        self.assert_output(out, "#rx_steps: 0 0 0")

    def test_rx_steps_with_values(self):
        with captured_output() as
    
    
    def test_rx_steps2(self):
        with captured_output() as (out, err):
            rx_steps(42, 43, 44.2)
        self.assert_output(out, '#rx_steps: 42 43 44.2')

if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    

    
