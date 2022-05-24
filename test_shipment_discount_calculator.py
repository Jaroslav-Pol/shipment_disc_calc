import unittest
from shipment_discount_calculator import *


class TestShipmentDiscountCalc(unittest.TestCase):
    def test_fl_to_str(self):
        self.assertEqual(float_to_str(1), '1.00')
        self.assertEqual(float_to_str(0), '0.00')
        self.assertEqual(float_to_str(1.22), '1.23')

    def test_data(self):
        self.assertEqual(couriers['LP']['price_s'], 1.5)
