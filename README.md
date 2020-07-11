# Uberaba ChatBot (Mônica)

<p>Projeto de ChatBot (assistente virtual) capaz de oferecer serviços e informações a respeito da cidade de Uberaba. Carinhosamente chamada de Mônica, o assistente é capaz de fornecer informações a respeito de eventos da cidade, shoppings, cinemas, clima, entre outros assuntos pertinentes já aplicados ou ainda em previsão, tudo através do Telegram.</p>

## Features

<ul>
  <li>Calendário de eventos e feriados</li>
  <li>Chamados de emergência</li>
  <li>Clima</li>
  <li>Filmes em cartaz
    <ul>
      <li>Cinemais</li>
      <li>Kinoplex</li>
    </ul>
  </li>
  <li>Notícias</li>
  <li>Notificações</li>
  <li>Shoppings
    <ul>
      <li>Praça Shopping</li>
      <li>Uberaba Shopping</li>
    </ul>
  </li>
</ul>

## Modo de uso

<p>Todas as features são acessadas pelo arquivo do chatbot, isto é, monica.py. O chatbot recebe uma requisição e retorna sua resposta. A comunicação entre o chatbot e o usuário deve ser feita através de uma interface. Neste caso, esta comunicação é realizada através de um bot no Telegram, chamado <a href=https://t.me/monica_urabot>@monica_urabot</a>.</p>
<p>Para permitir a atividade do bot no Telegram, é necessário que o script server.py esteja em execução. Desta forma, o bot permanece capaz de receber e responder requisições. Por outro lado, se o interesse é de apenas enviar uma mensagem ou notificação para os usuários cadastrados no banco de dados através do Telegram, utiliza-se o script alert.py, alterando os campos de mensagens conforme o desejado.</p>

## Detalhamento de Features

### Calendário de feriados

<p>Utiliza da API Google Calendar para obter a agenda de feriados nacionais. Permite a inserção de um calendário pessoal de eventos (eventos municipais, por exemplo). Para tal, basta ter o calendário criado no Google Calendar, e inserir o id do calendário no arquivo my_calendar.py.</p>

### Chamados de emergência

<p>Proposta para acionar serviços de emergência como bombeiros, ambulância ou polícia, todos através da iteração com o chatbot. A feature é parcialmente funcional, reconhecendo o escopo da solicitação, direcionando ao melhor setor de atendimento, e reconhecendo o endereço da ocorrência. Contudo, não existe qualquer serviço sendo realmente acionado em resposta ao uso do chatbot.</p>

### Clima

<p>Retorna detalhes do clima atual na cidade de Uberaba através da API de clima HG Brasil.</p>

### Filmes em Cartaz

<p>Oferece a lista de filmes em cartaz em qualquer um dos dois cinemas de Uberaba: Cinemais ou Kinoplex.</p>

### Notícias

<p>Apresenta os chamados das últimas notícias encontradas no site do Jornal de Uberaba.</p>

### Notificações

<p>Permite ao controlador enviar notificações a todos os usuários cadastrados <b>que deixaram abilitado o recebimento de notificações</b>. Esta feature tem a finalindade de lançar alertas de interesse da comunidade de Uberaba, como eventuais reformas ou acidentes no trânsito, bem como perigos a nível municipal.</p>

### Shoppings

<p>Disponibiliza uma listagem de todas as lojas atualmente em funcionamento no shopping requisitado.</p>

## Requisitos

<p>O requirements.txt ainda será disponibilizado. Além das bibliotecas, também é necessário um token de chatbot do Telegram, bem como credentials.json e token.picle do Google Calendar API, junto a um token da API HGBrasil. O passo-a-passo para obtenção e aplicação correta destes itens será disponibilizado em breve.</p>
