# Versão do PYTHON: 3.10

# /*******************************************************************************
# Autor: Naila
# Componente Curricular: Algoritmos I
# Concluido em:
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************/
import os  # Importação do módulo os


# Função para abrir o file *txt de armazenamento e retornar um dicionário.
def openCache():
    lista = []
    dic = {}
    # Tentar abrir o file de armazenamento, caso ele já tenha sido criado.
    try:
        with open("cache.dat", "r", encoding='utf-8') as cache:
            b = cache.read()
            # Percorrer a array criada a partir do file e retirar a quebra de linha.
            for line in b.split("\n"):
                cache1 = line.split("***")
                # Enumerar a array.
                for i, v in enumerate(cache1):
                    if v != "":  # Ignorar os espaços em branco.
                        # Se o índice for par, significa que ele é um termo
                        if i % 2 == 0:
                            lista.append(v)
                        # Se o índice for impar, signica que ele é uma array com o caminho do arquivo e a quantidade de termos.
                        else:
                            lista.append(eval(v))
            # Tranformar a lista em um dicionário.
            for i, v in enumerate(lista):
                if i % 2 == 0:
                    aux = v
                elif i % 2 != 0:
                    dic[aux] = v
    # Caso o file ainda não tenha sido criado o programa prossegue com o ciclo.
    except:
        pass
    # Retorna o dicionário igual ao do Indice Invertido.
    return dic


# Função que cria o índice invertido
def InvertedIndex(array, dictionaryTerms):
    # array para armazenar as referências
    listReferences = list()
    # Lista com as preposições que devem ser ignoradas para adição no índice invertido.
    prepositions = ["é", "a", "e", "i", "o", "u", "de", "em", "por", "ao", "do", "no", "pelo", "da", "pela", "das",
                    "pelo", "os", "aos", "dos", "nos", "as", "das", "nas", "um", "numa", "uma", "com", "até", "de",
                    "por"]
    # Enumerar o indice e o objeto
    for indice, objeto in enumerate(array):
        # Se existerem o objetos
        if objeto:
            # lista auxiliar para armazenar e colocar no dicionário.
            aux = objeto[0].lower().strip().split(":")
            for elemento in aux:
                # Retorna o elemento de forma minúscula
                elemento.lower()
                # Retirar elementos indesejáveis.
                if elemento not in prepositions and elemento != "":
                    if elemento in dictionaryTerms.keys():
                        # Procurar se elemento existe ou não.
                        if objeto[1] not in dictionaryTerms.get(elemento):
                            # Adiciona elemento no dicionário de termos.
                            dictionaryTerms.get(elemento).append(objeto[1])
                            dictionaryTerms.get(elemento).append(objeto[2])
                    else:
                        dictionaryTerms[elemento] = listReferences
                        if objeto[1] not in dictionaryTerms.get(elemento):
                            dictionaryTerms.get(elemento).append(objeto[1])
                            dictionaryTerms.get(elemento).append(objeto[2])
                    listReferences = []
            # Deixa a lista auxiliar vazia novamente.
            aux = []
    return dictionaryTerms


# Leitura do diretório.
def readfile(diretorio):
    # Lista para armazenar os termos, o caminho e a quantidade que o termo de repete no arquivo.
    lista = []
    # Caracteres que devem ser substituídos por espaço.
    caracteres = [",", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ".", ":", ";", "<", "=", ">", "?", "@", "[",
                  "]", "^", "_", "`", "{", "|", "}", "~"]
    # Verifica se é um diretório.
    if os.path.isdir(diretorio):
        # Pecorre o diretório, as subpastas e os arquivos presentes no diretório.
        for root, directories, files in os.walk(diretorio):
            # Percorre os arquivos.
            for file in files:
                # Separa a extensão do arquivo para a verificação.
                a, extensao = os.path.splitext(file)
                # Verifica se a extensão do arquivo é ".txt"
                if extensao == ".txt":
                    # Armazena o caminho completo do arquivo.
                    fullPath = os.path.join(root, file)
                    # Tentar abrir o file.
                    try:
                        with open(fullPath, "r", encoding='utf-8') as arq:
                            # Dicionário para armazenar os termos temporariamente.
                            newDic = {}
                            aux = []
                            # Percorre o arquivo recebido para substituir os caracteres especiais por espaço.
                            for i in arq:
                                i = i.strip()
                                i = i.lower()
                                for c in caracteres:
                                    i = i.replace(c, " ")
                                # Separa as palavras por espaço.
                                words = i.split(" ")
                                for j in words:
                                    if j in newDic:
                                        newDic[j] = newDic[j] + 1
                                    else:
                                        newDic[j] = 1
                            # Adicionar as palavras do dicionário em uma array.
                            aux = []
                            for k, v in newDic.items():
                                if k != "":
                                    aux.append(k)
                                    aux.append(fullPath)
                                    aux.append(v)
                                    lista.append(aux)
                                    aux = []
                            newDic = {}
                    # Se ocorrer um erro na leitura de algum file ele deve ser ignorado e programa deve seguir o ciclo lendo os outros arquivos.
                    except:
                        print(f"\nO file {fullPath}\n"
                              f"pertencente ao diretório {diretorio} não foi indexado!\n")
    # Mostrar para o usuário que epenas diretórios podem ser indexados.
    else:
        print("\nApenas dirétórios podem ser indexados!\n")
    # Retornar array.
    return lista


# Adiconar o índice invertido no cache.
def addCache(indice):
    with open("cache.dat", "w", encoding='utf-8') as cache:
        for k, v in indice.items():
            cache.write(f"{k}***{v}")
            cache.write(f"\n")


# Função utilizada para realizar a busca de termos no índice invertido.
def search(term, dictionary):
    # Lista para ordenar.
    listSort = []
    indice = []
    # Realiza a busca do termo procurado no dicionário.
    if term in dictionary:
        indice = dictionary.get(term)
        for i in range(len(indice)):
            aux = []
            if i % 2 == 0:
                aux.append(indice[i])
                aux.append(indice[i + 1])
                listSort.append(aux)
            aux = []

    # Chama a função de ordenação.
    bubbleSort(listSort)

    # Mostrar para o usuário.
    print("──" * 40)
    print(f"Quantidade de Arquivos com o termo {term}: {(len(listSort))}".center(75, " "))
    for i in range(len(listSort)):
        print("──" * 40)
        print(f"Arquivo: {listSort[i][0]}  │ Frequência: {listSort[i][1]}")
    print("──" * 40)


# Algoritmo utilizado para ordenação
def bubbleSort(lista):
    # Ordenação de forma decrescente.
    for j in range(len(lista) - 1):
        for i in range(len(lista) - 1):
            if lista[i][1] < lista[i + 1][1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]


# Função para remover diretório.
def removeDirectory(dictionaryTerms, directory, display):
    count = 0
    # Percorre o diretório.
    for root, directories, files in os.walk(directory):
        for file in files:
            # Armazenar extensão e termo do arquivo.
            a, extension = os.path.splitext(file)
            # Verifica se a extensão é txt.
            if extension == ".txt":
                # Armazena caminho completo.
                fullPath = os.path.join(root, file)
                # Armazena apenas a parte do caminho no diretório.
                caminhoDiretorio = os.path.dirname(fullPath)
                # # Percorre as chaves e os valores em um dicionário copiado.
                for k, v in dictionaryTerms.copy().items():
                    # Percorrer a array com caminho completo e quantidade.
                    for c in range(len(v)):
                        # Verifica se existem elementos na array.
                        if len(v) > 0:
                            # Verifica se a quantidade de itens condiz com a quantidade de itens na array.
                            if c < len(v):
                                # Se o índice for par, ou seja, se o valor na array for um caminho.
                                if c % 2 == 0:
                                    # Armazena apenas a parte do diretório do caminho.
                                    caminhoIndice = os.path.dirname(v.copy()[c])
                                    # Remove as ocorrências do caminho no dicionário.
                                    if caminhoIndice == caminhoDiretorio:
                                        del (v[c + 1])
                                        del (v[c])
                                        count += 1
                                        # Se a array ficar vazia, a chave é apagada do dicionário.
                                        if len(v) == 0:
                                            dictionaryTerms.pop(k)
    # O dicionário é reescrito.
    addCache(dictionaryTerms)
    if count == 0:
        print("\nO diretório não pertence ao sistema!\n")
    elif count > 0 and display == 1:
        print("\nDiretório removido!\n")
    return dictionaryTerms


# Função para remover arquivos.
def removeFile(dictionaryTerms, file):
    count = 0
    # Retorna o caminho absoluto do aruivo.
    fullPath = os.path.abspath(file)
    a, extension = os.path.splitext(fullPath)
    if extension == ".txt":
        for k, v in dictionaryTerms.copy().items():
            for c in range(len(v)):
                if len(v) > 0:
                    if c < len(v):
                        if c % 2 == 0:
                            if v.copy()[c] == fullPath:
                                del (v[c + 1])
                                del (v[c])
                                count += 1
                                if len(v) == 0:
                                    dictionaryTerms.pop(k)
    addCache(dictionaryTerms)
    if count > 0:
        print("\nArquivo removido!\n")

    elif count == 0:
        print("\nO file não pertence ao sistema!\n")
    return dictionaryTerms


# Função para verificar se é necessário remover um arquivo ou um diretório.
def toRemove(dictionaryTerms, directory, display):
    if os.path.isdir(directory):
        removeDirectory(dictionaryTerms, directory, display)

    elif os.path.isfile(directory):
        removeFile(dictionaryTerms, directory)

    else:
        print("\nENTRADA INVÁLIDA\n")


# Visualizar os índice invertido.
def view(dictionaryTerms):
    print("Visualização do Índice Invertido".center(75, " "))
    for k, v in dictionaryTerms.items():
        print("──" * 40)
        print(f"Termo: {k}".center(75, " "))
        for i in range(len(v)):
            if i % 2 == 0:
                print(f"--> {v[i]}")
    print()


# Criar um arquivo para adiconar os caminhos adiconados.
def check():
    with open("diretorios.cache", "a", encoding='utf-8') as ver:
        pass


# Tabela com argumentos que podem ser utilizados.
def help_cli():
    print("┌─────────┬────────────────────────────────────────┐\n"
          "│   -i    │   Indexar arquivos em um diretório.    │\n"
          "│   -b    │   Buscar termo em um diretório.        │\n"
          "│   -v    │   Visualizar índice.                   │\n"
          "│   -r    │   Remover diretório/file do índice.    │\n"
          "│   -h    │   Ajuda para compreender o sistema.    │\n"
          "└─────────┴────────────────────────────────────────┘\n")
    print()


# Função para atualizar o índice.
def update(dictionaryTerms, diretorio):
    # Primeiro o diretório é removido.
    toRemove(dictionaryTerms, diretorio, 0)
    # Depois o diretório é reescrita novamente.
    arquivo = readfile(diretorio)
    dictionaryTerms = openCache()
    dictionaryTerms = InvertedIndex(arquivo, dictionaryTerms)
    addCache(dictionaryTerms)


# Leitura do cache para diretório e retornar array com diretório indexados.
def cacheDirectory():
    lista = []
    with open("diretorios.cache", "r", encoding='utf-8') as cache:
        cacheDiretorio = cache.readlines()
        for i in cacheDiretorio:
            a = i.split("\n")
            for line in a:
                if line != "":
                    lista.append(line)
    return lista


# Adicionar os caminhos indexados no cache para diretório.
def addCacheDirectory(diretorio):
    with open("diretorios.cache", "a", encoding='utf-8') as cache:
        cache.write(diretorio)
        cache.write("\n")


def updateDirectory(listaCacheDirectory, directory):
    if os.path.isdir(directory):
        for i in range(len(listaCacheDirectory.copy())):
            if len(listaCacheDirectory) > i:
                if listaCacheDirectory[i] == directory:
                    del (listaCacheDirectory[i])

    with open("diretorios.cache", "w", encoding='utf-8') as cache:
        for line in listaCacheDirectory:
            cache.write(line)
            cache.write(f"\n")


def helpIndexar():
    print("┌─────────┬───────────────────────────────────────────────────────────┐\n"
          "│   -b    │             Buscar termo em um diretório.                 │\n"
          "│         │                                                           │\n"
          "│    1.   │  --> É necessário primeiro o argumento [-b],              │\n"
          "│         │   e depois o termo que deve ser buscado.                  │\n"
          "│    2.   │  --> O termo não deve possuir espaço.                     │\n"
          "│    3.   │  --> Preposições não são armazenadas pelo sistema, então  │\n"
          "│         │   o usuário deve buscar apenas palavras úteis.            │\n"
          "└─────────┴───────────────────────────────────────────────────────────┘\n")


def helpRemover():
    print("┌─────────┬─────────────────────────────────────────────────────────────────┐\n"
          "│   -r    │             Remover diretório/file do índice.                   │\n"
          "│         │                                                                 │\n"
          "│    1.   │   --> Arquivos e diretórios podem ser removidos.                │\n"
          "│    2.   │   --> É necessário colocar aspas ('') no caminho do diretório   │\n"
          "│         │   ou do file.                                                   │\n"
          "└─────────┴─────────────────────────────────────────────────────────────────┘\n")
