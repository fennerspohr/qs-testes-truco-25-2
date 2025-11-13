"""Testes de métodos da classe Carta"""

import sys
import pytest
sys.path.append('../qs-testes-truco-25-2')

from truco.carta import Carta
from truco.pontos import MANILHA, CARTAS_VALORES, ENVIDO


def test__init__():
    """Testando se método __init__ de Carta cria corretamente a instância"""

    instance = Carta(5, "ESPADAS")
    assert instance.numero == 5
    assert instance.naipe == "ESPADAS"

def test_verificar_carta_alta(espadao, bastiao, carta_alta_ouro, carta_baixa_copas, carta_baixa_ouro):
    """Testa todos os condicionais de verificar_carta_alta"""

    # Duas manilhas
    assert espadao.verificar_carta_alta(espadao, bastiao) == espadao
    # Uma manilha e uma carta normal
    assert bastiao.verificar_carta_alta(carta_alta_ouro, bastiao) == bastiao
    # Duas cartas normais de valores diferentes
    assert carta_alta_ouro.verificar_carta_alta(carta_baixa_copas, carta_alta_ouro) == carta_alta_ouro
    # Duas cartas normais de valores iguais
    assert carta_baixa_ouro.verificar_carta_alta(carta_baixa_ouro, carta_baixa_copas) == carta_baixa_copas

def test_verificar_carta_baixa(espadao, bastiao, carta_alta_ouro, carta_baixa_copas, carta_baixa_ouro):
    """Testa todos os condicionais de verificar_carta_baixa"""

    # Duas manilhas
    assert espadao.verificar_carta_baixa(espadao, bastiao) == bastiao
    # Uma manilha e uma carta normal
    assert bastiao.verificar_carta_baixa(bastiao, carta_alta_ouro) == carta_alta_ouro
    # Duas cartas normais de valores diferentes
    assert carta_alta_ouro.verificar_carta_baixa(carta_baixa_copas, carta_alta_ouro) == carta_baixa_copas
    # Duas cartas normais de valores iguais
    assert carta_baixa_ouro.verificar_carta_baixa(carta_baixa_copas, carta_baixa_ouro) == carta_baixa_ouro

def test_retornar_pontos_cartas(espadao, carta_alta_ouro):
    """Testa os condicionais de retornar_pontos_cartas"""

    # Manilha
    assert espadao.retornar_pontos_carta(espadao) == MANILHA["1 de ESPADAS"]
    # Carta normal
    assert carta_alta_ouro.retornar_pontos_carta(carta_alta_ouro) == CARTAS_VALORES["3"]

def test_classficar_carta(espadao, carta_alta_ouro, carta_baixa_ouro):
    """Testa se classficar método retorna as cartas com rank e pontuação corretos"""
    
    pontos, rank = espadao.classificar_carta([espadao, carta_alta_ouro, carta_baixa_ouro])
    assert pontos == [MANILHA["1 de ESPADAS"], CARTAS_VALORES["3"], CARTAS_VALORES["4"]]
    assert rank == ['Alta', 'Media', 'Baixa']

def test_exibir_carta(espadao, capsys):
    """Testa se a exibição da carta e do número de opção está correta"""

    # Sem número 
    espadao.exibir_carta()
    captured = capsys.readouterr()
    assert captured.out == f"[] {espadao.numero} de {espadao.naipe}\n"
    # Com número
    espadao.exibir_carta(2) 
    captured = capsys.readouterr()
    assert captured.out == f"[2] {espadao.numero} de {espadao.naipe}\n"

def test_retornar_carta(bastiao):
    """Testa se o retorno do número e naipe está correto"""
    assert bastiao.retornar_carta() == f"{bastiao.numero} de {bastiao.naipe}"

def test_retornar_pontos_envido(bastiao):
    """Testa se os pontos de envido retornados estão corretos"""
    assert bastiao.retornar_pontos_envido(bastiao) == ENVIDO[str(bastiao.numero)]

def test_retornar_numero(bastiao):
    """Testa retorno do número da carta"""
    assert bastiao.retornar_numero() == bastiao.numero

def test_retornar_naipe(bastiao):
    """Testa retorno do naipe da carta"""
    assert bastiao.retornar_naipe() == bastiao.naipe

def test_retornar_naipe_codificado(espadao, carta_alta_ouro, bastiao, carta_baixa_copas):
    """Testa todos os condicionais de retorno de naipe codificado"""
    assert espadao.retornar_naipe_codificado() == 1
    assert carta_alta_ouro.retornar_naipe_codificado() == 2
    assert bastiao.retornar_naipe_codificado() == 3
    assert carta_baixa_copas.retornar_naipe_codificado() == 4
