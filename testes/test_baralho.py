"""Testes de métodos da classe BAralho"""

import sys
import random
import pytest
sys.path.append('../qs-testes-truco-25-2')

from truco.baralho import Baralho


def test_criar_baralho(baralho):
    """Testa se o baralho é criado com naipes e valores válidos"""

    for n in range(0, 40):
        assert baralho.cartas[n].naipe in ["ESPADAS", "OUROS", "COPAS", "BASTOS"]
        assert (1 <= baralho.cartas[n].numero < 8) or (10 <= baralho.cartas[n].numero < 13)

def test_embaralhar(baralho):
    """Utiliza uma seed específica para testar se o baralho está sendo embaralhado"""
    seed = 0xBEEF

    random.seed(seed)
    expected = random.shuffle(Baralho().cartas)

    assert baralho.embaralhar() == expected

def test_retirar_carta(baralho):
    """Testa se a carta retornada é a última e se o baralho diminui"""

    carta = baralho.cartas[39]
    assert baralho.retirar_carta() == carta
    assert len(baralho.cartas) == 39

def test_resetar(baralho):
    """Testa se o baralho fica zerado depois de resetar"""
    baralho.vira = [2]
    baralho.cartas = [2]
    baralho.manilhas = [2]
    baralho.resetar()
    assert baralho.vira == []
    assert baralho.manilhas == []
    assert baralho.cartas == []

def test_printar_baralho(baralho, capsys):
    """Verifica se a exibição do baralho está correta"""
    
    expected = ""
    for c in baralho.cartas:
        expected += f"[] {c.numero} de {c.naipe}\n"
    baralho.printar_baralho()
    captured = capsys.readouterr()
    assert captured.out == expected
