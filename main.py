import itertools

# --- CONFIGURAÇÃO INICIAL ---
abertura = {'a': 3, 'e': 2, 'o': 2, 'i': 1, 'u': 1, 'y': 1}
fechadas_ou_traseiras = ['i', 'y', 'u', 'o']

class Fonema:
    def __init__(self, char, tipo, **propriedades):
        self.char = char
        self.tipo = tipo  # 'C', 'V', 'S', 'C_MISTA'
        self.ponto = propriedades.get('ponto')
        self.modo = propriedades.get('modo')
        self.sibilante = propriedades.get('sibilante', False)
        self.rotica = propriedades.get('rotica', False)
        self.nasal = propriedades.get('nasal', False)
        self.liquida = propriedades.get('liquida', False)
        self.obstruente = propriedades.get('obstruente', False)

    def __repr__(self):
        return self.char

# --- INVENTÁRIO DE SONS ---
sons = {
    'm': Fonema('m', 'C', ponto='bilabial', nasal=True),
    'n': Fonema('n', 'C', ponto='alveolar', nasal=True),
    'ñ': Fonema('ñ', 'C', ponto='velar',    nasal=True),
    'p': Fonema('p', 'C', ponto='bilabial', obstruente=True),
    't': Fonema('t', 'C', ponto='alveolar', obstruente=True),
    'k': Fonema('k', 'C', ponto='velar',    obstruente=True),
    'q': Fonema('q', 'C', ponto='uvular',   obstruente=True),
    'v': Fonema('v', 'C', ponto='bilabial', obstruente=True),
    'ð': Fonema('ð', 'C', ponto='dental',   obstruente=True),
    's': Fonema('s', 'C', ponto='alveolar', sibilante=True, obstruente=True),
    'j': Fonema('j', 'C', ponto='velar',    obstruente=True),
    'r': Fonema('r', 'C', ponto='alveolar', rotica=True, liquida=True),
    'rh':Fonema('rh','C', ponto='uvular',   rotica=True, liquida=True),
    'b': Fonema('b', 'C', ponto='bilabial', obstruente=True),
    'd': Fonema('d', 'C', ponto='alveolar', obstruente=True),
    'g': Fonema('g', 'C', ponto='velar',    obstruente=True),
    'î': Fonema('î', 'S', ponto='palatal',  liquida=False), # Semivogal
    'w': Fonema('w', 'S', ponto='bilabial', liquida=False), # Semivogal
    'û': Fonema('û', 'S', ponto='velar',    liquida=False)  # Semivogal
}

# --- GERAÇÃO DE MISTURAS ---
def criar_mistura(letras):
    primeiro = sons[letras[0]]
    return Fonema("".join(letras), 'C_MISTA', ponto=primeiro.ponto, 
                  sibilante=primeiro.sibilante, rotica=primeiro.rotica, 
                  nasal=primeiro.nasal, liquida=primeiro.liquida)

bi_lista = [['s','p'], ['s','b'], ['g','b'], ['j','v'], ['ñ','m'], ['p','t'], ['b','d'], ['m','n'], ['s','t'], ['s','d'], ['r','t'], ['r','d'], ['k','t'], ['g','d'], ['ñ','n'], ['rh','t'], ['rh','d'], ['s','k'], ['s','g'], ['r','k'], ['r','g'], ['s','q'], ['r','q'], ['rh','q']]
tri_lista = [['s','p','t'], ['s','b','d'], ['g','b','d'], ['ñ','m','n'], ['s','k','t'], ['s','g','d'], ['r','k','t'], ['r','g','d']]

for l in bi_lista + tri_lista:
    m = criar_mistura(l)
    sons[m.char] = m

# --- GERAÇÃO DE VOGAIS ---
vogais_simples = ['a', 'e', 'o', 'i', 'u', 'y']
vogais_finais = []
for v1 in vogais_simples:
    vogais_finais.append(v1)
    if v1 in fechadas_ou_traseiras: vogais_finais.append(v1 + "̃")
    for v2 in vogais_simples:
        if abertura[v1] > abertura[v2] and v1 != 'y' and v2 != 'y':
            vogais_finais.append(v1 + v2)
            if v2 in fechadas_ou_traseiras: vogais_finais.append(v1 + v2 + "̃")

# --- VALIDAÇÃO ---
def validar_silaba(c_on=None, l_on=None, v=None, c_co=None):
    if c_on and l_on:
        if c_on.nasal and l_on.tipo != 'S': return False # Regra 10 
    
    if c_on and c_on.tipo == 'C_MISTA':
        if not (c_on.ponto in ['velar', 'bilabial'] or c_on.sibilante or c_on.char == 'ñmn'):
            return False # Regra 7, 9 [cite: 7, 9]

    if c_co and c_co.tipo == 'C_MISTA':
        if c_co.sibilante or c_co.char == 'ñmn' or not (c_co.ponto in ['velar', 'bilabial'] or c_co.liquida):
            return False # Regra 8, 9 [cite: 8, 9]
            
    return True

# --- GERADOR EXAUSTIVO ---
def gerar_tudo():
    consoantes = [None] + list(sons.values())
    liquidas = [None] + [s for s in sons.values() if s.liquida or s.tipo == 'S']
    
    valido = []
    for co, lo, vo, cc in itertools.product(consoantes, liquidas, vogais_finais, consoantes):
        if validar_silaba(co, lo, vo, cc):
            res = f"{co if co else ''}{lo if lo else ''}{vo}{cc if cc else ''}"
            valido.append(res)
    return valido

# Execução
resultado = gerar_tudo()
print(f"Sucesso! Geradas {len(resultado)} sílabas válidas.")
print("Exemplos:", resultado[100:110])