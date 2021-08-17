from src.leilao.excecoes import LanceInvalido


class Usuario:

    def __init__(self, nome, carteira):
        self.__nome = nome
        self.__carteira = carteira

    @property
    def nome(self):
        return self.__nome

    @property
    def carteira(self):
        return self.__carteira

    def propoe_lance(self, leilao, valor):
        if valor > self.__carteira:
            raise LanceInvalido(
                'Não pode propor lance com valor maior que valor da carteira.')

        lance = Lance(self, valor)
        leilao.propoe(lance)

        self.__carteira -= valor


class Lance:

    def __init__(self, usuario, valor):
        self.usuario = usuario
        self.valor = valor


class Leilao:

    def __init__(self, descricao):
        self.maior_lance = 0.0
        self.menor_lance = 0.0
        self.descricao = descricao
        self.__lances = []

    def propoe(self, lance: Lance):
        if self.lance_valido(lance):
            if not self._tem_lances():
                self.menor_lance = lance.valor

            self.maior_lance = lance.valor

            self.__lances.append(lance)

    @property
    def lances(self):
        return self.__lances[:]

    def lance_valido(self, lance):
        return not self._tem_lances() or self._usuarios_diferentes(lance) and \
            self._valor_maior_que_lance_anterior(lance)

    def _tem_lances(self):
        return self.__lances

    def _usuarios_diferentes(self, lance):
        if self.__lances[-1].usuario != lance.usuario:
            return True
        raise LanceInvalido('Usuário não pode propor lances seguidos.')

    def _valor_maior_que_lance_anterior(self, lance):
        if lance.valor > self.__lances[-1].valor:
            return True
        raise LanceInvalido(
            'O valor do lance deve ser maior que o lance anterior.')
