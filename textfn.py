"""Funções de texto (estilo 4Devs "Funções String") — offline, só biblioteca padrão.

Toda função devolve uma str pronta pra mostrar ao usuário.
"""
from __future__ import annotations

import html
import re
import unicodedata


# 1 ---------------------------------------------------------------
def remover_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# 2 ---------------------------------------------------------------
def inverter_texto(texto: str) -> str:
    return texto[::-1]


# 3 ---------------------------------------------------------------
MODOS_CAIXA = ["MAIÚSCULAS", "minúsculas", "Primeira Maiúscula", "Título", "iNVERTER"]


def _primeira_maiuscula(texto: str) -> str:
    out = []
    capitalizar = True
    for ch in texto.lower():
        if capitalizar and ch.isalpha():
            out.append(ch.upper())
            capitalizar = False
        else:
            out.append(ch)
        if ch in ".!?\n":
            capitalizar = True
    return "".join(out)


def _titulo(texto: str) -> str:
    return re.sub(r"\w+", lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), texto)


def maiusculas_minusculas(texto: str, modo: str) -> str:
    if modo == "MAIÚSCULAS":
        return texto.upper()
    if modo == "minúsculas":
        return texto.lower()
    if modo == "Primeira Maiúscula":
        return _primeira_maiuscula(texto)
    if modo == "Título":
        return _titulo(texto)
    if modo == "iNVERTER":
        return texto.swapcase()
    return texto


# 4 ---------------------------------------------------------------
def contar_caracteres(texto: str) -> str:
    total = len(texto)
    sem_espacos = len(re.sub(r"\s", "", texto))
    palavras = len(re.findall(r"\w+", texto))
    linhas = len(texto.splitlines()) if texto else 0
    paragrafos = len([p for p in re.split(r"\n\s*\n", texto) if p.strip()])
    return (f"Caracteres: {total}\n"
            f"Caracteres sem espaços: {sem_espacos}\n"
            f"Palavras: {palavras}\n"
            f"Linhas: {linhas}\n"
            f"Parágrafos: {paragrafos}")


# 5 ---------------------------------------------------------------
def contar_ocorrencias(texto: str, palavra: str) -> str:
    palavra = palavra.strip()
    if not palavra:
        return "Digite a palavra que quer contar."
    n = len(re.findall(r"(?<!\w)" + re.escape(palavra) + r"(?!\w)", texto, flags=re.IGNORECASE))
    vez = "vez" if n == 1 else "vezes"
    return f'A palavra "{palavra}" aparece {n} {vez} no texto.'


# 6 ---------------------------------------------------------------
def ordem_alfabetica(texto: str, reverso: bool = False) -> str:
    linhas = [l for l in texto.splitlines() if l.strip()]
    linhas.sort(key=lambda s: remover_acentos(s).casefold(), reverse=reverso)
    return "\n".join(linhas)


# 7 ---------------------------------------------------------------
def texto_para_html(texto: str) -> str:
    esc = html.escape(texto, quote=True)
    esc = esc.replace("\r\n", "\n")
    return esc.replace("\n", "<br>\n")


# 8 ---------------------------------------------------------------
def cortar_texto(texto: str, inicio: int, fim: int) -> str:
    try:
        i, f = int(inicio), int(fim)
    except (TypeError, ValueError):
        return "Erro: início e fim devem ser números."
    return texto[i:f]


# 9 ---------------------------------------------------------------
def dividir_string(texto: str, separador: str) -> str:
    partes = texto.split(separador) if separador else texto.split()
    return "\n".join(f"{i}: {p}" for i, p in enumerate(partes, 1))


# 10 --------------------------------------------------------------
def info_caractere(texto: str) -> str:
    if not texto:
        return "Digite um ou mais caracteres."
    linhas = []
    for ch in texto[:50]:
        nome = unicodedata.name(ch, "?")
        mostra = repr(ch) if ch.isspace() else ch
        linhas.append(f"{mostra}   decimal {ord(ch)}   U+{ord(ch):04X}   {nome}")
    if len(texto) > 50:
        linhas.append(f"... (mostrando só os 50 primeiros de {len(texto)})")
    return "\n".join(linhas)


# 11 --------------------------------------------------------------
_UNI = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
        "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete",
        "dezoito", "dezenove"]
_DEZ = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta",
        "oitenta", "noventa"]
_CEN = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos",
        "setecentos", "oitocentos", "novecentos"]
_ESCALAS = [("", ""), ("mil", "mil"), ("milhão", "milhões"), ("bilhão", "bilhões"),
            ("trilhão", "trilhões")]


def _ate_999(n: int) -> str:
    if n == 0:
        return ""
    if n == 100:
        return "cem"
    c, resto = divmod(n, 100)
    partes = []
    if c:
        partes.append(_CEN[c])
    if resto:
        if resto < 20:
            partes.append(_UNI[resto])
        else:
            d, u = divmod(resto, 10)
            partes.append(_DEZ[d] + (f" e {_UNI[u]}" if u else ""))
    return " e ".join(partes)


def numero_por_extenso(numero) -> str:
    try:
        n = int(str(numero).strip().replace(".", "").replace(" ", ""))
    except (TypeError, ValueError):
        return "Erro: digite um número inteiro."
    if abs(n) >= 10 ** 15:
        return "Erro: o limite é 999 trilhões."
    if n == 0:
        return "zero"
    negativo = n < 0
    n = abs(n)
    grupos = []
    while n:
        n, g = divmod(n, 1000)
        grupos.append(g)
    pedacos = []  # (texto, valor_do_grupo)
    for i in range(len(grupos) - 1, -1, -1):
        g = grupos[i]
        if not g:
            continue
        if i == 0:
            txt = _ate_999(g)
        elif i == 1:
            txt = "mil" if g == 1 else f"{_ate_999(g)} mil"
        else:
            sing, plur = _ESCALAS[i]
            txt = f"{_ate_999(g)} {sing if g == 1 else plur}"
        pedacos.append((txt, g))
    # Regra do "e": antes do último grupo se ele for < 100 ou centena exata
    out = pedacos[0][0]
    for idx in range(1, len(pedacos)):
        txt, g = pedacos[idx]
        ultimo = idx == len(pedacos) - 1
        if ultimo and (g < 100 or g % 100 == 0):
            out += " e " + txt
        else:
            out += " " + txt
    return ("menos " if negativo else "") + out


# 12 --------------------------------------------------------------
def remover_trocar_n(texto: str, trocar_por: str = " ") -> str:
    return texto.replace("\r\n", "\n").replace("\r", "\n").replace("\n", trocar_por)


# 13 --------------------------------------------------------------
ESTILOS_LETRAS = ["Negrito", "Itálico", "Script", "Monoespaçado", "Bolha", "Quadrado",
                  "Invertido", "Largo (fullwidth)"]

_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LO = "abcdefghijklmnopqrstuvwxyz"
_DG = "0123456789"

# exceções do bloco Mathematical Alphanumeric (letras que já existiam em outro lugar)
_ITALIC_EXC = {"h": "ℎ"}
_SCRIPT_EXC = {"B": "ℬ", "E": "ℰ", "F": "ℱ", "H": "ℋ", "I": "ℐ", "L": "ℒ", "M": "ℳ",
               "R": "ℛ", "e": "ℯ", "g": "ℊ", "o": "ℴ"}

_INVERT = dict(zip(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'\"()[]{}<>_&",
    "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀ꓭƆꓷƎℲ⅁HIſꓘ˥WNOԀῸꓤS⊥∩ΛMX⅄Z0ƖᄅƐㄣϛ9ㄥ86˙'¡¿,„)(][}{><‾⅋"))


def _math(ch: str, up: int, lo: int, dg: int | None, exc: dict | None = None) -> str:
    if exc and ch in exc:
        return exc[ch]
    if ch in _UP:
        return chr(up + _UP.index(ch))
    if ch in _LO:
        return chr(lo + _LO.index(ch))
    if dg is not None and ch in _DG:
        return chr(dg + _DG.index(ch))
    return ch


def _bolha(ch: str) -> str:
    if ch in _UP:
        return chr(0x24B6 + _UP.index(ch))
    if ch in _LO:
        return chr(0x24D0 + _LO.index(ch))
    if ch == "0":
        return "⓪"
    if ch in "123456789":
        return chr(0x2460 + int(ch) - 1)
    return ch


def _quadrado(ch: str) -> str:
    c = ch.upper()
    if c in _UP:
        return chr(0x1F130 + _UP.index(c))
    return ch


def _largo(ch: str) -> str:
    if 0x21 <= ord(ch) <= 0x7E:
        return chr(ord(ch) + 0xFEE0)
    if ch == " ":
        return "　"
    return ch


def letras_personalizadas(texto: str, estilo: str) -> str:
    texto = remover_acentos(texto)
    if estilo == "Negrito":
        f = lambda c: _math(c, 0x1D400, 0x1D41A, 0x1D7CE)
    elif estilo == "Itálico":
        f = lambda c: _math(c, 0x1D434, 0x1D44E, None, _ITALIC_EXC)
    elif estilo == "Script":
        f = lambda c: _math(c, 0x1D49C, 0x1D4B6, None, _SCRIPT_EXC)
    elif estilo == "Monoespaçado":
        f = lambda c: _math(c, 0x1D670, 0x1D68A, 0x1D7F6)
    elif estilo == "Bolha":
        f = _bolha
    elif estilo == "Quadrado":
        f = _quadrado
    elif estilo == "Invertido":
        return "".join(_INVERT.get(c, c) for c in reversed(texto))
    elif estilo == "Largo (fullwidth)":
        f = _largo
    else:
        return texto
    return "".join(f(c) for c in texto)


def letras_diferentes(texto: str) -> str:
    """Mostra o texto em todos os estilos (Gerador de Letras Diferentes)."""
    if not texto.strip():
        texto = "Caixa de Ferramentas"
    return "\n\n".join(f"{e}:\n{letras_personalizadas(texto, e)}" for e in ESTILOS_LETRAS)


# 14 --------------------------------------------------------------
def _checagem_leve(texto: str) -> list[str]:
    avisos = []
    for m in re.finditer(r"\b(\w+)\s+\1\b", texto, flags=re.IGNORECASE):
        avisos.append(f'Palavra repetida em sequência: "{m.group(0)}"')
    if re.search(r"[^\S\n]{2,}", texto):
        avisos.append("Há espaços duplos no texto.")
    for m in re.finditer(r"([!?.,;:])\1+", texto):
        if m.group(0) != "...":
            avisos.append(f'Pontuação repetida: "{m.group(0)}"')
    for m in re.finditer(r"\s+([,.;:!?])", texto):
        avisos.append(f'Espaço antes da pontuação: "{m.group(0).strip()}"')
    return avisos


def corretor_ortografico(texto: str) -> str:
    if not texto.strip():
        return "Digite um texto pra corrigir."
    linhas = []
    try:
        from spellchecker import SpellChecker  # pyspellchecker
        sp = SpellChecker(language="pt")
        palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto)
        desconhecidas = sp.unknown([p.lower() for p in palavras if len(p) > 1])
        vistos = set()
        for p in palavras:
            pl = p.lower()
            if pl in desconhecidas and pl not in vistos:
                vistos.add(pl)
                sug = sp.correction(pl)
                linhas.append(f"✗ {p}  →  {sug}" if sug and sug != pl else f"✗ {p}  (sem sugestão)")
        if not linhas:
            linhas.append("✓ Nenhum erro de ortografia encontrado.")
    except Exception:
        linhas.append("(Dicionário de português não instalado — fazendo checagem básica.)")
    extras = _checagem_leve(texto)
    if extras:
        linhas.append("")
        linhas.extend(extras)
    return "\n".join(linhas)
