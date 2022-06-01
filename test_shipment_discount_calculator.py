import unittest
from shipment_discount_calculator import *


class TestShipmentDiscountCalc(unittest.TestCase):
    def test_fl_to_str(self):
        self.assertEqual(float_to_str(1.02985548), '1.03')
        self.assertEqual(float_to_str(0), '0.00')
        self.assertEqual(float_to_str('I am string'), 'I am string')

    def test_la_poste(self):
        self.assertEqual(la_poste({
            'tr_date': ['2021', '12', '31'],
            'size': 'L',
            'courier': 'LP',

        }), {
            'reduced_price': 6.9,
            'discount': '-'
        })
