"""Geradores de dados fictícios (pessoa, empresa, veículo, currículo, etc.) — offline.

Todos os documentos vêm do brdocs (dígitos verificadores corretos). São dados FICTÍCIOS
pra testar sistemas — não pertencem a pessoas ou empresas reais.
"""
from __future__ import annotations

import os
import random
import secrets
import string
import tempfile
import unicodedata
from datetime import date, timedelta

import brdocs
import datasets as D


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.lower() if c.isalnum() or c == ".")


def _signo(d: date) -> str:
    nome = D.SIGNOS[0][0]
    for n, (m, dd) in D.SIGNOS:
        if (d.month, d.day) >= (m, dd):
            nome = n
    return nome


def _idade(nasc: date, hoje: date | None = None) -> int:
    hoje = hoje or date.today()
    return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))


def _data_aleatoria(idade_min: int, idade_max: int) -> date:
    hoje = date.today()
    ini = hoje - timedelta(days=365.25 * (idade_max + 1) - 1)
    fim = hoje - timedelta(days=365.25 * idade_min)
    return ini + timedelta(days=random.randint(0, (fim - ini).days))


def _cidade():
    return random.choice(D.CIDADES_UF)


def _cep(prefixo: str) -> str:
    d = prefixo + "".join(str(random.randint(0, 9)) for _ in range(6))
    return f"{d[:5]}-{d[5:]}"


def _endereco(cid=None) -> tuple[str, str, str, str]:
    cid = cid or _cidade()
    logr = f"{random.choice(D.LOGRADOUROS)} {random.choice(D.NOMES_RUA)}, {random.randint(1, 3999)}"
    return logr, random.choice(D.BAIRROS), f"{cid[0]}/{cid[1]}", _cep(cid[3])


def _celular(ddd: str) -> str:
    return f"({ddd}) 9{random.randint(6000, 9999)}-{random.randint(0, 9999):04d}"


def _fixo(ddd: str) -> str:
    return f"({ddd}) {random.randint(2000, 5999)}-{random.randint(0, 9999):04d}"


def _primeiro(sexo: str) -> tuple[str, str]:
    if sexo not in ("Masculino", "Feminino"):
        sexo = random.choice(["Masculino", "Feminino"])
    return (random.choice(D.NOMES_M if sexo == "Masculino" else D.NOMES_F)), sexo


def _nome_completo(sexo: str = "Aleatório") -> tuple[str, str]:
    p, sexo = _primeiro(sexo)
    s1, s2 = random.sample(D.SOBRENOMES, 2)
    return f"{p} {s1} {s2}", sexo


# ---------------------------------------------------------------- nomes
def gerar_nome(sexo: str = "Aleatório", quantidade: int = 10) -> str:
    try:
        q = max(1, min(int(quantidade), 500))
    except (TypeError, ValueError):
        q = 10
    return "\n".join(_nome_completo(sexo)[0] for _ in range(q))


# ---------------------------------------------------------------- pessoa
def _dados_pessoa(sexo: str = "Aleatório", idade_min=18, idade_max=75) -> dict:
    nome, sexo = _nome_completo(sexo)
    sobren = nome.split()[-2:]
    nasc = _data_aleatoria(idade_min, idade_max)
    cid = _cidade()
    logr, bairro, cidade, cep = _endereco(cid)
    mae = f"{random.choice(D.NOMES_F)} {random.choice(D.SOBRENOMES)} {sobren[0]}"
    pai = f"{random.choice(D.NOMES_M)} {random.choice(D.SOBRENOMES)} {sobren[1]}"
    p = _slug(nome.split()[0])
    email = f"{p}.{_slug(sobren[-1])}{random.randint(1, 99)}@{random.choice(D.DOMINIOS_EMAIL)}"
    altura = random.randint(150, 195) if sexo == "Masculino" else random.randint(148, 182)
    peso = round(random.uniform(55, 105) if sexo == "Masculino" else random.uniform(45, 90), 1)
    return {
        "Nome": nome, "Sexo": sexo, "Idade": f"{_idade(nasc)} anos",
        "Data de nascimento": nasc.strftime("%d/%m/%Y"),
        "CPF": brdocs.gen_cpf(), "RG": brdocs.gen_rg(), "CNH": brdocs.gen_cnh(),
        "PIS": brdocs.gen_pis(), "Título de eleitor": brdocs.gen_titulo(),
        "Mãe": mae, "Pai": pai, "E-mail": email,
        "Senha": gerar_senha(10, simbolos=False),
        "Celular": _celular(cid[2]), "Telefone fixo": _fixo(cid[2]),
        "Endereço": logr, "Bairro": bairro, "Cidade": cidade, "CEP": cep,
        "Altura": f"{altura / 100:.2f} m".replace(".", ","),
        "Peso": f"{peso} kg".replace(".", ","),
        "Tipo sanguíneo": random.choice(D.TIPOS_SANGUE),
        "Signo": _signo(nasc), "Cor favorita": random.choice(D.CORES_FAVORITAS),
    }


def _fmt(d: dict) -> str:
    w = max(len(k) for k in d)
    return "\n".join(f"{k + ':':<{w + 2}}{v}" for k, v in d.items())


def gerar_pessoa(sexo: str = "Aleatório", quantidade: int = 1) -> str:
    try:
        q = max(1, min(int(quantidade), 50))
    except (TypeError, ValueError):
        q = 1
    return ("\n" + "─" * 40 + "\n").join(_fmt(_dados_pessoa(sexo)) for _ in range(q))


# ---------------------------------------------------------------- empresa
def gerar_empresa() -> str:
    nome = f"{random.choice(D.EMPRESA_PALAVRAS)} {random.choice(D.EMPRESA_RAMOS)}"
    abertura = _data_aleatoria(1, 40)
    cid = _cidade()
    logr, bairro, cidade, cep = _endereco(cid)
    dom = _slug(nome.replace(" ", ""))
    return _fmt({
        "Razão social": f"{nome} {random.choice(D.EMPRESA_TIPOS)}",
        "Nome fantasia": nome,
        "CNPJ": brdocs.gen_cnpj(),
        "Inscrição estadual (SP)": brdocs.gen_ie_sp(),
        "Data de abertura": abertura.strftime("%d/%m/%Y"),
        "Site": f"www.{dom}.com.br",
        "E-mail": f"contato@{dom}.com.br",
        "Telefone": _fixo(cid[2]),
        "Celular": _celular(cid[2]),
        "Endereço": logr, "Bairro": bairro, "Cidade": cidade, "CEP": cep,
    })


# ---------------------------------------------------------------- veículo
def gerar_veiculo() -> str:
    marca = random.choice(list(D.MARCAS_MODELOS))
    cid = _cidade()
    return _fmt({
        "Marca": marca,
        "Modelo": random.choice(D.MARCAS_MODELOS[marca]),
        "Ano": random.randint(1995, date.today().year),
        "Cor": random.choice(D.CORES),
        "Combustível": random.choice(D.COMBUSTIVEIS),
        "Placa": brdocs.gen_placa(True),
        "RENAVAM": brdocs.gen_renavam(),
        "Cidade": f"{cid[0]}/{cid[1]}",
    })


def gerar_placa(tipo: str = "Mercosul", quantidade: int = 5) -> str:
    try:
        q = max(1, min(int(quantidade), 500))
    except (TypeError, ValueError):
        q = 5
    merc = tipo != "Antiga (cinza)"
    return "\n".join(brdocs.gen_placa(merc) for _ in range(q))


# ---------------------------------------------------------------- currículo
def gerar_curriculo() -> str:
    p = _dados_pessoa(idade_min=22, idade_max=55)
    nasc_ano = int(p["Data de nascimento"][-4:])
    cargo = random.choice(D.CARGOS)
    formatura = nasc_ano + random.randint(21, 25)
    hoje = date.today().year
    exps = []
    ano = max(formatura, hoje - random.randint(4, 15))
    for i in range(random.randint(2, 3)):
        fim = min(hoje, ano + random.randint(1, 5))
        emp = f"{random.choice(D.EMPRESA_PALAVRAS)} {random.choice(D.EMPRESA_RAMOS)}"
        periodo = f"{ano} – {'atual' if fim >= hoje else fim}"
        exps.append(f"  • {periodo}  {emp}\n    Cargo: {random.choice(D.CARGOS)}")
        ano = fim
        if fim >= hoje:
            break
    idiomas = random.sample(D.IDIOMAS, random.randint(1, 2))
    linhas = [
        p["Nome"].upper(),
        f"{p['Idade']} · {p['Cidade']} · {p['Celular']} · {p['E-mail']}",
        "",
        "OBJETIVO",
        f"  Atuar como {cargo}, contribuindo com dedicação e crescimento profissional.",
        "",
        "FORMAÇÃO",
        f"  • {random.choice(D.CURSOS)} — {random.choice(D.FACULDADES)} (concluído em {min(formatura, hoje)})",
        "",
        "EXPERIÊNCIA PROFISSIONAL",
        *exps,
        "",
        "HABILIDADES",
        "  " + ", ".join(random.sample(D.HABILIDADES, 5)),
        "",
        "IDIOMAS",
        *[f"  • {i} {random.choice(D.NIVEIS_IDIOMA)}" for i in idiomas],
    ]
    return "\n".join(linhas)


# ---------------------------------------------------------------- nicks
_LEET = str.maketrans({"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"})


def gerar_nicks(quantidade: int = 10) -> str:
    try:
        q = max(1, min(int(quantidade), 200))
    except (TypeError, ValueError):
        q = 10
    out = []
    for _ in range(q):
        a, s = random.choice(D.NICK_ADJ), random.choice(D.NICK_SUB)
        estilo = random.randint(0, 4)
        if estilo == 0:
            n = f"{a}{s}{random.randint(1, 999)}"
        elif estilo == 1:
            n = f"xX{a}{s}Xx"
        elif estilo == 2:
            n = f"{a}_{s}".translate(_LEET)
        elif estilo == 3:
            n = f"{s}{random.choice(['BR', 'Gamer', 'TV', 'YT', 'Pro'])}"
        else:
            n = f"{a.lower()}.{s.lower()}{random.randint(10, 99)}"
        out.append(unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode())
    return "\n".join(out)


# ---------------------------------------------------------------- lorem
_LOREM = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
          "incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud "
          "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure "
          "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur "
          "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt "
          "mollit anim id est laborum curabitur pretium tincidunt lacus nulla gravida orci a odio "
          "nullam varius turpis et commodo pharetra est eros bibendum elit nec luctus magna felis "
          "sollicitudin mauris integer in mauris eu nibh euismod gravida").split()


def gerar_lorem(paragrafos: int = 3) -> str:
    try:
        n = max(1, min(int(paragrafos), 50))
    except (TypeError, ValueError):
        n = 3
    ps = []
    for i in range(n):
        frases = []
        for _ in range(random.randint(4, 7)):
            w = random.choices(_LOREM, k=random.randint(6, 14))
            frases.append(" ".join(w).capitalize() + ".")
        if i == 0:
            frases[0] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        ps.append(" ".join(frases))
    return "\n\n".join(ps)


# ---------------------------------------------------------------- senha
def gerar_senha(tamanho: int = 12, maiusculas: bool = True, minusculas: bool = True,
                numeros: bool = True, simbolos: bool = True) -> str:
    try:
        t = max(4, min(int(tamanho), 256))
    except (TypeError, ValueError):
        t = 12
    grupos = []
    if maiusculas:
        grupos.append(string.ascii_uppercase)
    if minusculas:
        grupos.append(string.ascii_lowercase)
    if numeros:
        grupos.append(string.digits)
    if simbolos:
        grupos.append("!@#$%&*()-_=+[]{};:,.?/")
    if not grupos:
        return "Erro: marque pelo menos um tipo de caractere."
    senha = [secrets.choice(g) for g in grupos]  # garante 1 de cada
    todos = "".join(grupos)
    senha += [secrets.choice(todos) for _ in range(t - len(senha))]
    secrets.SystemRandom().shuffle(senha)
    return "".join(senha)


# ---------------------------------------------------------------- números
def numeros_aleatorios(quantidade: int = 10, minimo: int = 1, maximo: int = 100) -> str:
    try:
        q, a, b = int(quantidade), int(minimo), int(maximo)
    except (TypeError, ValueError):
        return "Erro: use números inteiros."
    if a > b:
        a, b = b, a
    q = max(1, min(q, 10000))
    return "\n".join(str(random.randint(a, b)) for _ in range(q))


def sorteador(quantidade: int = 6, de: int = 1, ate: int = 60) -> str:
    try:
        q, a, b = int(quantidade), int(de), int(ate)
    except (TypeError, ValueError):
        return "Erro: use números inteiros."
    if a > b:
        a, b = b, a
    if q < 1 or q > b - a + 1:
        return f"Erro: não dá pra sortear {q} números diferentes entre {a} e {b}."
    nums = sorted(random.SystemRandom().sample(range(a, b + 1), q))
    return "Números sorteados:\n" + "  ".join(f"{n:02d}" for n in nums)


# ---------------------------------------------------------------- símbolos
SIMBOLOS = {
    "Setas": "← ↑ → ↓ ↔ ↕ ⇐ ⇑ ⇒ ⇓ ⇔ ➔ ➜ ➤ ⟵ ⟶ ↩ ↪ ↺ ↻ ⬅ ⬆ ⬇ ➡",
    "Estrelas e formas": "★ ☆ ✦ ✧ ✩ ✪ ✯ ✰ ● ○ ◆ ◇ ■ □ ▲ △ ▼ ▽ ◀ ▶ ♦ ♢ ⬤ ◉",
    "Corações e cartas": "♥ ♡ ❤ ❥ ❣ ♠ ♤ ♣ ♧ ♦ ♢",
    "Checks e marcações": "✓ ✔ ✗ ✘ ☐ ☑ ☒ ⊠ ⊗ ⊕ ※ ‼ ⁉",
    "Moedas": "R$ $ € £ ¥ ¢ ₿ ₹ ₽ ₩ ₪ ¤",
    "Matemática": "± × ÷ ≈ ≠ ≤ ≥ ∞ √ ∑ ∏ ∫ ∂ ∆ π µ ° ‰ ¼ ½ ¾ ² ³ ¹ ∈ ∉ ∩ ∪ ⊂ ⊃ ∀ ∃ ¬ ∧ ∨",
    "Letras gregas": "α β γ δ ε ζ η θ λ μ ξ π ρ σ τ φ χ ψ ω Ω Σ Δ Φ Ψ",
    "Pontuação e tipografia": "« » “ ” ‘ ’ „ … — – • · ¶ § † ‡ © ® ™ ℠ ¿ ¡ º ª",
    "Clima e natureza": "☀ ☁ ☂ ☃ ☄ ⚡ ❄ ☘ ✿ ❀ ❁ ✾ ☽ ☾",
    "Música": "♩ ♪ ♫ ♬ ♭ ♮ ♯",
    "Caixas (desenho)": "─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬ ░ ▒ ▓ █",
    "Diversos": "☎ ✉ ✂ ✏ ✒ ⌚ ⌛ ☕ ⚓ ⚙ ⚠ ☢ ☣ ☮ ☯ ♻ ⚽ ⚾ ✈ ♀ ♂ ⚥",
}


def simbolos() -> str:
    return "\n\n".join(f"{k}:\n{v}" for k, v in SIMBOLOS.items())


# ---------------------------------------------------------------- imagem
def gerar_imagem(largura: int = 600, altura: int = 400, texto: str = "", pasta: str | None = None) -> str:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return "Erro: Pillow não disponível"
    try:
        w, h = max(10, min(int(largura), 8000)), max(10, min(int(altura), 8000))
    except (TypeError, ValueError):
        return "Erro: largura e altura devem ser números."
    cor = tuple(random.randint(0, 255) for _ in range(3))
    lum = 0.299 * cor[0] + 0.587 * cor[1] + 0.114 * cor[2]
    cor_txt = (20, 20, 20) if lum > 140 else (245, 245, 245)
    img = Image.new("RGB", (w, h), cor)
    dr = ImageDraw.Draw(img)
    txt = texto.strip() or f"{w}x{h}"
    tam = max(10, min(w, h) // 6)
    try:
        fonte = ImageFont.truetype("segoeui.ttf", tam)
    except Exception:
        try:
            fonte = ImageFont.truetype("arial.ttf", tam)
        except Exception:
            fonte = ImageFont.load_default()
    box = dr.textbbox((0, 0), txt, font=fonte)
    tw, th = box[2] - box[0], box[3] - box[1]
    dr.text(((w - tw) / 2 - box[0], (h - th) / 2 - box[1]), txt, fill=cor_txt, font=fonte)
    if not pasta:
        pics = os.path.join(os.path.expanduser("~"), "Pictures")
        pasta = os.path.join(pics, "Imagens Geradas") if os.path.isdir(pics) else tempfile.gettempdir()
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"imagem_{w}x{h}_{random.randint(1000, 9999)}.png")
    img.save(caminho)
    return caminho
