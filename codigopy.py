import os
from tabulate import tabulate

# Lista de palavras reservadas
RESERVED_WORDS = [
    "int", "float", "return", "if", "else", "for", "while", "break",
    "continue", "void", "char", "double", "include", "define"
]


class LexicalAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.content = []
        self.position = 0
        self.tokens = []
        self.symbol_table = {}

    def load_file(self):
        try:
            # Verificar se o arquivo existe
            if not os.path.isfile(self.filename):
                raise FileNotFoundError(f"Arquivo '{self.filename}' não encontrado.")

            print(f"Tentando abrir o arquivo: {os.path.abspath(self.filename)}")
            with open(self.filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    raise Exception("Arquivo vazio!")
                self.content = list(content)
                print("Conteúdo do arquivo lido com sucesso:")
                print(content)
        except Exception as e:
            print(f"Erro Léxico: {e}")
            exit(1)

    def is_end_of_file(self):
        return self.position >= len(self.content)

    def next_char(self):
        if self.is_end_of_file():
            return None
        char = self.content[self.position]
        self.position += 1
        return char

    def peek_char(self):
        if self.is_end_of_file():
            return None
        return self.content[self.position]

    def back(self):
        self.position -= 1

    def is_letter(self, char):
        return char.isalpha()

    def is_digit(self, char):
        return char.isdigit()

    def is_whitespace(self, char):
        return char in ' \t\n\r'

    def is_operator(self, char):
        return char in "+-*/=><!&|"

    def is_delimiter(self, char):
        return char in "(),{}[];"

    def tokenize(self):
        while not self.is_end_of_file():
            char = self.next_char()

            # Ignorar espaços em branco
            if self.is_whitespace(char):
                continue

            # Identificar palavras reservadas ou identificadores
            if self.is_letter(char):
                term = char
                while self.peek_char() and (self.is_letter(self.peek_char()) or self.is_digit(self.peek_char())):
                    term += self.next_char()
                if term in RESERVED_WORDS:
                    self.tokens.append(("RESERVED", term))
                else:
                    self.tokens.append(("IDENTIFIER", term))
                    self.update_symbol_table(term)

            # Identificar números
            elif self.is_digit(char):
                term = char
                while self.peek_char() and self.is_digit(self.peek_char()):
                    term += self.next_char()
                self.tokens.append(("NUMBER", term))

            # Identificar operadores
            elif self.is_operator(char):
                next_char = self.peek_char()
                if next_char and (char + next_char) in ["==", "!=", "<=", ">=", "&&", "||"]:
                    self.tokens.append(("OPERATOR", char + self.next_char()))
                else:
                    self.tokens.append(("OPERATOR", char))

            # Identificar delimitadores
            elif self.is_delimiter(char):
                self.tokens.append(("DELIMITER", char))

            # Strings entre aspas
            elif char == '"':
                term = ""
                while self.peek_char() and self.peek_char() != '"':
                    term += self.next_char()
                self.next_char()  # Consumir o fechamento da aspa
                self.tokens.append(("STRING", term))

            # Caso contrário, erro léxico
            else:
                print(f"Erro Léxico: Caractere inválido '{char}' encontrado.")
                exit(1)

    def update_symbol_table(self, symbol):
        if symbol not in self.symbol_table:
            self.symbol_table[symbol] = len(self.symbol_table) + 1

    def print_tables(self):
        # Tabela de Tokens
        print("\nLISTA DE TOKENS:")
        token_table = [(i + 1, token_type, token_value) for i, (token_type, token_value) in enumerate(self.tokens)]
        print(tabulate(token_table, headers=["#", "Tipo", "Valor"], tablefmt="grid"))

        # Tabela de Símbolos
        print("\nTABELA DE SÍMBOLOS:")
        symbol_table = [(index, symbol) for symbol, index in self.symbol_table.items()]
        print(tabulate(symbol_table, headers=["#", "Símbolo"], tablefmt="grid"))


def main():
    filename = "input.txt"

    # Tentar usar caminho absoluto se o arquivo não estiver no mesmo diretório
    if not os.path.isfile(filename):
        print(f"Arquivo '{filename}' não encontrado no diretório atual. Tentando caminho absoluto...")
        filename = os.path.join(os.getcwd(), "input.txt")

    analyzer = LexicalAnalyzer(filename)
    analyzer.load_file()
    analyzer.tokenize()
    analyzer.print_tables()


if __name__ == "__main__":
    main()
