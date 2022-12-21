# Trabalho 1 - Fundamentos de Sistemas Embarcados

## Aluno

| Matrícula  | Aluno                      |
| ---------- | -------------------------- |
| 19/0012307 | Eduardo Afonso Dutra Silva |

<br>

## Intalação

Após clonar o repositório, acesse a pasta e execute os seguintes comandos:

- Copie a pasta `app` para a raspberry pi:
```
scp -P <porta> -r app/* <login>@<ip>:<diretório>
```

- acesse a raspberry pi:
```
ssh <login>@<ip> -p <porta>
```

- acesse o diretório onde os arquivos foram enviados

- instale as dependências:
```
pip install -r requirements.txt
```
<br>

## Execução

- A execução tanto do servidor central quanto das salas distribuídas se dá pelo comando:

```
python3 main.py [OPTIONS]
```

- Sendo que para o servidor central as opções devem ser

```
python3 main.py S <sala usada para execução (número entre 1 e 4)>
```

- E para a execução do servidor distribuído:

```
python3 main.py R <sala usada para execução> <sala do servidor central>
```
