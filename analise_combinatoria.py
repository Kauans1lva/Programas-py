from itertools import combinations

def encontrar_combinacoes(numeros, alvo):
    """
    Gera todas as combinações de números que somam aproximadamente ao valor-alvo.

    :param numeros: Lista de números disponíveis.
    :param alvo: Valor-alvo da soma.
    :return: Gerador de combinações que somam ao alvo.
    """
    for r in range(1, len(numeros) + 1):  # Testar combinações de todos os tamanhos
        for combinacao in combinations(numeros, r):
            soma = sum(combinacao)
            if abs(soma - alvo) < 0.01:  # Margem de erro de 0.01
                yield combinacao

def main():
    print("Bem-vindo ao programa de análise combinatória de números!")
    
    while True:  # Loop para continuar pedindo novos valores
        # Solicitar o valor-alvo
        try:
            alvo = input("\nDigite o valor que deseja encontrar (use vírgula para decimais): ").replace(",", ".")
            if alvo.lower() == "sair":
                print("Encerrando o programa. Até logo!")
                break
            alvo = float(alvo)
        except ValueError:
            print("Erro: O valor-alvo deve ser um número válido.")
            continue
        
        # Solicitar os números disponíveis
        try:
            numeros_input = input("Digite os números separados por ponto e vírgula (;), usando vírgula para decimais: ")
            if numeros_input.lower() == "sair":
                print("Encerrando o programa. Até logo!")
                break
            numeros = [float(num.strip().replace(",", ".")) for num in numeros_input.split(";")]
        except ValueError:
            print("Erro: Todos os números fornecidos devem ser válidos.")
            continue
        
        # Exibir os números fornecidos
        print(f"Números fornecidos: {numeros}")
        
        # Encontrar e exibir combinações
        print(f"Procurando combinações que somam aproximadamente {alvo}...")
        combinacoes = encontrar_combinacoes(numeros, alvo)
        encontrou = False
        
        for combinacao in combinacoes:
            encontrou = True
            print(f"Combinação encontrada: {combinacao}")
        
        if not encontrou:
            print(f"Não foi encontrada nenhuma combinação que soma {alvo}.")
        else:
            print("Todas as combinações foram exibidas.")
        
        # Perguntar se o usuário deseja continuar
        print("\nPressione Enter para buscar outro valor ou digite 'sair' para encerrar.")
        if input().strip().lower() == "sair":
            print("Encerrando o programa. Até logo!")
            break

if __name__ == "__main__":
    main()
