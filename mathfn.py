"""Modulo de funcoes matematicas em portugues (estilo secao "Matematica" do 4Devs).

Python 3.13, apenas biblioteca padrao, sem interface grafica.
Todas as funcoes retornam uma string legivel para humanos.
Em caso de entrada invalida, retornam uma mensagem amigavel comecando com "Erro:".
"""

import math
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------


def _fmt(numero):
    """Formata um numero arredondando para 4 casas e removendo zeros a direita."""
    try:
        valor = round(float(numero), 4)
    except (TypeError, ValueError):
        return str(numero)
    if valor == int(valor):
        return str(int(valor))
    texto = f"{valor:.4f}".rstrip("0").rstrip(".")
    return texto


def _para_int(x):
    """Converte para int aceitando int, float inteiro ou string numerica."""
    if isinstance(x, bool):
        raise ValueError("valor booleano")
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        if x != int(x):
            raise ValueError("nao e inteiro")
        return int(x)
    if isinstance(x, str):
        return int(x.strip())
    raise ValueError("tipo invalido")


def _para_float(x):
    """Converte para float aceitando int, float ou string (virgula ou ponto)."""
    if isinstance(x, bool):
        raise ValueError("valor booleano")
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        return float(x.strip().replace(",", "."))
    raise ValueError("tipo invalido")


# ---------------------------------------------------------------------------
# CALCULADORAS
# ---------------------------------------------------------------------------

_ROMANOS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_ROMANO_VALOR = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def _int_para_romano(n):
    resultado = []
    for valor, simbolo in _ROMANOS:
        while n >= valor:
            resultado.append(simbolo)
            n -= valor
    return "".join(resultado)


def _romano_para_int(texto):
    total = 0
    anterior = 0
    for caractere in reversed(texto):
        atual = _ROMANO_VALOR[caractere]
        if atual < anterior:
            total -= atual
        else:
            total += atual
            anterior = atual
    return total


def conversor_romano(valor: str) -> str:
    """Converte entre numero decimal (1..3999) e algarismo romano."""
    texto = str(valor).strip()
    if texto == "":
        return "Erro: informe um numero (1 a 3999) ou algarismos romanos"

    # Caso decimal
    if texto.lstrip("+-").isdigit():
        try:
            numero = int(texto)
        except ValueError:
            return "Erro: valor invalido"
        if numero < 1 or numero > 3999:
            return "Erro: o numero deve estar entre 1 e 3999"
        return f"{numero} = {_int_para_romano(numero)}"

    # Caso romano
    letras = texto.upper()
    if all(c in _ROMANO_VALOR for c in letras):
        numero = _romano_para_int(letras)
        # Valida ida e volta para evitar romanos malformados
        if _int_para_romano(numero) != letras:
            return "Erro: algarismo romano invalido"
        return f"{letras} = {numero}"

    return "Erro: informe um numero (1 a 3999) ou algarismos romanos validos"


def fatorar(n) -> str:
    """Fatoracao em numeros primos de um inteiro n >= 2."""
    try:
        numero = _para_int(n)
    except (ValueError, TypeError):
        return "Erro: informe um numero inteiro"
    if numero < 2:
        return "Erro: informe um numero inteiro maior ou igual a 2"

    original = numero
    fatores = []
    divisor = 2
    while divisor * divisor <= numero:
        expoente = 0
        while numero % divisor == 0:
            numero //= divisor
            expoente += 1
        if expoente > 0:
            fatores.append((divisor, expoente))
        divisor += 1 if divisor == 2 else 2
    if numero > 1:
        fatores.append((numero, 1))

    partes = []
    for base, expoente in fatores:
        if expoente == 1:
            partes.append(str(base))
        else:
            partes.append(f"{base}^{expoente}")
    return f"{original} = " + " x ".join(partes)


def mdc(a, b) -> str:
    """Maximo divisor comum entre a e b."""
    try:
        x = _para_int(a)
        y = _para_int(b)
    except (ValueError, TypeError):
        return "Erro: informe dois numeros inteiros"
    resultado = math.gcd(x, y)
    return f"MDC({x}, {y}) = {resultado}"


def mmc(a, b) -> str:
    """Minimo multiplo comum entre a e b."""
    try:
        x = _para_int(a)
        y = _para_int(b)
    except (ValueError, TypeError):
        return "Erro: informe dois numeros inteiros"
    resultado = math.lcm(x, y)
    return f"MMC({x}, {y}) = {resultado}"


def porcentagem(valor: float, percentual: float) -> str:
    """Calcula o percentual de um valor."""
    try:
        v = _para_float(valor)
        p = _para_float(percentual)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    resultado = v * p / 100
    return f"{_fmt(p)}% de {_fmt(v)} = {_fmt(resultado)}"


def regra_de_3(a: float, b: float, c: float) -> str:
    """Resolve a regra de tres simples: a/b = c/x  ->  x = b*c/a."""
    try:
        va = _para_float(a)
        vb = _para_float(b)
        vc = _para_float(c)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if va == 0:
        return "Erro: o primeiro valor nao pode ser zero"
    x = vb * vc / va
    return f"{_fmt(va)}/{_fmt(vb)} = {_fmt(vc)}/x -> x = {_fmt(x)}"


def resto_divisao(a: int, b: int) -> str:
    """Quociente e resto da divisao de a por b."""
    try:
        x = _para_int(a)
        y = _para_int(b)
    except (ValueError, TypeError):
        return "Erro: informe dois numeros inteiros"
    if y == 0:
        return "Erro: divisao por zero"
    quociente = x // y
    resto = x % y
    return f"{x} = {y}*{quociente} + {resto} (quociente = {quociente}, resto = {resto})"


# ---------------------------------------------------------------------------
# AREAS
# ---------------------------------------------------------------------------


def area_circulo(raio: float) -> str:
    try:
        r = _para_float(raio)
    except (ValueError, TypeError):
        return "Erro: informe um numero valido"
    if r < 0:
        return "Erro: o raio nao pode ser negativo"
    return f"Area do circulo = {_fmt(math.pi * r * r)}"


def area_quadrado(lado: float) -> str:
    try:
        lado_v = _para_float(lado)
    except (ValueError, TypeError):
        return "Erro: informe um numero valido"
    if lado_v < 0:
        return "Erro: o lado nao pode ser negativo"
    return f"Area do quadrado = {_fmt(lado_v * lado_v)}"


def area_retangulo(base: float, altura: float) -> str:
    try:
        b = _para_float(base)
        h = _para_float(altura)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if b < 0 or h < 0:
        return "Erro: as medidas nao podem ser negativas"
    return f"Area do retangulo = {_fmt(b * h)}"


def area_triangulo(base: float, altura: float) -> str:
    try:
        b = _para_float(base)
        h = _para_float(altura)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if b < 0 or h < 0:
        return "Erro: as medidas nao podem ser negativas"
    return f"Area do triangulo = {_fmt(b * h / 2)}"


def area_pentagono(lado: float) -> str:
    try:
        lado_v = _para_float(lado)
    except (ValueError, TypeError):
        return "Erro: informe um numero valido"
    if lado_v < 0:
        return "Erro: o lado nao pode ser negativo"
    area = (5 * lado_v * lado_v) / (4 * math.tan(math.pi / 5))
    return f"Area do pentagono = {_fmt(area)}"


def area_hexagono(lado: float) -> str:
    try:
        lado_v = _para_float(lado)
    except (ValueError, TypeError):
        return "Erro: informe um numero valido"
    if lado_v < 0:
        return "Erro: o lado nao pode ser negativo"
    area = (3 * math.sqrt(3) / 2) * lado_v * lado_v
    return f"Area do hexagono = {_fmt(area)}"


def area_poligono_regular(n_lados: int, lado: float) -> str:
    try:
        n = _para_int(n_lados)
        lado_v = _para_float(lado)
    except (ValueError, TypeError):
        return "Erro: informe valores validos"
    if n < 3:
        return "Erro: o poligono precisa de pelo menos 3 lados"
    if lado_v < 0:
        return "Erro: o lado nao pode ser negativo"
    area = (n * lado_v * lado_v) / (4 * math.tan(math.pi / n))
    return f"Area do poligono regular = {_fmt(area)}"


def area_losango(diagonal_maior: float, diagonal_menor: float) -> str:
    try:
        d_maior = _para_float(diagonal_maior)
        d_menor = _para_float(diagonal_menor)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if d_maior < 0 or d_menor < 0:
        return "Erro: as diagonais nao podem ser negativas"
    return f"Area do losango = {_fmt(d_maior * d_menor / 2)}"


def area_trapezio(base_maior: float, base_menor: float, altura: float) -> str:
    try:
        b_maior = _para_float(base_maior)
        b_menor = _para_float(base_menor)
        h = _para_float(altura)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if b_maior < 0 or b_menor < 0 or h < 0:
        return "Erro: as medidas nao podem ser negativas"
    return f"Area do trapezio = {_fmt((b_maior + b_menor) * h / 2)}"


def area_paralelogramo(base: float, altura: float) -> str:
    try:
        b = _para_float(base)
        h = _para_float(altura)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if b < 0 or h < 0:
        return "Erro: as medidas nao podem ser negativas"
    return f"Area do paralelogramo = {_fmt(b * h)}"


def area_elipse(semieixo_a: float, semieixo_b: float) -> str:
    try:
        a = _para_float(semieixo_a)
        b = _para_float(semieixo_b)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if a < 0 or b < 0:
        return "Erro: os semieixos nao podem ser negativos"
    return f"Area da elipse = {_fmt(math.pi * a * b)}"


def area_coroa_circular(raio_maior: float, raio_menor: float) -> str:
    try:
        r_maior = _para_float(raio_maior)
        r_menor = _para_float(raio_menor)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if r_maior < 0 or r_menor < 0:
        return "Erro: os raios nao podem ser negativos"
    if r_menor > r_maior:
        return "Erro: o raio menor nao pode ser maior que o raio maior"
    return f"Area da coroa circular = {_fmt(math.pi * (r_maior * r_maior - r_menor * r_menor))}"


def area_setor_circular(raio: float, angulo_graus: float) -> str:
    try:
        r = _para_float(raio)
        angulo = _para_float(angulo_graus)
    except (ValueError, TypeError):
        return "Erro: informe numeros validos"
    if r < 0:
        return "Erro: o raio nao pode ser negativo"
    return f"Area do setor circular = {_fmt(math.pi * r * r * angulo / 360)}"


# ---------------------------------------------------------------------------
# DATAS
# ---------------------------------------------------------------------------

_FORMATO_DATA = "%d/%m/%Y"


def _parse_data(texto):
    return datetime.strptime(str(texto).strip(), _FORMATO_DATA)


def dias_entre(data1: str, data2: str) -> str:
    """Numero absoluto de dias entre duas datas."""
    try:
        d1 = _parse_data(data1)
        d2 = _parse_data(data2)
    except (ValueError, TypeError):
        return "Erro: data invalida (use dd/mm/aaaa)"
    dias = abs((d2 - d1).days)
    return f"Dias entre {data1} e {data2} = {dias}"


def somar_dias(data: str, dias: int) -> str:
    """Soma uma quantidade de dias a uma data."""
    try:
        base = _parse_data(data)
        quantidade = _para_int(dias)
    except (ValueError, TypeError):
        return "Erro: data invalida (use dd/mm/aaaa)"
    resultado = base + timedelta(days=quantidade)
    return resultado.strftime(_FORMATO_DATA)


def subtrair_dias(data: str, dias: int) -> str:
    """Subtrai uma quantidade de dias de uma data."""
    try:
        base = _parse_data(data)
        quantidade = _para_int(dias)
    except (ValueError, TypeError):
        return "Erro: data invalida (use dd/mm/aaaa)"
    resultado = base - timedelta(days=quantidade)
    return resultado.strftime(_FORMATO_DATA)
