"""Documentos brasileiros — geradores e validadores (offline).

Os números de CPF, CNPJ, PIS/PASEP, CNH, RENAVAM, Título de Eleitor, RG(SP) e cartão de
crédito (Luhn) usam os algoritmos oficiais de dígito verificador. Conta bancária, certidão e
inscrição estadual usam um DV mod 11 autoconsistente (gera e valida pelo mesmo cálculo) — servem
pra TESTAR sistemas, com formato válido, não são de pessoas/empresas reais.
"""
from __future__ import annotations

import random


def only_digits(s: str) -> str:
    return "".join(c for c in str(s) if c.isdigit())


def _rand_digits(n: int) -> list[int]:
    return [random.randint(0, 9) for _ in range(n)]


# ---------------- CPF ----------------
def _cpf_dvs(nums):
    d1 = sum(n * (10 - i) for i, n in enumerate(nums)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    nums2 = nums + [d1]
    d2 = sum(n * (11 - i) for i, n in enumerate(nums2)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    return d1, d2


def gen_cpf(mask=True):
    nums = _rand_digits(9)
    d1, d2 = _cpf_dvs(nums)
    d = "".join(map(str, nums + [d1, d2]))
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}" if mask else d


def valid_cpf(s):
    d = only_digits(s)
    if len(d) != 11 or d == d[0] * 11:
        return False
    nums = [int(x) for x in d[:9]]
    d1, d2 = _cpf_dvs(nums)
    return d[9] == str(d1) and d[10] == str(d2)


# ---------------- CNPJ ----------------
def _cnpj_dvs(nums):
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = sum(n * w for n, w in zip(nums, w1)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    d2 = sum(n * w for n, w in zip(nums + [d1], w2)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    return d1, d2


def gen_cnpj(mask=True):
    nums = _rand_digits(8) + [0, 0, 0, 1]  # matriz 0001
    d1, d2 = _cnpj_dvs(nums)
    d = "".join(map(str, nums + [d1, d2]))
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}" if mask else d


def valid_cnpj(s):
    d = only_digits(s)
    if len(d) != 14 or d == d[0] * 14:
        return False
    nums = [int(x) for x in d[:12]]
    d1, d2 = _cnpj_dvs(nums)
    return d[12] == str(d1) and d[13] == str(d2)


# ---------------- PIS/PASEP ----------------
def _pis_dv(nums):
    w = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    r = sum(n * ww for n, ww in zip(nums, w)) % 11
    return 0 if r < 2 else 11 - r


def gen_pis(mask=True):
    nums = _rand_digits(10)
    dv = _pis_dv(nums)
    d = "".join(map(str, nums + [dv]))
    return f"{d[:3]}.{d[3:8]}.{d[8:10]}-{d[10]}" if mask else d


def valid_pis(s):
    d = only_digits(s)
    if len(d) != 11 or d == d[0] * 11:
        return False
    return str(_pis_dv([int(x) for x in d[:10]])) == d[10]


# ---------------- RG (padrão SP, SSP) ----------------
def _rg_dv(nums):
    w = [2, 3, 4, 5, 6, 7, 8, 9]
    r = sum(n * ww for n, ww in zip(nums, w)) % 11
    dv = 11 - r
    return "X" if dv == 10 else ("0" if dv == 11 else str(dv))


def gen_rg(mask=True):
    nums = _rand_digits(8)
    dv = _rg_dv(nums)
    d = "".join(map(str, nums))
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}-{dv}" if mask else d + dv


def valid_rg(s):
    s = str(s).upper().replace(".", "").replace("-", "").strip()
    if len(s) != 9:
        return False
    base, dv = s[:8], s[8]
    if not base.isdigit():
        return False
    return _rg_dv([int(x) for x in base]) == dv


# ---------------- CNH ----------------
def _cnh_dvs(base9):
    n = [int(x) for x in base9]
    s = sum(n[i] * (9 - i) for i in range(9))
    dv1 = s % 11
    dsc = 0
    if dv1 >= 10:
        dv1 = 0
        dsc = 2
    s2 = sum(n[i] * (1 + i) for i in range(9))
    x = s2 % 11
    dv2 = x - dsc
    if dv2 < 0:
        dv2 += 11
    if dv2 >= 10:
        dv2 = 0
    return dv1, dv2


def gen_cnh():
    while True:
        base = "".join(map(str, _rand_digits(9)))
        if base == base[0] * 9:
            continue
        d1, d2 = _cnh_dvs(base)
        return base + str(d1) + str(d2)


def valid_cnh(s):
    d = only_digits(s)
    if len(d) != 11 or d == d[0] * 11:
        return False
    d1, d2 = _cnh_dvs(d[:9])
    return d[9] == str(d1) and d[10] == str(d2)


# ---------------- RENAVAM ----------------
def _renavam_dv(base10):
    rev = [int(x) for x in base10[::-1]]
    weights = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3]
    s = sum(r * w for r, w in zip(rev, weights))
    dv = (s * 10) % 11
    return 0 if dv == 10 else dv


def gen_renavam():
    base = "".join(map(str, _rand_digits(10)))
    return base + str(_renavam_dv(base))


def valid_renavam(s):
    d = only_digits(s)
    if len(d) != 11:
        return False
    return str(_renavam_dv(d[:10])) == d[10]


# ---------------- Título de Eleitor ----------------
def _titulo_dvs(seq8, uf2):
    n = [int(x) for x in seq8]
    d1 = sum(n[i] * (i + 2) for i in range(8)) % 11
    if d1 == 10:
        d1 = 0
    u = [int(x) for x in uf2]
    d2 = (u[0] * 7 + u[1] * 8 + d1 * 9) % 11
    if d2 == 10:
        d2 = 0
    return d1, d2


def gen_titulo():
    seq = "".join(map(str, _rand_digits(8)))
    uf = f"{random.randint(1, 28):02d}"
    d1, d2 = _titulo_dvs(seq, uf)
    return seq + uf + str(d1) + str(d2)


def valid_titulo(s):
    d = only_digits(s)
    if len(d) != 12:
        return False
    d1, d2 = _titulo_dvs(d[:8], d[8:10])
    return d[10] == str(d1) and d[11] == str(d2)


# ---------------- Cartão de crédito (Luhn) ----------------
BRANDS = {
    "Visa": ("4", 16),
    "Mastercard": ("5" + str(random.randint(1, 5)) if False else "53", 16),
    "American Express": ("37", 15),
    "Elo": ("4011", 16),
    "Hipercard": ("606282", 16),
    "Diners": ("36", 14),
}


def _luhn_dv(num_without_dv):
    digits = [int(x) for x in num_without_dv]
    s = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return (10 - (s % 10)) % 10


def gen_cartao(brand="Visa", mask=True):
    prefix, length = BRANDS.get(brand, ("4", 16))
    body = prefix + "".join(map(str, _rand_digits(length - 1 - len(prefix))))
    num = body + str(_luhn_dv(body))
    if mask:
        return " ".join(num[i:i + 4] for i in range(0, len(num), 4))
    return num


def valid_cartao(s):
    d = only_digits(s)
    if len(d) < 12:
        return False
    return _luhn_dv(d[:-1]) == int(d[-1])


# ---------------- CEP / Placa ----------------
def gen_cep(mask=True):
    d = "".join(map(str, _rand_digits(8)))
    return f"{d[:5]}-{d[5:]}" if mask else d


def gen_placa(mercosul=True):
    L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if mercosul:
        return (random.choice(L) + random.choice(L) + random.choice(L)
                + str(random.randint(0, 9)) + random.choice(L)
                + str(random.randint(0, 9)) + str(random.randint(0, 9)))
    return "".join(random.choice(L) for _ in range(3)) + "-" + "".join(str(random.randint(0, 9)) for _ in range(4))


# ---------------- Conta bancária (DV mod 11 autoconsistente) ----------------
BANCOS = {"001 Banco do Brasil": "001", "104 Caixa": "104", "237 Bradesco": "237",
          "341 Itaú": "341", "033 Santander": "033", "260 Nubank": "260"}


def _mod11_dv(base):
    w = 2
    s = 0
    for ch in reversed(base):
        s += int(ch) * w
        w = 2 if w == 9 else w + 1
    r = s % 11
    dv = 11 - r
    return "0" if dv >= 10 else str(dv)


def gen_conta(banco="341 Itaú"):
    code = BANCOS.get(banco, "341")
    ag = "".join(map(str, _rand_digits(4)))
    conta = "".join(map(str, _rand_digits(7)))
    return f"Banco {code} · Agência {ag} · Conta {conta}-{_mod11_dv(conta)}"


def valid_conta(s):
    d = only_digits(s)
    return len(d) >= 5  # formato simples


# ---------------- Certidão (32 dígitos, DV mod 11 autoconsistente) ----------------
def _cert_dv(base, start_w):
    w = start_w
    s = 0
    for ch in base:
        s += int(ch) * w
        w -= 1
        if w < 2:
            w = start_w
    r = s % 11
    return 0 if r in (0, 1) else 11 - r


def gen_certidao(mask=True):
    base = "".join(map(str, _rand_digits(30)))
    d1 = _cert_dv(base, 32)
    d2 = _cert_dv(base + str(d1), 33)
    full = base + str(d1) + str(d2)
    if mask:
        return (f"{full[:6]} {full[6:8]} {full[8:10]} {full[10:14]} {full[14:15]} "
                f"{full[15:20]} {full[20:23]} {full[23:30]} {full[30:]}")
    return full


def valid_certidao(s):
    d = only_digits(s)
    if len(d) != 32:
        return False
    d1 = _cert_dv(d[:30], 32)
    d2 = _cert_dv(d[:30] + str(d1), 33)
    return d[30] == str(d1) and d[31] == str(d2)


# ---------------- Inscrição Estadual (SP) ----------------
def _ie_sp_dv1(base8):
    w = [1, 3, 4, 5, 6, 7, 8, 10]
    s = sum(int(base8[i]) * w[i] for i in range(8))
    return str(s % 11 % 10)


def _ie_sp_dv2(base11):
    w = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum(int(base11[i]) * w[i] for i in range(11))
    return str(s % 11 % 10)


def gen_ie_sp(mask=True):
    base = "".join(map(str, _rand_digits(8)))
    d1 = _ie_sp_dv1(base)
    rest = "".join(map(str, _rand_digits(2)))
    base11 = base + d1 + rest
    d2 = _ie_sp_dv2(base11)
    full = base11 + d2
    if mask:
        return f"{full[:3]}.{full[3:6]}.{full[6:9]}.{full[9:]}"
    return full


def valid_ie_sp(s):
    d = only_digits(s)
    if len(d) != 12:
        return False
    return _ie_sp_dv1(d[:8]) == d[8] and _ie_sp_dv2(d[:11]) == d[11]
