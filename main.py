# Versão do PYTHON: 3.10

# /*******************************************************************************
# Autor: Naila
# Componente Curricular: Algoritmos I
# Concluido em: 02/07/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************/

import os

# Importação do módulo ArgParse
from argparse import ArgumentParser

# Importação do módulo com as funções utilizadas para fazer o sistema.
import mod


# Função para criação das linhas de comando.
def main():
    mod.check()
    dictionaryTerms = {}

    parser = ArgumentParser(prog="HEALTH SEARCH",
                            usage="\n"
                                  "┌─────────┬────────────────────────────────────────┐\n"
                                  "│   -i    │   Indexar diretório.                   │\n"
                                  "│   -b    │   Buscar termo em um diretório.        │\n"
                                  "│   -v    │   Visualizar índice.                   │\n"
                                  "│   -r    │   Remover diretório/file do índice. │\n"
                                  "│   -h    │   Ajuda para compreender o sistema.    │\n"
                                  "└─────────┴────────────────────────────────────────┘\n")

    # Criação de linhas de comando que só funcionam de forma única.
    # Ou seja, só pode ser utilizada uma por vez.
    group = parser.add_mutually_exclusive_group()

    # Adição do argumento em conjunto com a ajuda e a ação para guardar o argumento.
    group.add_argument("-i", "--indexar", help="Indexar arquivos em um diretório.", action="store")
    group.add_argument("-b", "--buscar", help="Buscar termo em um diretório", action="store")
    group.add_argument("-r", "--remover", help="Remover diretório do índice", action="store")
    group.add_argument("-v", "--visualizar", help="Visualizar índice", action="store_true")

    args = parser.parse_args()
    # Se a opção escolhida for "-i".
    if args.indexar is not None:
        # Chamar a função de listar os diretórios já indexados.
        directoryList = mod.cacheDirectory()

        if os.path.isdir(args.indexar):
            # Se o dicionário não foi indexado, ele é indexado ao índice invertido e adiconado no file de armazenamento.
            if args.indexar not in directoryList:
                file = mod.readfile(args.indexar)
                dictionaryTerms = mod.openCache()
                dictionaryTerms = mod.InvertedIndex(file, dictionaryTerms)
                mod.addCache(dictionaryTerms)
                mod.addCacheDirectory(args.indexar)
                print("\nDiretório indexado com sucesso!\n")

            # Se o dicionário já foi indexado antes, ele é apenas atualizado.
            elif args.indexar in directoryList:
                dictionaryTerms = mod.openCache()
                mod.update(dictionaryTerms, args.indexar)
                print("\nDiretório atualizado com sucesso!\n")

        elif args.indexar.lower() == "help":
            mod.helpIndexar()

        else:
            print("\nÉ necessário utilizar um diretório válido!\n")

    # Se a opção escolhida for "-b".
    elif args.buscar is not None:
        dictionaryTerms = mod.openCache()
        mod.search(args.buscar.lower(), dictionaryTerms)

    # Se a opção escolhida for "-v".
    elif args.visualizar:
        dictionaryTerms = mod.openCache()
        mod.view(dictionaryTerms)

    # Se a opção escolhida for "-r"
    elif args.remover is not None:
        directoryList = mod.cacheDirectory()
        if args.remover.lower() == "help":
            mod.helpRemover()

        else:
            dictionaryTerms = mod.openCache()
            mod.toRemove(dictionaryTerms, args.remover, 1)
            mod.updateDirectory(directoryList, args.remover)

    else:
        print("\nÉ necessário colocar um argumento para utilizar o sistema!\n")
        mod.help_cli()


if __name__ == '__main__':
    main()
