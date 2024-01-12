# Rinha - Dev

## Sobre o projeto
Este projeto foi desenvolvido como um desafio proposto pelo meu amigo e colega de trabalho, Wilson Santos. Surgiu da necessidade de consolidar meus conhecimentos em uma nova linguagem de programação, após meu chefe na empresa onde trabalho solicitar que eu aprendesse Python para contribuir em novos projetos.

Atualmente, o projeto visa promover uma competição amigável entre os desenvolvedores cadastrados na plataforma. Os participantes podem fazer login através do GitHub, cadastrar seus repositórios públicos e serão pontuados com base neles, gerando um ranking dos participantes.
## Pre-requisitos

- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- .env file

## Instruções para .env
1. Crie um GitHub APP: [GitHub Apps](https://docs.github.com/pt/apps/creating-github-apps)

2. Preencha as informaçoes abaixo:
```
GITHUB_CLIENT_ID=seu_client_id_do_github
GITHUB_CLIENT_SECRET=seu_client_secret_do_github
GITHUB_REDIRECT_URI="http://localhost:8000/callback"
URL_HOST="http://localhost:8000"
```

3. Caso vá utilizar com Docker (Confome configurado no `GitHub APP`)
```
GITHUB_REDIRECT_URI="http://localhost:8087/callback"
URL_HOST="http://web:8000"
```

4. Caso vá utilizar LocalHost (Confome configurado no `GitHub APP`)
```
GITHUB_REDIRECT_URI="http://localhost:8000/callback"
URL_HOST="http://localhost:8000/"
```

## Como iniciar (Docker)
1. Clone o repositório ou baixe o arquivo zipado.
  
2. Adicione o arquivo .env a raiz do projeto.
```yaml
Garanta que no seu .env as seguintes variáveis estejam assim:
DOCKER = True
DEBUG = False
```
    
4. Inicie o container do Docker
```bash
docker-compose up -d
```

5. Acesse `http://localhost:8087/`

## Como iniciar (LocalHost)
1. Clone o repositório ou baixe o arquivo zipado.
   
2. Adicione o arquivo .env a raiz do projeto
   

4. Instale o ambiente virtual:

   (WINDOWS)
   ```
   virtualenv ./venv
   ```
   (LINUX)
   ```
   python3 -m venv venv
   ```
5. Ative o ambiente virtal:

   (WINDOWS)
   ```
   .\venv\Scripts\Activate
   ```
   (LINUX)
   ```
   source venv/bin/activate
   ```

6. Insale as dependencias:

   (WINDOWS/LINUX)
   ```
    pip install -r requirements.txt
   ```
 7. Rode o seu projeto com:
    ```
    python manage.py runserver
    ```
    Acesse: `http://localhost:8000/`

## Como utilizar
### Pagina inicial:
Nessa tela você será capaz de:
* Ver o menu de interacão ( Inicio | Ranking | Novidades | Meus Repositorios | Login/Sair )
* Ver o botão de login no corpo do site
* Acessar Ranking, Novidades
* Realizar Login via GitHub
* Tela de Meus repositorios so pode ser acessada após logar
![image](https://github.com/mabeldev/Rinha-Dev/assets/116887689/52620239-2290-4ce5-8893-d04721954be8)

### Meus Repositorios:
Nessa tela você será capaz de:
* Ver os seus repositorios publicos do github
* Ver os seus repositorios salvos no banco de dados do projeto
* Importar um repositorio do github para o banco de dados
* Sincronizar as informações de um projeto do banco de dados pelo github
* Remover um projeto do banco de dados
* Ver informações personalizadas do projeto no banco de dados: ![image](https://github.com/mabeldev/Rinha-Dev/assets/116887689/45b426fa-c039-4c5b-b5a1-e6e1417e1d5e)
![image](https://github.com/mabeldev/Rinha-Dev/assets/116887689/ca710a96-1319-4e75-881a-bd96ffee378b)

### Ranking:
Nessa tela você será capaz de:
* Ver o ranking dos devs cadastrados na Rinha-Dev
![image](https://github.com/mabeldev/Rinha-Dev/assets/116887689/e44f03d4-7c98-4a73-a29c-8281c35473cd)


## Tecnologias utilizadas
* Python
* Django
* Docker
* MySQL
* Gunicorn
* NGINX
  

_ps: as imagens utilizadas nesse site foram geradas por ia (edge image creator)_
