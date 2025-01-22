import unittest
from src.exceptions.SaldoInsuficienteException import SaldoInsuficienteException
from src.negocio.ContaImposto import ContaImposto


class TestContaImposto(unittest.TestCase):
    def setUp(self):
        self.conta_imposto = ContaImposto("123", 1000.0)

    def test_debitar_valor_valido(self):
        self.conta_imposto.debitar(100.0)
        self.assertAlmostEqual(self.conta_imposto.getSaldo(), 899.62, places=2)

    def test_debitar_valor_limite(self):
        self.conta_imposto.debitar(996.11)
        self.assertAlmostEqual(self.conta_imposto.getSaldo(), 0.0, places=2)

    def test_debitar_saldo_insuficiente(self):
        with self.assertRaises(SaldoInsuficienteException):
            self.conta_imposto.debitar(1001.0)

    def test_debitar_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.conta_imposto.debitar(-100.0)

    def test_debitar_valor_zero(self):
        with self.assertRaises(ValueError):
            self.conta_imposto.debitar(0.0)

    def test_get_tipo(self):
        self.assertEqual(self.conta_imposto.get_tipo(), "imposto")


if __name__ == "__main__":
    unittest.main()
