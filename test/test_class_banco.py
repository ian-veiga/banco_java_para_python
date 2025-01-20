import unittest
from unittest.mock import Mock, MagicMock
from src.negocio.Banco import Banco
from src.negocio.Cliente import Cliente
from src.negocio.ContaAbstrata import ContaAbstrata
from src.negocio.ContaEspecial import ContaEspecial
from src.negocio.ContaPoupanca import ContaPoupanca
from src.exceptions.ClienteJaCadastradoException import ClienteJaCadastradoException
from src.exceptions.ClienteNaoCadastradoException import ClienteNaoCadastradoException
from src.exceptions.ContaJaAssociadaException import ContaJaAssociadaException
from src.exceptions.ContaJaCadastradaException import ContaJaCadastradaException
from src.exceptions.ContaNaoEncontradaException import ContaNaoEncontradaException
from src.exceptions.RenderBonusContaEspecialException import RenderBonusContaEspecialException
from src.exceptions.RenderJurosPoupancaException import RenderJurosPoupancaException
from src.exceptions.ValorInvalidoException import ValorInvalidoException

class TestBanco(unittest.TestCase):

    def setUp(self):
        # Mock dos repositórios
        self.clientes_mock = Mock()
        self.contas_mock = Mock()

        # Instância da classe Banco
        self.banco = Banco(self.clientes_mock, self.contas_mock)

    def test_cadastrar_cliente_sucesso(self):
        cliente = Cliente("123", "Teste")
        self.clientes_mock.inserir.return_value = True

        self.banco.cadastrar_cliente(cliente)

        self.clientes_mock.inserir.assert_called_once_with(cliente)

    def test_cadastrar_cliente_ja_cadastrado(self):
        cliente = Cliente("123", "Teste")
        self.clientes_mock.inserir.return_value = False

        with self.assertRaises(ClienteJaCadastradoException):
            self.banco.cadastrar_cliente(cliente)

    def test_procurar_cliente_sucesso(self):
        cliente = Cliente("123", "Teste")
        self.clientes_mock.procurar.return_value = cliente

        resultado = self.banco.procurar_cliente("123")

        self.assertEqual(resultado, cliente)
        self.clientes_mock.procurar.assert_called_once_with("123")

    def test_cadastrar_conta_sucesso(self):
        conta = Mock(spec=ContaAbstrata)
        self.contas_mock.inserir.return_value = True

        self.banco.cadastrar_conta(conta)

        self.contas_mock.inserir.assert_called_once_with(conta)

    def test_cadastrar_conta_ja_cadastrada(self):
        conta = Mock(spec=ContaAbstrata)
        self.contas_mock.inserir.return_value = False

        with self.assertRaises(ContaJaCadastradaException):
            self.banco.cadastrar_conta(conta)

    def test_associar_conta_sucesso(self):
        # Mock para cliente e conta
        cliente_mock = Mock()
        conta_mock = Mock()

        cliente_mock.get_cpf.return_value = "123"
        cliente_mock.get_contas.return_value = []

        # Configura o método getIterator() para retornar uma lista de clientes simulados
        self.clientes_mock.getIterator.return_value = [cliente_mock]
        self.clientes_mock.procurar.return_value = cliente_mock
        self.contas_mock.procurar.return_value = conta_mock

        # Chama o método associar_conta
        self.banco.associar_conta("123", "001")

        # Verifica se o método foi chamado corretamente
        cliente_mock.adicionar_conta.assert_called_once_with("001")
        self.clientes_mock.atualizar.assert_called_once_with(cliente_mock)


    def test_associar_conta_cliente_nao_cadastrado(self):
        self.clientes_mock.procurar.return_value = None

        with self.assertRaises(ClienteNaoCadastradoException):
            self.banco.associar_conta("123", "001")

    def test_associar_conta_conta_nao_encontrada(self):
        self.clientes_mock.procurar.return_value = Mock()
        self.contas_mock.procurar.return_value = None

        with self.assertRaises(ContaNaoEncontradaException):
            self.banco.associar_conta("123", "001")

    def test_creditar_sucesso(self):
        conta_mock = Mock()
        conta_mock.getNumero.return_value = "001"
        self.contas_mock.existe.return_value = True

        self.banco.creditar(conta_mock, 100.0)

        conta_mock.creditar.assert_called_once_with(100.0)
        self.contas_mock.atualizar.assert_called_once_with(conta_mock)

    def test_creditar_valor_invalido(self):
        conta_mock = Mock()

        with self.assertRaises(ValorInvalidoException):
            self.banco.creditar(conta_mock, -50.0)

    def test_render_bonus_sucesso(self):
        conta_mock = Mock(spec=ContaEspecial)
        conta_mock.getNumero.return_value = "001"
        self.contas_mock.existe.return_value = True

        self.banco.render_bonus(conta_mock)

        conta_mock.renderbonus.assert_called_once()
        self.contas_mock.atualizar.assert_called_once_with(conta_mock)

    def test_render_bonus_excecao(self):
        conta_mock = Mock(spec=ContaAbstrata)

        with self.assertRaises(RenderBonusContaEspecialException):
            self.banco.render_bonus(conta_mock)

    def test_render_juros_sucesso(self):
        conta_mock = Mock(spec=ContaPoupanca)
        conta_mock.getNumero.return_value = "001"
        self.contas_mock.existe.return_value = True

        self.banco.render_juros(conta_mock)

        conta_mock.render_juros.assert_called_once_with(0.5)
        self.contas_mock.atualizar.assert_called_once_with(conta_mock)

    def test_render_juros_excecao(self):
        conta_mock = Mock(spec=ContaAbstrata)

        with self.assertRaises(RenderJurosPoupancaException):
            self.banco.render_juros(conta_mock)
