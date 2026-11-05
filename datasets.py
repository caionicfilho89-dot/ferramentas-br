"""Dados brasileiros realistas para geração de dados fictícios (offline)."""
from __future__ import annotations

NOMES_M = [
    "Miguel", "Arthur", "Heitor", "Bernardo", "Theo", "Davi", "Gabriel",
    "Pedro", "Samuel", "Lorenzo", "Benjamin", "Matheus", "Lucas", "Benício",
    "Rafael", "Enzo", "João", "Nicolas", "Guilherme", "Gustavo", "Felipe",
    "Henrique", "Murilo", "Pedro Henrique", "Vinícius", "Bryan", "Daniel",
    "Bento", "Caio", "Eduardo", "Leonardo", "Antônio", "Carlos", "Marcelo",
    "Ricardo", "Fernando", "Roberto", "Paulo", "André", "Bruno", "Diego",
    "Rodrigo", "Thiago", "Marcos", "Fábio", "Leandro", "Alexandre",
    "Victor", "Igor", "Otávio",
]

NOMES_F = [
    "Helena", "Alice", "Laura", "Maria", "Sophia", "Manuela", "Maria Eduarda",
    "Valentina", "Giovanna", "Maria Clara", "Beatriz", "Heloísa", "Júlia",
    "Luiza", "Isabella", "Mariana", "Lara", "Lívia", "Marina", "Clara",
    "Rafaela", "Yasmin", "Gabriela", "Ana Luiza", "Isabel", "Larissa",
    "Emanuelly", "Fernanda", "Camila", "Amanda", "Carolina", "Juliana",
    "Patrícia", "Aline", "Bruna", "Vanessa", "Letícia", "Natália",
    "Vitória", "Rebeca", "Bianca", "Sabrina", "Daniela", "Renata",
    "Priscila", "Tatiane", "Jéssica", "Carla", "Simone", "Mônica",
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
    "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
    "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha",
    "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques", "Machado",
    "Mendes", "Freitas", "Cardoso", "Ramos", "Gonçalves", "Santana", "Teixeira",
    "Araújo", "Correia", "Cavalcante", "Pinto", "Monteiro", "Moura", "Cunha",
    "Castro", "Campos", "Cardozo", "Melo", "Duarte", "Reis", "Azevedo",
    "Fonseca", "Batista", "Farias", "Nogueira", "Tavares", "Pires", "França",
    "Macedo", "Aragão", "Barros", "Caldeira",
]

# (cidade, UF, DDD, prefixo de CEP de 2 dígitos)
CIDADES_UF = [
    ("São Paulo", "SP", "11", "01"), ("Rio de Janeiro", "RJ", "21", "20"),
    ("Belo Horizonte", "MG", "31", "30"), ("Brasília", "DF", "61", "70"),
    ("Salvador", "BA", "71", "40"), ("Fortaleza", "CE", "85", "60"),
    ("Curitiba", "PR", "41", "80"), ("Recife", "PE", "81", "50"),
    ("Porto Alegre", "RS", "51", "90"), ("Manaus", "AM", "92", "69"),
    ("Belém", "PA", "91", "66"), ("Goiânia", "GO", "62", "74"),
    ("Campinas", "SP", "19", "13"), ("Guarulhos", "SP", "11", "07"),
    ("São Luís", "MA", "98", "65"), ("Maceió", "AL", "82", "57"),
    ("Natal", "RN", "84", "59"), ("Teresina", "PI", "86", "64"),
    ("Campo Grande", "MS", "67", "79"), ("João Pessoa", "PB", "83", "58"),
    ("Florianópolis", "SC", "48", "88"), ("Vitória", "ES", "27", "29"),
    ("Cuiabá", "MT", "65", "78"), ("Aracaju", "SE", "79", "49"),
    ("Santos", "SP", "13", "11"), ("Ribeirão Preto", "SP", "16", "14"),
    ("Uberlândia", "MG", "34", "38"), ("Londrina", "PR", "43", "86"),
    ("Niterói", "RJ", "21", "24"), ("Caxias do Sul", "RS", "54", "95"),
]

UFS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
       "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

DDDS = sorted({c[2] for c in CIDADES_UF})

BAIRROS = [
    "Centro", "Jardim América", "Vila Nova", "Bela Vista", "Santa Cecília",
    "Boa Vista", "Vila Mariana", "Moema", "Pinheiros", "Tatuapé",
    "Copacabana", "Ipanema", "Tijuca", "Barra da Tijuca", "Savassi",
    "Funcionários", "Pampulha", "Boa Viagem", "Meireles", "Aldeota",
    "Batel", "Água Verde", "Moinhos de Vento", "Cidade Baixa",
    "Jardim Botânico", "Setor Bueno", "Vila Olímpia", "Itaim Bibi",
    "Liberdade", "Perdizes",
]

LOGRADOUROS = ["Rua", "Rua", "Rua", "Avenida", "Avenida", "Travessa", "Alameda",
               "Praça", "Estrada", "Largo", "Ladeira"]

NOMES_RUA = [
    "das Flores", "dos Andradas", "Sete de Setembro", "XV de Novembro",
    "Tiradentes", "Dom Pedro II", "Santos Dumont", "Brasil", "Paulista",
    "das Palmeiras", "Getúlio Vargas", "Rui Barbosa", "Marechal Deodoro",
    "José Bonifácio", "Barão do Rio Branco", "dos Bandeirantes", "Castro Alves",
    "Monteiro Lobato", "Carlos Gomes", "Duque de Caxias", "da Liberdade",
    "Floriano Peixoto", "Machado de Assis", "São João", "Independência",
]

MARCAS_MODELOS = {
    "Volkswagen": ["Gol", "Polo", "Virtus", "T-Cross", "Nivus"],
    "Chevrolet": ["Onix", "Onix Plus", "Tracker", "Spin", "Montana"],
    "Fiat": ["Argo", "Mobi", "Cronos", "Strada", "Toro"],
    "Ford": ["Ka", "Fiesta", "EcoSport", "Ranger", "Territory"],
    "Toyota": ["Corolla", "Corolla Cross", "Hilux", "Yaris", "Etios"],
    "Honda": ["Civic", "Fit", "City", "HR-V", "WR-V"],
    "Hyundai": ["HB20", "HB20S", "Creta", "Tucson", "i30"],
    "Renault": ["Kwid", "Sandero", "Logan", "Duster", "Captur"],
}

CORES = ["Branco", "Preto", "Prata", "Cinza", "Vermelho", "Azul",
         "Verde", "Bege", "Marrom", "Amarelo", "Dourado", "Vinho"]

COMBUSTIVEIS = ["Gasolina", "Etanol", "Flex", "Diesel", "GNV"]

SIGNOS = [  # (nome, (mes, dia) de início)
    ("Capricórnio", (1, 1)), ("Aquário", (1, 20)), ("Peixes", (2, 19)),
    ("Áries", (3, 21)), ("Touro", (4, 20)), ("Gêmeos", (5, 21)),
    ("Câncer", (6, 21)), ("Leão", (7, 23)), ("Virgem", (8, 23)),
    ("Libra", (9, 23)), ("Escorpião", (10, 23)), ("Sagitário", (11, 22)),
    ("Capricórnio", (12, 22)),
]

CORES_FAVORITAS = ["azul", "verde", "vermelho", "amarelo", "roxo", "preto",
                   "branco", "laranja", "rosa", "cinza"]
TIPOS_SANGUE = ["O+", "O+", "A+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"]

DOMINIOS_EMAIL = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br", "uol.com.br",
                  "bol.com.br", "terra.com.br"]

# empresas
EMPRESA_PALAVRAS = ["Alfa", "Nova", "Prime", "Brasil", "Sol", "Horizonte", "Vale", "Global",
                    "Master", "Real", "Ideal", "Líder", "Total", "Forte", "Aurora", "Delta",
                    "Atlântico", "Serra", "Rio", "Mega"]
EMPRESA_RAMOS = ["Comércio", "Tecnologia", "Transportes", "Alimentos", "Construções",
                 "Consultoria", "Engenharia", "Distribuidora", "Serviços", "Informática",
                 "Logística", "Móveis", "Confecções", "Materiais Elétricos", "Agropecuária"]
EMPRESA_TIPOS = ["Ltda", "Ltda", "ME", "EIRELI", "S.A.", "EPP"]

# currículo
CARGOS = ["Analista de Sistemas", "Desenvolvedor Python", "Assistente Administrativo",
          "Analista Financeiro", "Vendedor", "Gerente de Projetos", "Designer Gráfico",
          "Técnico de Suporte", "Auxiliar de Logística", "Analista de Marketing",
          "Recepcionista", "Engenheiro Civil", "Professor", "Enfermeiro", "Contador"]
CURSOS = ["Ciência da Computação", "Administração", "Engenharia Civil", "Direito",
          "Análise e Desenvolvimento de Sistemas", "Ciências Contábeis", "Marketing",
          "Pedagogia", "Enfermagem", "Design Gráfico", "Sistemas de Informação"]
FACULDADES = ["USP", "UNICAMP", "UFMG", "UFRJ", "PUC", "Mackenzie", "UNIP", "Anhembi Morumbi",
              "FIAP", "UFPR", "UFRGS", "Estácio", "UNESP"]
HABILIDADES = ["Pacote Office", "Comunicação", "Trabalho em equipe", "Python", "SQL",
               "Excel avançado", "Atendimento ao cliente", "Gestão de tempo", "Liderança",
               "Photoshop", "Negociação", "Power BI", "Git", "Resolução de problemas"]
IDIOMAS = ["Inglês", "Espanhol", "Francês", "Italiano", "Alemão"]
NIVEIS_IDIOMA = ["básico", "intermediário", "avançado", "fluente"]

# nicks
NICK_ADJ = ["Dark", "Shadow", "Silent", "Mad", "Crazy", "Epic", "Fast", "Toxic", "Iron",
            "Ghost", "Pro", "Lucky", "Wild", "Frozen", "Golden", "Red", "Black", "Neon",
            "Savage", "Cyber", "Brabo", "Sinistro", "Monstro", "Ligeiro"]
NICK_SUB = ["Wolf", "Sniper", "Dragon", "Hunter", "Ninja", "Killer", "Master", "Knight",
            "Tiger", "Gamer", "Viper", "Phoenix", "Reaper", "Samurai", "Falcon", "Panda",
            "Lobo", "Tubarão", "Jacaré", "Mago", "Guerreiro"]
