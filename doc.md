# Gerador de Scripts SQL

## Descrição do Projeto

Este é um aplicativo Flask que permite gerar scripts de INSERT para SQL Server a partir de arquivos CSV ou XLSX. O projeto simplifica a criação de scripts de inserção em massa, oferecendo uma interface web intuitiva e recursos de processamento de dados.

## Recursos Principais

- Suporte para arquivos CSV e XLSX
- Interface web amigável
- Geração de scripts SQL em lotes
- Tratamento de diferentes tipos de dados
- Download de scripts gerados

## Requisitos do Sistema

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/joaooliveira10/INSERT-Speeds-up.git
cd INSERT-Speeds-up
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

### requirements.txt
```
flask
pandas
openpyxl
sqlalchemy
```

## Executando o Aplicativo

```bash
python app.py
```

Acesse no navegador: `http://localhost:5000`

## Uso

1. Insira o nome da tabela
2. Especifique as colunas (separadas por vírgula e sem espaços)
3. Faça upload do arquivo CSV ou XLSX
4. Clique em "Gerar Scripts"

### Exemplo de Arquivo de Entrada

| nome   | idade | cidade     |
|--------|-------|------------|
| João   | 30    | São Paulo  |
| Maria  | 25    | Rio        |

### Exemplo de Uso na Interface

- **Nome da Tabela**: usuarios
- **Colunas**: nome, idade, cidade
- **Arquivo**: planilha.xlsx

## Limitações Conhecidas

- Suporte limitado a tipos de dados complexos
- Não realiza conexão direta com banco de dados
- Scripts gerados devem ser revisados antes do uso em produção

## Segurança

- Validação de upload de arquivos
- Tratamento de caracteres especiais
- Geração segura de scripts

## Contribuição

1. Faça um fork do projeto
2. Crie sua branch de feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
