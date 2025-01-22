import unittest
from src.negocio.ContaAbstrata import ContaAbstrata
from src.negocio.ContaTeste import ContaTeste
from src.exceptions.SaldoInsuficienteException import SaldoInsuficienteException

class TestContaAbstrata(unittest.TestCase):
    def setUp(self):
        self.conta = ContaTeste("001", 1000.0)

    def test_get_numero(self):
        self.assertEqual(self.conta.getNumero(), "001")

    def test_set_numero(self):
        self.conta.setNumero("002")
        self.assertEqual(self.conta.getNumero(), "002")

    def test_get_saldo(self):
        self.assertEqual(self.conta.getSaldo(), 1000.0)

    def test_set_saldo(self):
        self.conta.setSaldo(500.0)
        self.assertEqual(self.conta.getSaldo(), 500.0)

    def test_creditar_valor_valido(self):
        self.conta.creditar(500.0)
        self.assertEqual(self.conta.getSaldo(), 1500.0)

    def test_creditar_valor_zero(self):
        self.conta.creditar(0.0)
        self.assertEqual(self.conta.getSaldo(), 1000.0)

    def test_creditar_valor_negativo(self):
        self.conta.creditar(-100.0)
        self.assertEqual(self.conta.getSaldo(), 1000.0)

    def test_debitar_valor_valido(self):
        self.conta.debitar(500.0)
        self.assertEqual(self.conta.getSaldo(), 500.0)

    def test_debitar_valor_excede_saldo(self):
        with self.assertRaises(SaldoInsuficienteException):
            self.conta.debitar(1500.0)

    def test_debitar_valor_zero(self):
        with self.assertRaises(ValueError):
            self.conta.debitar(0.0)

    def test_debitar_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.conta.debitar(-100.0)

    def test_get_tipo(self):
        self.assertEqual(self.conta.get_tipo(), "teste")

    def test_eq_mesmo_numero(self):
        outra_conta = ContaTeste("001", 500.0)
        self.assertTrue(self.conta == outra_conta)

    def test_eq_diferente_numero(self):
        outra_conta = ContaTeste("002", 500.0)
        self.assertFalse(self.conta == outra_conta)

if __name__ == "__main__":
    unittest.main()
