import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (preserved behaviour)
    # ------------------------------------------------------------------
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_keyword(self):
        """Passing service='standard' explicitly must match the default."""
        self.assertEqual(shipping_quote(2, "local", service="standard"), 8.0)
        self.assertEqual(shipping_quote(2, "regional", service="standard"), 11.0)

    # ------------------------------------------------------------------
    # Express service ($7 surcharge on top of standard)
    # ------------------------------------------------------------------
    def test_express_local(self):
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_surcharge_is_seven_dollars(self):
        """Express quote must be exactly $7 more than standard for every weight."""
        for weight in (1, 5, 10.5):
            with self.subTest(weight=weight):
                std = shipping_quote(weight, "local")
                exp = shipping_quote(weight, "local", service="express")
                self.assertAlmostEqual(exp - std, 7.0)

    # ------------------------------------------------------------------
    # Validation errors
    # ------------------------------------------------------------------
    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "international")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")
