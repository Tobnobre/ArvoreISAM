# Classes para representar as páginas e os nós do índice
class Page:
    def __init__(self, initial_records = None, capacity=2):
        self.records = initial_records if initial_records else []  # Lista de registros (chave, dado)
        self.capacity = capacity
        self.next_overflow = None # Ponteiro para a próxima página de overflow

class IndexNode:
    def __init__(self, keys, children):
        self.keys = keys           # Ex: [20, 33]
        self.children = children   # Referências para outros IndexNodes ou Pages

def initialize_index():
    # Páginas Folha Primárias (Capacidade 2) - onde os dados são armazenados
    folhaA = Page([10, 15])
    folhaB = Page([20, 27])
    folhaC = Page([33, 37])
    folhaD = Page([40, 46])
    folhaE = Page([51, 55])
    folhaF = Page([63, 97])

    # O nível intermediário
    # O nó esquerdo aponta para as páginas que contêm chaves menores que 40
    # Enquanto o nó direito aponta para as páginas que contêm chaves maiores ou iguais a 40
    noEsq = IndexNode([20, 33], [folhaA, folhaB, folhaC]) 
    noDir = IndexNode([51, 63], [folhaD, folhaE, folhaF])

    # A raiz 
    # Aponta para os nós intermediários
    raiz = IndexNode([40], [noEsq, noDir])
    
    return raiz
