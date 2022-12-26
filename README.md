# Desafio Técnico

## Exercício proposto
Criar uma API que recebe uma imagem e utiliza um sistema de filas para mudar seu tamanho para as proporções 384x384

## Tecnologias utilizadas
- FastAPI - Como framework python
- Celery - Para distribuição de tarefas
- RabbitMQ - Com broker de mensageria
- Redis - Como backend do celery
- Pytest - Para testes unitários

## Fluxo geral
Após bater na rota /resize, a imagem é transformada em uma string base64 e passada para a função resize_image que é uma task Celery, responsável por enviar a solicitação a uma fila do RabbitMQ com o método Delay. O resultado conseguimos acessar por conta do redis, pelo método get. A imagem é tranformada de novo para bytes e retornada na response

## Pré Requisitos para utilizar
Docker (> 20.10) e Docker Compose (> 2.8) instalados. 
Para mais informações de instalação acesse https://docs.docker.com/get-docker/

## Como rodar
Com os pré requisitos instalados, clonar o projeto e rodar o comado 'make up' dentro do diretório. Para parar a aplicação basta rodar 'make down'

## Como rodar os testes unitários
Rodar o comando 'make test' dentro do diretório do projeto

## Como testar
### Com postman:
1. Selecionar a aba 'body'
2. Marcar a opção 'form-data'
3. Em 'key' Utilizar como formato o tipo 'file' (passar o mouse por cima do campo e clicar na setinha a direita)
4. Selecionar um arquivo de imagem JPG ou PNG do seu computador
5. Enviar a solicitação com método POST no ip local, porta 8000

### Com cURL:
1. Utilize o seguinte comando, substituindo o \<PATH\> pelo path do arquivo JPG ou PNG a partir da sua máquina (exemplo: /home/user/image.png). Troque o \<FILE\> pelo nome que desejar para a imagem redimensionada, resultado da request (não esqueça de usar a mesma extensão que o arquivo de input). O arquivo será criado na pasta do projeto:
``` 
curl -L -X POST 'http://127.0.0.1:8000/resize' \
-F 'file=@"<PATH>"' \
-o <FILE>
```

## Extras propostos
### *Se o tamanho for parametrizável como você mudaria a sua arquitetura?*
Usaria um campo extra 'size' na request, passaria ele de parâmetro para a função resize_image e utilizaria esse valor na função de resize do Pillow
### *Qual a complexidade da sua solução?*
Quanto complexidade de desenvolvimento, tentei fazer o mais simples possível, deixei a maior parte das configurações como padrão. A solução em si consiste em apenas dois arquivos (main e tasks) que juntos não somam 50 linhas e são fáceis de manusear.   
Já de análise assintótica, temos: O(1) *Constante* para o envio e O(n) *linear* para memória e enfileiramento
### *É possível melhorar a performance da solução? Como as melhorias impactam a leitura e manutenção do código?*
É sim. Como comentei, utilizei as configurações padrão, mas é possivel modificar campos do Celery como Timeout, número de workers, quantidade de filas e também do FastAPI além de configurar variáveis de ambientes. Nesse caso, utilizaria um arquivo separado de configuração e um .env para não poluir e deixar as coisas separadas, facilitando alterações futuras. Na parte de teste, fiz apenas um pra testar a função principal do desafio, mas faria também testes da API, testando diferentes respostas para situações diferentes como request em branco ou tipo de arquivo inválido
### *De que forma o sistema pode escalar com a arquitetura planejada?*
Como utilizei o Celery, caso seja necessário escalar a aplicação é simples de fazer, adicionando novas rotas no main e novas funções em tasks. Além disso, podemos facilmente aumentar o número de workers e configurar mais filas no rabbitmq