'''
simple tests
'''

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        '''test adding number together.'''
        res = calc.add(5,6)

        self.assertEqual(res,11)
    def test_another(self):
        res = calc.add(9,0)

        self.assertEqual(res,14)
