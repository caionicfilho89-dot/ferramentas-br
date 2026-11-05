# 🇧🇷 Ferramentas BR (4Devs offline)

**74 ferramentas** num app só — geradores e validadores de documentos brasileiros, funções de texto e calculadoras de matemática. Inspirado no site 4Devs, mas **100% offline**: nada vai pra internet.

Feito em Python + PyQt6.

## As 74 ferramentas

**Geradores (26):** CPF, CNPJ, RG, CNH, PIS/PASEP, RENAVAM, Título de Eleitor, CEP, Inscrição Estadual, Cartão de Crédito, Conta Bancária, Certidões, Placa de Veículos, Pessoas, Empresas, Veículos, Currículo, Nomes, Nicks, Números Aleatórios, Senha, Lorem Ipsum, Imagem, Símbolos, Letras diferentes, Sorteador de números.

**Validadores (11):** CPF, CNPJ, RG, CNH, PIS/PASEP, RENAVAM, Título de Eleitor, Inscrição Estadual, Cartão de Crédito, Conta Bancária, Certidões.

**Texto (14):** corretor ortográfico, ordem alfabética, contador de caracteres, contador de ocorrências, texto→HTML, cortar texto, dividir string, info de caractere, inverter texto, letras personalizadas, maiúsc/minúsc, número por extenso, remover acentos, remover/trocar quebras de linha.

**Matemática — Calculadoras (7):** números romanos, fatorar, MDC, MMC, porcentagem, regra de 3, resto da divisão.

**Matemática — Áreas (13):** círculo, quadrado, retângulo, triângulo, pentágono, hexágono, polígono regular, losango, trapézio, paralelogramo, elipse, coroa circular, setor circular.

**Datas (3):** dias entre datas, somar dias, subtrair dias.

## Como usar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Rode:
   ```
   pythonw ferramentas_br.pyw
   ```
3. Escolha a ferramenta na lista à esquerda, preencha os campos e clique no botão. O resultado aparece e dá pra **copiar**.

## Importante

Os documentos (CPF, CNPJ, etc.) são **gerados por algoritmo** (dígitos verificadores corretos) para **testar sistemas** — **não pertencem a pessoas ou empresas reais**. CPF, CNPJ, PIS, CNH, RENAVAM, Título e cartão (Luhn) seguem os algoritmos oficiais; conta bancária, certidão e inscrição estadual usam um dígito verificador autoconsistente (formato válido).

## Requisitos

- Windows / Linux / macOS
- Python 3.10+
- `PyQt6`, `Pillow` (gerador de imagem), `pyspellchecker` (corretor ortográfico — opcional, tem modo alternativo)

## Licença

MIT — veja [LICENSE](LICENSE).
