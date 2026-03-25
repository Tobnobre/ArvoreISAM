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
    # Páginas Folha Primárias (Capacidade 2) - inicializadas com tuplas (chave, dado)
    folhaA = Page([(10, "R10"), (15, "R15")])
    folhaB = Page([(20, "R20"), (27, "R27")])
    folhaC = Page([(33, "R33"), (37, "R37")])
    folhaD = Page([(40, "R40"), (46, "R46")])
    folhaE = Page([(51, "R51"), (55, "R55")])
    folhaF = Page([(63, "R63"), (97, "R97")])

    # O nível intermediário aponta para os filhos e usa apenas inteiros como guias
    noEsq = IndexNode([20, 33], [folhaA, folhaB, folhaC]) 
    noDir = IndexNode([51, 63], [folhaD, folhaE, folhaF])

    # A raiz aponta para os nós intermediários
    raiz = IndexNode([40], [noEsq, noDir])
    
    return raiz

def inserir(raiz, chave, dado=None, verbose=False):
  
    no_atual = raiz
    custo = 0
    caminho = []
    
    # 1. Navegar pelo índice para encontrar a folha primária correta
    # Continuamos descendo enquanto o nó atual for um IndexNode
    while isinstance(no_atual, IndexNode):
        custo += 1
        caminho.append(f"IndexNode({no_atual.keys})")
        
        idx_filho = 0
        # Encontra o ramo correto: avança enquanto a chave for maior ou igual ao separador
        while idx_filho < len(no_atual.keys) and chave >= no_atual.keys[idx_filho]:
            idx_filho += 1
            
        no_atual = no_atual.children[idx_filho]
        
    # Quando o loop termina, no_atual é a página folha primária (instância de Page)
    pagina_atual = no_atual
    
    # 2. Percorrer a cadeia de overflow, se necessário, até achar uma página com espaço
    while len(pagina_atual.records) >= pagina_atual.capacity:
        custo += 1
        caminho.append(f"Page({pagina_atual.records})")
        
        if pagina_atual.next_overflow is None:
            # Se não houver próxima página de overflow, criamos uma nova
            pagina_atual.next_overflow = Page(capacity=pagina_atual.capacity)
            
        # Avançamos para a página de overflow
        pagina_atual = pagina_atual.next_overflow
        
    # 3. Inserir o registro
    custo += 1 # Conta a página final onde o registro é efetivamente inserido
    caminho.append(f"Page(Nova Inserção/Espaço)")
    
    # O trabalho pede a inserção de registros no formato (18, R18), por isso usamos tuplas.
    registro = (chave, dado) if dado else chave
    pagina_atual.records.append(registro)
    
    # (Opcional) Ordenar os registros dentro da página para facilitar a busca e a leitura
    # Verifica se é uma tupla para ordenar pela chave (índice 0)
    pagina_atual.records.sort(key=lambda x: x[0] if isinstance(x, tuple) else x)
    
    if verbose:
        print(f"--- Inserindo chave {chave} ---")
        print(f"Caminho percorrido: {' -> '.join(caminho)}")
        print(f"Custo total: {custo} nós acessados\n")


def buscar(raiz, chave, verbose=False):
 
    no_atual = raiz
    custo = 0
    caminho = []
    
    # 1. Navegar pelo índice para encontrar a folha primária correta
    while isinstance(no_atual, IndexNode):
        custo += 1
        caminho.append(f"IndexNode({no_atual.keys})")
        
        idx_filho = 0
        # Encontra o ramo correto: avança enquanto a chave for maior ou igual ao separador
        while idx_filho < len(no_atual.keys) and chave >= no_atual.keys[idx_filho]:
            idx_filho += 1
            
        no_atual = no_atual.children[idx_filho]
        
    # Quando o loop termina, no_atual é a página folha primária (instância de Page)
    pagina_atual = no_atual
    
    # 2. Percorrer a cadeia de overflow, se necessário, até achar a chave ou esgotar as páginas
    while pagina_atual is not None:
        custo += 1
        caminho.append(f"Page({pagina_atual.records})")
        
        # Procura a chave na página atual
        for registro in pagina_atual.records:
            encontrado = False
            # Verifica se é uma tupla (chave, dado) ou apenas a chave
            if isinstance(registro, tuple):
                if registro[0] == chave:
                    encontrado = True
            else:
                if registro == chave:
                    encontrado = True
            
            if encontrado:
                if verbose:
                    print(f"--- Busca por Igualdade: Chave {chave} ---")
                    print(f"Caminho percorrido: {' -> '.join(caminho)}")
                    print(f"Custo total: {custo} nós acessados\n")
                return registro  # Chave encontrada!
        
        # Se não encontrou na página atual, avança para a próxima página de overflow
        pagina_atual = pagina_atual.next_overflow
        
    if verbose:
        print(f"--- Busca por Igualdade: Chave {chave} ---")
        print(f"Caminho percorrido: {' -> '.join(caminho)}")
        print(f"Resultado: Registro não encontrado na árvore")
        print(f"Custo total: {custo} nós acessados\n")
        
    # 3. Se chegou aqui, a chave não foi encontrada em nenhuma página
    return None

def remover(raiz, chave, verbose=False):
 
    no_atual = raiz
    custo = 0
    caminho = []
    
    # 1. Navegar pelo índice para encontrar a folha primária correta
    while isinstance(no_atual, IndexNode):
        custo += 1
        caminho.append(f"IndexNode({no_atual.keys})")
        
        idx_filho = 0
        # Encontra o ramo correto: avança enquanto a chave for maior ou igual ao separador
        while idx_filho < len(no_atual.keys) and chave >= no_atual.keys[idx_filho]:
            idx_filho += 1
            
        no_atual = no_atual.children[idx_filho]
        
    # Quando o loop termina, no_atual é a página folha primária
    pagina_atual = no_atual
    
    # 2. Percorrer a cadeia de overflow procurando a chave para remover
    while pagina_atual is not None:
        custo += 1
        caminho.append(f"Page({pagina_atual.records})")
        
        registro_alvo = None
        
        # Procura a chave na página atual
        for registro in pagina_atual.records:
            # Verifica se é uma tupla (chave, dado) ou apenas a chave
            if isinstance(registro, tuple):
                if registro[0] == chave:
                    registro_alvo = registro
                    break
            else:
                if registro == chave:
                    registro_alvo = registro
                    break
        
        # Se encontrou, remove o registro da lista da página
        if registro_alvo is not None:
            pagina_atual.records.remove(registro_alvo)
            
            if verbose:
                print(f"--- Remoção: Chave {chave} ---")
                print(f"Caminho percorrido: {' -> '.join(caminho)}")
                print(f"Resultado: Registro removido com sucesso!")
                print(f"Custo total: {custo} nós acessados\n")
            return True
            
        # Se não encontrou na página atual, avança para a próxima página de overflow
        pagina_atual = pagina_atual.next_overflow
        
    # 3. Se chegou aqui, a chave não foi encontrada para remoção
    if verbose:
        print(f"--- Remoção: Chave {chave} ---")
        print(f"Caminho percorrido: {' -> '.join(caminho)}")
        print(f"Resultado: Registro não encontrado para remoção")
        print(f"Custo total: {custo} nós acessados\n")
        
    return False

def imprimir_estrutura(no, nivel=0):
 
    if no is None:
        return
    
    # Indentação baseada no nível
    indent = "    " * nivel
    
    if isinstance(no, IndexNode):
        # Imprime o nó interno
        print(f"{indent}Nó Interno: {no.keys}")
        
        # Imprime os filhos recursivamente
        for i, child in enumerate(no.children):
            print(f"{indent}  Filho {i}:")
            imprimir_estrutura(child, nivel + 2)
            
    elif isinstance(no, Page):
        # Imprime a página folha
        print(f"{indent}Página Folha: {no.records}")
        
        # Se tiver overflow, imprime também
        if no.next_overflow:
            print(f"{indent}  -> Overflow:")
            imprimir_estrutura(no.next_overflow, nivel + 2)

# --- Exemplo de uso ---
raiz = initialize_index()
inserir(raiz, 18, "R18", verbose=True) # Exemplo com verbose na inserção
inserir(raiz, 22, "R22")
inserir(raiz, 27, "R27")
inserir(raiz, 35, "R35")
inserir(raiz, 41, "R41")
inserir(raiz, 44, "R44")
inserir(raiz, 63, "R63")
inserir(raiz, 67, "R67")
inserir(raiz, 83, "R83")
inserir(raiz, 86, "R86")
inserir(raiz, 121, "R121")
inserir(raiz, 145, "R145", verbose=True)

print("Estrutura da Árvore ISAM:\n")
imprimir_estrutura(raiz)

print("\n" + "="*50)
print("Buscando chaves por Igualdade (Com Métricas):")
print("="*50 + "\n")

res22 = buscar(raiz, 22, verbose=True)
print(f">> Retorno Final: {res22}\n")

res35 = buscar(raiz, 35, verbose=True)
print(f">> Retorno Final: {res35}\n")

res44 = buscar(raiz, 44, verbose=True)
print(f">> Retorno Final: {res44}\n")

res90 = buscar(raiz, 90, verbose=True)
print(f">> Retorno Final: {res90}\n")
