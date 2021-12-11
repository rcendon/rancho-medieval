## Rancho Medieval App

---

Trabalho realizado pelo Grupo AlphaSoftwares para fins de aprovação
na disciplina OPE-1 do curso de ADS da Faculdade Impacta de Tecnologia.

### Integrantes

---

1. Daniel Avilla
2. Daniel Cabral
4. Rafael Cendon
5. Vitor

### Descrição

---

Trata-se de sistema criado para automatizar as relações entre vendas  
e baixa no estoque de uma empresa alimentícia fictícia "UltraFood Ali-  
mentos LTDA.", do ramo de restaurantes.

Além disso, o sistema busca ser a interface entre o cliente e a em-  
presa, recebendo e processando os pedidos dos clientes até o fim de  
seu ciclo de vida.

Nesse esteio, o sistema foi implementado como um site (web app) in-  
terativo.

O aplicativo foi dividido em duas seções, uma para os clientes e outra para os administradores e funcionários. 

Para acessar a aplicação online, na seção dos clientes, acesse o link https://rancho-medieval.herokuapp.com/ .

Para acessar a aplicação online, na seção dos funcinoários e administradores, acesse o link https://rancho-medieval.herokuapp.com/login_colaborador .

### Instalação 

Caso se busque instalar o aplicativo localmente, favor clonar esse repositório e 

É pré-requisito para o funcionamento da aplicação que a linguagem de programação Python (versão 3.9) esteja instalada em seu computador e que se utilize um banco de dados PostgreSQL.

Além disso, devem ser instalados os módulos indicados no arquivo "requirements.txt, a partir do seguinte comando no terminal":

~~~

pip install -r requirements.txt

~~~

Por fim, deve-se criar arquivo chamado ".env" dentro do diretório "app", contendo as seguintes informações:

~~~

DATABASE_URL=''

SECRET_KEY=''

~~~



