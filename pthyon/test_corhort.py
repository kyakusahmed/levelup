import unittest
from corhort import Corhort


class TestCohort(unittest.TestCase):
    def test_attendees(self):
        ande35 = Corhort(70, "dec", 2, "3weeks")
        self.assertIs(type(ande35.duration), int)
        self.assertIsInstance(ande35, Corhort)