"""Registro das 74 ferramentas (estilo 4Devs), amarrando cada função a uma categoria e aos
campos de entrada. A interface (ferramentas_br.pyw) lê isto e monta os formulários sozinha.

Cada Campo: (chave, rótulo, tipo, default, opções). tipo in {texto, multiline, int, float, bool, escolha}.
Cada Func: chave, nome, categoria, campos, run(valores)->str, botao.
"""
from __future__ import annotations

import brdocs
import fakes
import mathfn
import textfn


class Campo:
    def __init__(self, chave, rotulo, tipo="texto", default=None, opcoes=None, placeholder=""):
        self.chave, self.rotulo, self.tipo = chave, rotulo, tipo
        self.default, self.opcoes, self.placeholder = default, opcoes, placeholder


class Func:
    def __init__(self, chave, nome, categoria, run, campos=None, botao="Gerar"):
        self.chave, self.nome, self.categoria = chave, nome, categoria
        self.run, self.campos, self.botao = run, campos or [], botao


MASK = lambda: Campo("mascara", "Com pontuação", "bool", True)  # noqa: E731


def _val(ok):
    return "✅  Válido!" if ok else "❌  Inválido."


FUNCS = [
    # ---------------- GERADORES ----------------
    Func("cpf", "Gerador de CPF", "Geradores", lambda v: brdocs.gen_cpf(v["mascara"]), [MASK()]),
    Func("cnpj", "Gerador de CNPJ", "Geradores", lambda v: brdocs.gen_cnpj(v["mascara"]), [MASK()]),
    Func("rg", "Gerador de RG", "Geradores", lambda v: brdocs.gen_rg(v["mascara"]), [MASK()]),
    Func("cnh", "Gerador de CNH", "Geradores", lambda v: brdocs.gen_cnh()),
    Func("pis", "Gerador de PIS/PASEP", "Geradores", lambda v: brdocs.gen_pis(v["mascara"]), [MASK()]),
    Func("renavam", "Gerador de RENAVAM", "Geradores", lambda v: brdocs.gen_renavam()),
    Func("titulo", "Gerador Título de Eleitor", "Geradores", lambda v: brdocs.gen_titulo()),
    Func("cep", "Gerador de CEP", "Geradores", lambda v: brdocs.gen_cep(v["mascara"]), [MASK()]),
    Func("ie", "Gerador Inscrição Estadual (SP)", "Geradores", lambda v: brdocs.gen_ie_sp(v["mascara"]), [MASK()]),
    Func("cartao", "Gerador Cartão de Crédito", "Geradores",
         lambda v: brdocs.gen_cartao(v["bandeira"], v["mascara"]),
         [Campo("bandeira", "Bandeira", "escolha", "Visa", list(brdocs.BRANDS.keys())), MASK()]),
    Func("conta", "Gerador de Conta Bancária", "Geradores",
         lambda v: brdocs.gen_conta(v["banco"]),
         [Campo("banco", "Banco", "escolha", "341 Itaú", list(brdocs.BANCOS.keys()))]),
    Func("certidao", "Gerador de Certidões", "Geradores", lambda v: brdocs.gen_certidao(v["mascara"]), [MASK()]),
    Func("placa", "Gerador Placa de Veículos", "Geradores",
         lambda v: brdocs.gen_placa(v["mercosul"]),
         [Campo("mercosul", "Padrão Mercosul", "bool", True)]),
    Func("pessoa", "Gerador de Pessoas", "Geradores", lambda v: fakes.gerar_pessoa()),
    Func("empresa", "Gerador de Empresas", "Geradores", lambda v: fakes.gerar_empresa()),
    Func("veiculo", "Gerador de Veículos", "Geradores", lambda v: fakes.gerar_veiculo()),
    Func("curriculo", "Gerador de Currículo", "Geradores", lambda v: fakes.gerar_curriculo()),
    Func("nomes", "Gerador de Nomes", "Geradores", lambda v: fakes.gerar_nome(v["sexo"]),
         [Campo("sexo", "Sexo", "escolha", "Aleatório", ["Aleatório", "Masculino", "Feminino"])]),
    Func("nicks", "Gerador de Nicks", "Geradores", lambda v: fakes.gerar_nicks(v["quantidade"]),
         [Campo("quantidade", "Quantidade", "int", 5)]),
    Func("numeros", "Gerador de Números Aleatórios", "Geradores",
         lambda v: fakes.numeros_aleatorios(v["quantidade"], v["minimo"], v["maximo"]),
         [Campo("quantidade", "Quantidade", "int", 10), Campo("minimo", "Mínimo", "int", 1),
          Campo("maximo", "Máximo", "int", 100)]),
    Func("senha", "Gerador de Senha", "Geradores",
         lambda v: fakes.gerar_senha(v["tamanho"], v["maiusculas"], v["minusculas"], v["numeros"], v["simbolos"]),
         [Campo("tamanho", "Tamanho", "int", 12), Campo("maiusculas", "Maiúsculas", "bool", True),
          Campo("minusculas", "Minúsculas", "bool", True), Campo("numeros", "Números", "bool", True),
          Campo("simbolos", "Símbolos", "bool", True)]),
    Func("lorem", "Gerador de Lorem Ipsum", "Geradores", lambda v: fakes.gerar_lorem(v["paragrafos"]),
         [Campo("paragrafos", "Parágrafos", "int", 3)]),
    Func("imagem", "Gerador de Imagem", "Geradores",
         lambda v: fakes.gerar_imagem(v["largura"], v["altura"], v["texto"]),
         [Campo("largura", "Largura (px)", "int", 600), Campo("altura", "Altura (px)", "int", 400),
          Campo("texto", "Texto (opcional)", "texto", "")]),
    Func("simbolos", "Símbolos para Copiar", "Geradores", lambda v: fakes.simbolos(), botao="Mostrar"),
    Func("letras_dif", "Gerador de Letras diferentes", "Geradores",
         lambda v: textfn.letras_personalizadas(v["texto"], v["estilo"]),
         [Campo("texto", "Texto", "texto", "", placeholder="digite aqui"),
          Campo("estilo", "Estilo", "escolha", "Negrito",
                ["Negrito", "Itálico", "Script", "Monoespaçado", "Bolha", "Quadrado", "Invertido", "Largo (fullwidth)"])]),
    Func("sorteador", "Sorteador de números", "Geradores",
         lambda v: fakes.sorteador(v["quantidade"], v["de"], v["ate"]),
         [Campo("quantidade", "Quantos sortear", "int", 6), Campo("de", "De", "int", 1),
          Campo("ate", "Até", "int", 60)], botao="Sortear"),

    # ---------------- VALIDADORES ----------------
    Func("v_cpf", "Validador de CPF", "Validadores", lambda v: _val(brdocs.valid_cpf(v["texto"])),
         [Campo("texto", "CPF", "texto", "")], botao="Validar"),
    Func("v_cnpj", "Validador de CNPJ", "Validadores", lambda v: _val(brdocs.valid_cnpj(v["texto"])),
         [Campo("texto", "CNPJ", "texto", "")], botao="Validar"),
    Func("v_rg", "Validador de RG", "Validadores", lambda v: _val(brdocs.valid_rg(v["texto"])),
         [Campo("texto", "RG", "texto", "")], botao="Validar"),
    Func("v_cnh", "Validador de CNH", "Validadores", lambda v: _val(brdocs.valid_cnh(v["texto"])),
         [Campo("texto", "CNH", "texto", "")], botao="Validar"),
    Func("v_pis", "Validador de PIS/PASEP", "Validadores", lambda v: _val(brdocs.valid_pis(v["texto"])),
         [Campo("texto", "PIS/PASEP", "texto", "")], botao="Validar"),
    Func("v_renavam", "Validador de RENAVAM", "Validadores", lambda v: _val(brdocs.valid_renavam(v["texto"])),
         [Campo("texto", "RENAVAM", "texto", "")], botao="Validar"),
    Func("v_titulo", "Validador Título de Eleitor", "Validadores", lambda v: _val(brdocs.valid_titulo(v["texto"])),
         [Campo("texto", "Título", "texto", "")], botao="Validar"),
    Func("v_ie", "Validar Inscrição Estadual (SP)", "Validadores", lambda v: _val(brdocs.valid_ie_sp(v["texto"])),
         [Campo("texto", "Inscrição Estadual", "texto", "")], botao="Validar"),
    Func("v_cartao", "Validador Cartão Crédito", "Validadores", lambda v: _val(brdocs.valid_cartao(v["texto"])),
         [Campo("texto", "Número do cartão", "texto", "")], botao="Validar"),
    Func("v_conta", "Validador Conta Bancária", "Validadores", lambda v: _val(brdocs.valid_conta(v["texto"])),
         [Campo("texto", "Conta", "texto", "")], botao="Validar"),
    Func("v_certidao", "Validador de Certidões", "Validadores", lambda v: _val(brdocs.valid_certidao(v["texto"])),
         [Campo("texto", "Certidão (32 dígitos)", "texto", "")], botao="Validar"),

    # ---------------- TEXTO ----------------
    Func("t_corretor", "Corretor Ortográfico", "Texto", lambda v: textfn.corretor_ortografico(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Corrigir"),
    Func("t_ordem", "Colocar em Ordem Alfabética", "Texto",
         lambda v: textfn.ordem_alfabetica(v["texto"], v["reverso"]),
         [Campo("texto", "Linhas", "multiline", ""), Campo("reverso", "Ordem inversa (Z→A)", "bool", False)],
         botao="Ordenar"),
    Func("t_contar", "Contador de Caracteres", "Texto", lambda v: textfn.contar_caracteres(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Contar"),
    Func("t_ocorr", "Contador de Ocorrência de Palavra", "Texto",
         lambda v: textfn.contar_ocorrencias(v["texto"], v["palavra"]),
         [Campo("texto", "Texto", "multiline", ""), Campo("palavra", "Palavra", "texto", "")], botao="Contar"),
    Func("t_html", "Converter Texto to HTML", "Texto", lambda v: textfn.texto_para_html(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Converter"),
    Func("t_cortar", "Cortar Textos", "Texto", lambda v: textfn.cortar_texto(v["texto"], v["inicio"], v["fim"]),
         [Campo("texto", "Texto", "multiline", ""), Campo("inicio", "Do caractere", "int", 0),
          Campo("fim", "Até o caractere", "int", 10)], botao="Cortar"),
    Func("t_dividir", "Dividir String", "Texto", lambda v: textfn.dividir_string(v["texto"], v["separador"]),
         [Campo("texto", "Texto", "multiline", ""), Campo("separador", "Separador", "texto", ",")], botao="Dividir"),
    Func("t_info", "Informações de Caracter", "Texto", lambda v: textfn.info_caractere(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Analisar"),
    Func("t_inverter", "Inverter Texto", "Texto", lambda v: textfn.inverter_texto(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Inverter"),
    Func("t_letras", "Letras Personalizadas", "Texto",
         lambda v: textfn.letras_personalizadas(v["texto"], v["estilo"]),
         [Campo("texto", "Texto", "texto", ""),
          Campo("estilo", "Estilo", "escolha", "Negrito",
                ["Negrito", "Itálico", "Script", "Monoespaçado", "Bolha", "Quadrado", "Invertido", "Largo (fullwidth)"])],
         botao="Transformar"),
    Func("t_caixa", "Maiúsculas e Minúsculas", "Texto",
         lambda v: textfn.maiusculas_minusculas(v["texto"], v["modo"]),
         [Campo("texto", "Texto", "multiline", ""),
          Campo("modo", "Modo", "escolha", "MAIÚSCULAS",
                ["MAIÚSCULAS", "minúsculas", "Primeira Maiúscula", "Título", "iNVERTER"])],
         botao="Aplicar"),
    Func("t_extenso", "Número por Extenso", "Texto", lambda v: textfn.numero_por_extenso(v["numero"]),
         [Campo("numero", "Número", "texto", "")], botao="Escrever"),
    Func("t_acentos", "Remover Acentos do Texto", "Texto", lambda v: textfn.remover_acentos(v["texto"]),
         [Campo("texto", "Texto", "multiline", "")], botao="Remover"),
    Func("t_n", "Remover ou Trocar \\n", "Texto", lambda v: textfn.remover_trocar_n(v["texto"], v["trocar_por"]),
         [Campo("texto", "Texto", "multiline", ""), Campo("trocar_por", "Trocar quebra por", "texto", " ")],
         botao="Aplicar"),

    # ---------------- MATEMÁTICA: CALCULADORAS ----------------
    Func("m_romano", "Conversor de Números Romanos", "Calculadoras", lambda v: mathfn.conversor_romano(v["valor"]),
         [Campo("valor", "Número ou romano", "texto", "")], botao="Converter"),
    Func("m_fatorar", "Fatorar Número", "Calculadoras", lambda v: mathfn.fatorar(v["n"]),
         [Campo("n", "Número", "int", 360)], botao="Fatorar"),
    Func("m_mdc", "MDC", "Calculadoras", lambda v: mathfn.mdc(v["a"], v["b"]),
         [Campo("a", "A", "int", 12), Campo("b", "B", "int", 18)], botao="Calcular"),
    Func("m_mmc", "MMC", "Calculadoras", lambda v: mathfn.mmc(v["a"], v["b"]),
         [Campo("a", "A", "int", 4), Campo("b", "B", "int", 6)], botao="Calcular"),
    Func("m_pct", "Porcentagem", "Calculadoras", lambda v: mathfn.porcentagem(v["valor"], v["percentual"]),
         [Campo("valor", "Valor", "float", 200), Campo("percentual", "Percentual (%)", "float", 15)], botao="Calcular"),
    Func("m_regra3", "Regra de 3 Simples", "Calculadoras", lambda v: mathfn.regra_de_3(v["a"], v["b"], v["c"]),
         [Campo("a", "A", "float", 2), Campo("b", "B", "float", 4), Campo("c", "C", "float", 10)], botao="Calcular"),
    Func("m_resto", "Resto da Divisão", "Calculadoras", lambda v: mathfn.resto_divisao(v["a"], v["b"]),
         [Campo("a", "Dividendo", "int", 17), Campo("b", "Divisor", "int", 5)], botao="Calcular"),

    # ---------------- MATEMÁTICA: ÁREAS ----------------
    Func("a_circulo", "Área do Círculo", "Áreas", lambda v: mathfn.area_circulo(v["raio"]),
         [Campo("raio", "Raio", "float", 5)], botao="Calcular"),
    Func("a_quadrado", "Área do Quadrado", "Áreas", lambda v: mathfn.area_quadrado(v["lado"]),
         [Campo("lado", "Lado", "float", 4)], botao="Calcular"),
    Func("a_retangulo", "Área do Retângulo", "Áreas", lambda v: mathfn.area_retangulo(v["base"], v["altura"]),
         [Campo("base", "Base", "float", 4), Campo("altura", "Altura", "float", 3)], botao="Calcular"),
    Func("a_triangulo", "Área do Triângulo", "Áreas", lambda v: mathfn.area_triangulo(v["base"], v["altura"]),
         [Campo("base", "Base", "float", 6), Campo("altura", "Altura", "float", 4)], botao="Calcular"),
    Func("a_pentagono", "Área do Pentágono", "Áreas", lambda v: mathfn.area_pentagono(v["lado"]),
         [Campo("lado", "Lado", "float", 5)], botao="Calcular"),
    Func("a_hexagono", "Área do Hexágono", "Áreas", lambda v: mathfn.area_hexagono(v["lado"]),
         [Campo("lado", "Lado", "float", 5)], botao="Calcular"),
    Func("a_poligono", "Área do Polígono Regular", "Áreas",
         lambda v: mathfn.area_poligono_regular(v["n_lados"], v["lado"]),
         [Campo("n_lados", "Nº de lados", "int", 8), Campo("lado", "Lado", "float", 5)], botao="Calcular"),
    Func("a_losango", "Área do Losango", "Áreas",
         lambda v: mathfn.area_losango(v["diagonal_maior"], v["diagonal_menor"]),
         [Campo("diagonal_maior", "Diagonal maior", "float", 8), Campo("diagonal_menor", "Diagonal menor", "float", 5)],
         botao="Calcular"),
    Func("a_trapezio", "Área do Trapézio", "Áreas",
         lambda v: mathfn.area_trapezio(v["base_maior"], v["base_menor"], v["altura"]),
         [Campo("base_maior", "Base maior", "float", 8), Campo("base_menor", "Base menor", "float", 4),
          Campo("altura", "Altura", "float", 3)], botao="Calcular"),
    Func("a_paralelogramo", "Área do Paralelogramo", "Áreas",
         lambda v: mathfn.area_paralelogramo(v["base"], v["altura"]),
         [Campo("base", "Base", "float", 6), Campo("altura", "Altura", "float", 4)], botao="Calcular"),
    Func("a_elipse", "Área da Elipse", "Áreas",
         lambda v: mathfn.area_elipse(v["semieixo_a"], v["semieixo_b"]),
         [Campo("semieixo_a", "Semieixo a", "float", 5), Campo("semieixo_b", "Semieixo b", "float", 3)], botao="Calcular"),
    Func("a_coroa", "Área da Coroa Circular", "Áreas",
         lambda v: mathfn.area_coroa_circular(v["raio_maior"], v["raio_menor"]),
         [Campo("raio_maior", "Raio maior", "float", 6), Campo("raio_menor", "Raio menor", "float", 4)], botao="Calcular"),
    Func("a_setor", "Área do Setor Circular", "Áreas",
         lambda v: mathfn.area_setor_circular(v["raio"], v["angulo_graus"]),
         [Campo("raio", "Raio", "float", 5), Campo("angulo_graus", "Ângulo (graus)", "float", 90)], botao="Calcular"),

    # ---------------- DATAS ----------------
    Func("d_entre", "Contador de dias entre datas", "Datas", lambda v: mathfn.dias_entre(v["data1"], v["data2"]),
         [Campo("data1", "Data inicial (dd/mm/aaaa)", "texto", ""), Campo("data2", "Data final (dd/mm/aaaa)", "texto", "")],
         botao="Calcular"),
    Func("d_somar", "Somar Dias em Datas", "Datas", lambda v: mathfn.somar_dias(v["data"], v["dias"]),
         [Campo("data", "Data (dd/mm/aaaa)", "texto", ""), Campo("dias", "Dias a somar", "int", 30)], botao="Somar"),
    Func("d_subtrair", "Subtrair Dias em Datas", "Datas", lambda v: mathfn.subtrair_dias(v["data"], v["dias"]),
         [Campo("data", "Data (dd/mm/aaaa)", "texto", ""), Campo("dias", "Dias a subtrair", "int", 30)], botao="Subtrair"),
]

# ordem das categorias na interface
CATEGORIAS = ["Geradores", "Validadores", "Texto", "Calculadoras", "Áreas", "Datas"]


def por_categoria():
    out = {c: [] for c in CATEGORIAS}
    for f in FUNCS:
        out.setdefault(f.categoria, []).append(f)
    return out
