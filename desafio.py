import textwrap


def menu():
    menu = """ \n
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair
    
    """

    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! o valor informado é inválido. @@@")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n=== Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n=== Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n=== Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! @@@")
    else:
        print("\n=== Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print(f"\n{15 * '*'}Extrato{18 * '*'}")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print(f"{40 * '*'}")


def criar_usuario(usuarios):
    cpf = input("\nDigite o CPF (Somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ já existe usuário com esse CPF! @@@")
        return
    nome = input("\nDigite o nome completo: ")
    data_nascimento = input("\nDigite o data de nascimento(dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nr - bairro - cidade/sigla estato: )")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtados[0] if usuarios_filtados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o cpf do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n=== Conta Criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrada! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência\t{conta['agencia']}
            C/C\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        match opcao:
            case "1":
                valor = float(input("Digite o valor a ser depositado: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            case "2":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES)
            case "3":
                exibir_extrato(saldo, extrato=extrato)

            case "4":
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
            case "5":
                listar_contas(contas)

            case "6":
                criar_usuario(usuarios)
            case "0":
                break


main()
