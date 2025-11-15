""""Testa métodos da classe Dados"""
import sys
import pytest
import pandas as pd
import os
sys.path.append('../qs-testes-truco-25-2')

from truco.dados import Dados

@pytest.fixture
def dados():
    return Dados()

@pytest.fixture
def colunas():
    return ['idMao', 'jogadorMao', 'cartaAltaRobo', 'cartaMediaRobo', 'cartaBaixaRobo', 'cartaAltaHumano', 'cartaMediaHumano', 'cartaBaixaHumano', 'primeiraCartaRobo', 'primeiraCartaHumano', 'segundaCartaRobo', 'segundaCartaHumano', 'terceiraCartaRobo', 'terceiraCartaHumano', 'ganhadorPrimeiraRodada', 'ganhadorSegundaRodada', 'ganhadorTerceiraRodada', 'quemPediuEnvido', 'quemPediuFaltaEnvido', 'quemPediuRealEnvido', 'pontosEnvidoRobo', 'pontosEnvidoHumano', 'quemNegouEnvido', 'quemGanhouEnvido', 'quemFlor', 'quemContraFlor', 'quemContraFlorResto', 'quemNegouFlor', 'pontosFlorRobo', 'pontosFlorHumano', 'quemGanhouFlor', 'quemEscondeuPontosEnvido', 'quemEscondeuPontosFlor', 'quemTruco', 'quemRetruco', 'quemValeQuatro', 'quemNegouTruco', 'quemGanhouTruco','quemEnvidoEnvido', 'quemFlor', 'naipeCartaAltaRobo', 'naipeCartaMediaRobo', 'naipeCartaBaixaRobo', 'naipeCartaAltaHumano', 'naipeCartaMediaHumano', 'naipeCartaBaixaHumano', 'naipePrimeiraCartaRobo', 'naipePrimeiraCartaHumano', 'naipeSegundaCartaRobo', 'naipeSegundaCartaHumano', 'naipeTerceiraCartaRobo', 'naipeTerceiraCartaHumano', 'qualidadeMaoRobo', 'qualidadeMaoHumano']

def test_carregar_modelo_zerado(dados, colunas):
    """Testa a criação de um dataframe zerado"""
    df = pd.DataFrame = dados.carregar_modelo_zerado()
    assert df.shape == (1,52)
    assert df.index.to_list() == [0]
    assert df.columns.to_list() != colunas

def test_tratamento_inicial_df(dados):
    """Testa se os dados iniciais do dataframe estão sendo tratados corretamente"""
    df = dados.tratamento_inicial_df()
    cols = ['naipeCartaAltaRobo', 'naipeCartaMediaRobo','naipeCartaBaixaRobo', 'naipeCartaAltaHumano','naipeCartaMediaHumano', 'naipeCartaBaixaHumano','naipePrimeiraCartaRobo', 'naipePrimeiraCartaHumano',	'naipeSegundaCartaRobo', 'naipeSegundaCartaHumano','naipeTerceiraCartaRobo', 'naipeTerceiraCartaHumano',]

    for i in cols:
        assert i in df.columns.to_list()
    
    for i in df.columns.to_list():
        if i not in cols:
            assert df[i].dtype == "int16"

def test_cartas_jogadas_pelo_bot(dados, espadao):
    """Testa se as cartas jogadas pelo bot estão sendo adicionadas corretamente ao dataframe"""
    try:
        dados.cartas_jogadas_pelo_bot("primeira", espadao)
    except:
        assert False
    
    assert dados.registro.primeiraCartaRobo[0] == espadao.retornar_numero()
    assert dados.registro.naipePrimeiraCartaRobo[0] == espadao.retornar_naipe_codificado()

    try:
        dados.cartas_jogadas_pelo_bot("segunda", espadao)
    except:
        assert False
    
    assert dados.registro.segundaCartaRobo[0] == espadao.retornar_numero()
    assert dados.registro.naipeSegundaCartaRobo[0] == espadao.retornar_naipe_codificado()

    try:
        dados.cartas_jogadas_pelo_bot("terceira", espadao)
    except:
        assert False
    
    assert dados.registro.terceiraCartaRobo[0] == espadao.retornar_numero()
    assert dados.registro.naipeTerceiraCartaRobo[0] == espadao.retornar_naipe_codificado()

def test_primeira_rodada(dados, carta_alta_ouro):
    """"Testa se os dados das jogadas do bot na primeira rodada estão sendo salvos corretamente"""
    try:    
        dados.primeira_rodada([3,2,1], ['Alta', 'Media', 'Baixa'], 1, carta_alta_ouro)
    except:
        assert False
    assert dados.registro.jogadorMao[0] == 1;
    assert dados.registro.cartaAltaRobo[0] == 3
    assert dados.registro.cartaMediaRobo[0] == 2
    assert dados.registro.cartaBaixaRobo[0] == 1
    assert dados.registro.qualidadeMaoBot == 1
    assert dados.registro.primeiraCartaHumano[0] == carta_alta_ouro.retornar_numero()
    assert dados.registro.naipePrimeiraCartaHumano[0] == carta_alta_ouro.retornar_naipe_codificado()

def test_segunda_rodada(dados, espadao, bastiao):
    """"Testa se os dados das jogadas do bot na segunda rodada estão sendo salvos corretamente"""
    try:
        dados.segunda_rodada(espadao, bastiao, 1)
    except:
        assert False
    assert dados.registro.ganhadorPrimeiraRodada[0] == 1
    assert dados.registro.primeiraCartaHumano[0] == espadao.retornar_numero()
    assert dados.registro.naipePrimeiraCartaHumano[0] == espadao.retornar_naipe_codificado()
    assert dados.registro.terceiraCartaRobo[0] == bastiao.retornar_numero()

def test_terceira_rodada(dados, espadao, bastiao):
    """"Testa se os dados das jogadas do bot na terceira rodada estão sendo salvos corretamente"""
    try:
        dados.terceira_rodada(espadao, bastiao, 1)
    except:
        assert False
    assert dados.registro.ganhadorSegundaRodada[0] == 1
    assert dados.registro.SegundaCartaHumano == espadao.retornar_numero()
    assert dados.registro.naipeSegundaCartaHumano[0] == espadao.retornar_naipe_codificado()
    assert dados.registro.terceiraCartaRobo[0] == bastiao.retornar_numero()

def test_finalizar_rodadas(dados, espadao):
    """Testa se as informações de cartas jogadas pelo oponente na rodada final estão sendo salvas corretamente"""
    try:
        dados.finalizar_rodadas(espadao,espadao, 1)
    except:
        assert False
    assert dados.registro.ganhadorTerceiraRodada[0] == 1
    assert dados.registro.terceiraCartaHumano[0] == espadao.retornar_numero()
    assert dados.registro.naipeTerceiraCartaHumano[0] == espadao.retornar_naipe_codificado()
    assert dados.registro.terceiraCartaRobo[0] == espadao.retornar_numero()

def test_envido(dados):
    """Testa se as informações referentes ao envido estão sendo salvas corretamente"""
    try:
        dados.envido(1, 2, 2, 1)
    except:
        assert False

    assert dados.registro.quemEnvido == 1
    assert dados.registro.quemRealEnvido == 2
    assert dados.registro.quemFaltaEnvido == 2
    assert dados.registro.quemGanhouEnvido[0] == 1

def test_truco(dados):
    """Testa se as informações referentes ao truco estão sendo salvas corretamente"""
    try:
        dados.truco(1,2,3,4,5)
    except:
        assert False
    assert dados.registro.quemTruco[0] == 1
    assert dados.registro.quemRetruco[0] == 2
    assert dados.registro.quemValeQuatro[0] == 3
    assert dados.registro.quemNegouTruco[0] == 4
    assert dados.registro.quemGanhouTruco[0] == 5

def test_flor(dados):
    """Testa se as informações referentes à flor estão sendo salvas corretamente"""
    try:
        dados.flor(1,2,3,4)
    except:
        assert False
    assert dados.registro.quemGanhouFlor[0] == 2
    assert dados.registro.quemFlor[0] == 1
    assert dados.registro.quemContraFlor[0] == 2
    assert dados.registro.quemContraFlorResto[0] == 3
    assert dados.registro.pontosFlorRobo[0] == 4

def test_vencedor_envido(dados):
    """Testa se as informações referentes ao vencedor do envido estão sendo salvas corretamente"""
    try:
        dados.vencedor_envido(1,2)
    except:
        assert False
    assert dados.registro.quemGanhouEnvido[0] == 1
    assert dados.registro.quemNegouEnvido[0] == 2

def test_vencedor_truco(dados):
    """Testa se as informações referentes ao vencedor do truco estão sendo salvas corretamente"""
    try:
        dados.vencedor_truco(1,2)
    except:
        assert False
    assert dados.registro.quemGanhouTruco[0] == 1
    assert dados.registro.quemNegouTruco[0] == 2

def test_vencedor_flor(dados):
    """Testa se as informações referentes ao vencedor do flor estão sendo salvas corretamente"""
    try:
        dados.vencedor_flor(1,2)
    except:
        assert False
    assert dados.registro.quemGanhouFlor[0]== 1
    assert dados.registro.quemNegouFlor[0]== 2

def test_retornar_registro(dados):
    """Testa se os registros retornados são corretos"""
    assert dados.registro.equals(dados.retornar_registro())

def test_retornar_casos(dados):
    """Testa se os casos retornados são corretos"""
    assert dados.casos.equals(dados.retornar_casos())

def test_finalizar_partida(dados):
    """Testa se as jogadas estão sendo salvas corretamente"""
    # Testa os dois condicionais
    if os.path.isfile("jogadas.csv"):
        os.remove("jogadas.csv")

    try:
        dados.finalizar_partida()
    except:
        assert False
    
    assert os.path.isfile("jogadas.csv")

    try:
        dados.finalizar_partida()
    except:
        assert False
    
    assert os.path.isfile("jogadas.csv")

def test_resetar(dados):
    """Testa se os dados estão sendo corretamente resetados"""
    #Insere registros para garantir que serão resetados
    dados.vencedor_truco(1,2)
    df_casos = dados.tratamento_inicial_df()
    df_registro = dados.carregar_modelo_zerado()

    try:
        dados.resetar()
    except:
        assert False

    assert dados.registro.equals(df_registro)
    assert dados.casos.equals(df_casos)