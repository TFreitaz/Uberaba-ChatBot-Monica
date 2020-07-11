import unidecode
import string

# import nltk
import pandas as pd
import requests
import time
from ztools import ztext
import re
from geopy.geocoders import Nominatim
from Calendar import myCalendar
import uracrawler as ura
from database import DataBase


class Chatbot:
    def __init__(self, name="Mônica"):
        self.name = name
        self.user = None
        self.answer = ""
        self.adapters = [
            self.Cancelar,
            self.Agradecimento,
            self.Amb_sent,
            self.Fireman_sent,
            self.Cop_sent,
            self.Emergence_address,
            self.Emergence,
            self.Today_events,
            self.Next_events,
            self.Today_holidays,
            self.Next_holidays,
            self.Kinoplex,
            self.Cinemais,
            self.Cinema,
            self.Praca_shopping,
            self.Ura_shopping,
            self.Shopping,
            self.Clima,
            self.Noticias,
            self.Turnoff_ntf,
            self.Turnon_ntf,
            self.Sair,
            self.Scape,
        ]
        self.classes = {
            "quest": [
                "qual",
                "quais",
                "como",
                "pode",
                "mostre",
                "poderia",
                "gostaria",
                "quero",
                "preciso",
                "que",
                "quando",
                "onde",
                "quanto",
                "quantos",
                "algum",
                "alguns",
            ],
            "calendario": ["eventos", "agenda", "calendario", "compromissos", "compromisso", "evento"],
            "male": ["masculino", "male", "m", "homem", "macho", "man"],
            "female": ["feminino", "female", "f", "w", "mulher", "femea", "woman"],
            "bitcoin": ["bitcoin", "bitplay", "bitscript", "criptomoeda"],
            "movie": ["filme", "filmes"],
            "cinemais": ["cinemais"],
            "kinoplex": ["kinoplex"],
            "emergencia": ["emergencia", "help", "socorro", "ajuda"],
            "cop": [
                "policia",
                "crime",
                "assalto",
                "sequestro",
                "roubo",
                "roubaram",
                "sequestraram",
                "assaltaram",
                "assaltou",
                "policial",
                "sequestrar",
                "roubar",
                "viatura",
                "assaltado",
            ],
            "fireman": ["bombeiro", "bombeiros", "incendio", "fogo", "explosao"],
            "amb": [
                "ambulancia",
                "medico",
                "doente",
                "hospital",
                "clinica",
                "mal",
                "desmaio",
                "desmaiei",
                "desmaiou",
                "acidente",
                "acidentou",
                "acidentado",
                "quebrou",
                "morrendo",
                "morrer",
                "infarto",
                "enfarto",
                "avc",
                "quebrou",
                "quebrei",
                "pulso",
                "pulsação",
            ],
            "venda": ["vender", "vende", "venda"],
            "compra": ["comprar", "compra"],
            "duvida": ["duvida", "questionamento", "pergunta", "saber", "sabe", "pregunta"],
            "intenção": ["quero", "desejo", "preciso", "vou"],
            "sair": ["sair"],
            "sim": ["sim", "positivo", "claro", "isso", "confirma", "confirmo", "s", "sm"],
            "nao": ["nao", "negativo", "n"],
            "agradecimento": ["valeu", "obrigado", "obrigada", "brigado", "vlw"],
            "mostrar": [
                "ver",
                "saber",
                "exibir",
                "mostrar",
                "classe",
                "classifico",
                "classificacao",
                "classificado",
                "classifica",
                "classificar",
                "qualifica",
                "preco",
                "custo",
                "lucro",
                "cotacao",
                "vender",
                "vende",
                "vendo",
                "venda",
            ],
            "dicas": ["dicas", "melhora", "melhor", "ajuda", "nutricao", "nutrientes", "terra", "melhorar", "crescer", "aumentar"],
            "cancelar": ["cancelar", "cancela", "outro", "errado"],
            "today": ["today", "hoje", "agora"],
            "event": ["evento", "compromisso", "eventos"],
            "next": ["proximo", "proximos", "seguir", "futuro", "futuros", "previsto", "previstos"],
            "holiday": ["feriado", "ferias", "folga", "feriados"],
            "shopping": ["shopping", "shoppings"],
            "praca": ["praca", "novo", "menor"],
            "urashopping": ["uberaba", "center", "antigo", "velho", "maior"],
            "filme": ["filme", "filmes", "movie", "movies", "cinema", "cinemas"],
            "loja": ["lojas", "estabelecimentos", "loja", "estabelecimento"],
            "clima": ["clima", "tempo", "previsao", "weather", "chover", "chuva", "sol", "temperatura"],
            "news": ["noticia", "noticias", "novidade", "novidades", "jornal"],
            "turnoff": ["desativar", "off", "parar", "pare", "desative"],
            "turnon": ["ativar", "ligar", "começar", "start", "ative", "ligue"],
            "notify": ["notificacao", "notificacoes", "notificar", "alerta", "alertas"],
        }
        self.chats = {}
        self.classification = []

        self.send_cep = None

    def ClearText(self, text):
        # stemmer = nltk.stem.RSLPStemmer()
        if type(text) == str:
            x = text.split()
        else:
            x = text
        if type(x) == list:
            newx = list()
            for word in x:
                w = word.lower()
                w = unidecode.unidecode(w)
                for c in list(string.punctuation):
                    w = w.replace(c, " ")
                if len(w) > 0:
                    if w[-1] == " ":
                        w = w[:-1]
                    # print('{} -> {}'.format(word, w))
                newx.append(w)
            text = " ".join(newx)
        else:
            text = " ".join(text)
        return text

    def insert(self, message):
        if user not in self.chats.keys():
            self.chats[user] = [message]
        else:
            self.chats[user].append(message)

    def address(self, ans):
        if not any(x == "uberaba" for x in ztext.ClearText(ans).split()):
            ans += " uberaba"
        geolocator = Nominatim(user_agent="monica_bot")
        location = geolocator.geocode(ans)
        if location:
            location = location[0].split(", ")[0]
        return location

    def number(self, ans):
        num = re.findall(r"\d+", ans)
        if len(num) > 0:
            return num[0]
        else:
            return None

    def send(self, ans):
        # self.answer = 'Zeca: ' + ans
        self.answer = ans
        return self.answer

    def start_talk(self):
        self.send("Olá! Como posso te ajudar?")
        return self.answer

    def classific(self, message):
        for word in self.classes.keys():
            if any(x in self.classes[word] for x in self.ClearText(message).split()):
                self.classification.append(word)

    def get_response(self, message):
        self.classific(message)
        for adap in self.adapters:
            ans = adap(message)
            if ans:
                return self.send(ans)

    def match(self, reqs):
        if all(x in self.classification for x in reqs):
            return True
        else:
            return False

    def Cancelar(self, message):
        reqs = ["cancelar"]
        if self.match(reqs):
            answer = "Tudo bem. Como posso te ajudar então?"
            self.classification = []
            return answer

    def Agradecimento(self, message):
        reqs = ["agradecimento"]
        if self.match(reqs):
            answer = "Se precisar, é só chamar."
            blocks = ["agradecimento"]
            self.classification = list(filter(lambda a: a not in blocks, self.classification))
            return answer

    def Amb_sent(self, message):
        reqs = ["amb", "address", "case", "number"]
        if self.match(reqs):
            answer = f"Está sendo enviada uma ambulância para o endereço {self.case_address} n° {self.case_number}. Para mais informações, disque 192."
            self.classification = ["sent_help"]
            return answer

    def Fireman_sent(self, message):
        reqs = ["fireman", "address", "case", "number"]
        if self.match(reqs):
            answer = f"Está sendo enviada uma equipe para o endereço {self.case_address} n° {self.case_number}. Para mais informações, disque 193."
            self.classification = ["sent_help"]
            return answer

    def Cop_sent(self, message):
        reqs = ["cop", "address", "case", "number"]
        if self.match(reqs):
            answer = f"Está sendo enviada uma viatura para o endereço {self.case_address} n° {self.case_number}. Para mais informações, disque 190."
            self.classification = ["sent_help"]
            return answer

    def Emergence_address(self, message):
        reqs = ["emergencia", "address"]
        if self.match(reqs):
            if not self.case_address:
                self.case_address = self.address(message)
            if self.case_address:
                if not self.case_number:
                    self.case_number = self.number(message)
                if self.case_number:
                    self.classification.append("number")
                    if not self.match(["caso"]):
                        answer = "Qual é o caso?"
                        self.classification.append("case")
                    elif not any(self.match(x) for x in [["cop"], ["fireman"], ["amb"]]):
                        answer = "Qual serviço você deseja exatamente?"
                else:
                    answer = "Qual o número do local?"
            else:
                answer = "Não encontrei seu endereço. Tente novamente"
            return answer

    def Emergence(self, message):
        reqs = ["emergencia"]
        reqs_2 = ["cop"]
        reqs_3 = ["amb"]
        reqs_4 = ["fireman"]
        if self.match(reqs) or self.match(reqs_2) or self.match(reqs_3) or self.match(reqs_4):
            self.case_address = None
            self.case_number = None
            if "address" not in self.classification:
                answer = "Qual o endereço?"
                self.classification.append("address")
            return answer

    def Today_events(self, message):
        reqs = ["event", "today"]
        if self.match(reqs):
            events = myCalendar.today_events(Id=myCalendar.urapython_id)
            if len(events) == 0:
                answer = "Nós não temos nenhum evento para hoje!"
            else:
                answer = "Estes são nossos eventos de hoje:\n"
                for event in events:
                    answer += "\n{} - {}".format(event["start"], event["name"])
            self.classification = []
            return answer

    def Next_events(self, message):
        reqs = ["event"]
        if self.match(reqs):
            events = myCalendar.next_events(Id=myCalendar.urapython_id)
            if len(events) == 0:
                answer = "Nós não temos nenhum evento previsto."
            else:
                answer = "Estes são nossos próximos eventos:\n"
                for event in events:
                    answer += "\n{} - {}".format(event["start"], event["name"])
            self.classification = []
            return answer

    def Today_holidays(self, message):
        reqs = ["holiday", "today"]
        if self.match(reqs):
            events = myCalendar.today_events(Id=myCalendar.holidays_id)
            if len(events) == 0:
                answer = "Nós não temos nenhum feriado hoje!"
            else:
                answer = "Este é o nosso feriado de hoje:\n"
                for event in events:
                    answer += "\n{} - {}".format(event["start"], event["name"])
            self.classification = []
            return answer

    def Next_holidays(self, message):
        reqs = ["holiday"]
        if self.match(reqs):
            events = myCalendar.next_events(Id=myCalendar.holidays_id)
            if len(events) == 0:
                answer = "Nós não temos nenhum feriado previsto."
            else:
                answer = "Estes são nossos próximos feriados:\n"
                for event in events:
                    answer += "\n{} - {}".format(event["start"], event["name"])
            self.classification = []
            return answer

    def Kinoplex(self, message):
        reqs = ["kinoplex"]
        if self.match(reqs):
            movies = ura.kinoplex()
            if len(movies) > 0:
                answer = "Estes são os filmes que estão passando no Kinoplex Uberaba:\n\n"
                for movie in movies:
                    answer += f" - {movie}\n"
            else:
                answer = "Não achei nenhum filme disponível no Kinoplex hoje."
            self.classification = []
            return answer

    def Cinemais(self, message):
        reqs = ["cinemais"]
        if self.match(reqs):
            movies = ura.cinemais()
            if len(movies) > 0:
                answer = "Estes são os filmes que estão passando no Cinemais Uberaba:\n\n"
                for movie in movies:
                    answer += f" - {movie}\n"
            else:
                answer = "Não achei nenhum filme disponível no Cinemais hoje."
            self.classification = []
            return answer

    def Cinema(self, message):
        reqs = ["filme"]
        if self.match(reqs):
            answer = "Temos dois cinemas em Uberaba:\n"
            answer += " - Cinemais\n"
            answer += " - Kinoplex\n\n"
            answer += "Sobre qual deseja saber?"
            return answer

    def Praca_shopping(self, message):
        reqs = ["praca", "loja", "shopping"]
        if self.match(reqs):
            lojas = ura.praca_shopping()
            answer = "Estas são as lojas do Uberaba Praça Shopping:\n\n"
            for loja in lojas:
                answer += f" - {loja}\n"
            self.classification = []
            return answer

    def Ura_shopping(self, message):
        reqs = ["urashopping", "loja", "shopping"]
        if self.match(reqs):
            lojas = ura.uberaba_shopping()
            answer = "Estas são as lojas do Shopping Uberaba:\n\n"
            for loja in lojas:
                answer += f" -{loja}\n"
            self.classification = []
            return answer

    def Shopping(self, message):
        reqs = ["shopping"]
        if self.match(reqs):
            answer = "Temos dois shoppings principais em Uberaba:\n"
            answer += " - Praça Shopping\n"
            answer += " - Uberaba Shopping\n\n"
            return answer

    def Clima(self, message):
        reqs = ["clima"]
        if self.match(reqs):
            results = ura.weather()["results"]
            today = results["forecast"][0]
            answer = "Aqui está:\n\n"
            answer += f'Uberaba, {today["date"]}\n'
            answer += f'Temperatura atual: {results["temp"]} ºC\n'
            answer += f'Agora: {results["description"]}\n'
            answer += f'Ao longo do dia: {today["description"]}\nMáxima: {today["max"]} ºC\nMínima: {today["min"]} ºC'
            self.classification = []
            return answer

    def Noticias(self, message):
        reqs = ["news"]
        if self.match(reqs):
            noticias = ura.news()[:5]
            answer = "Aqui está:\n\n"
            for noticia in noticias:
                answer += f"{noticia[0]} - {noticia[1]}.\n"
                answer += f"\t{noticia[2]}\n\n"
            self.classification = []
            return answer

    def Turnoff_ntf(self, message):
        reqs = ["turnoff", "notify"]
        if self.match(reqs):
            uradb = DataBase()
            uradb.update_user(self.user[0], {"notification": 0})
            answer = "Ok, suas notificações foram desativadas. Para ativá-las novamente é só me pedir."
            return answer

    def Turnon_ntf(self, message):
        reqs = ["turnon", "notify"]
        if self.match(reqs):
            uradb = DataBase()
            uradb.update_user(self.user[0], {"notification": 1})
            answer = "Ok, suas notificações foram ativadas. Para desativá-las é só me pedir."
            return answer

    def Sair(self, message):
        reqs = ["sair"]
        if self.match(reqs):
            answer = "Espero ter ajudado. Até mais!"
            self.classification = []
            return answer

    def Scape(self, message):
        answer = "Sinto muito, mas não entendi."
        return answer


# bot = Chatbot()
# print(f'{bot.name}: {bot.start_talk()}')
# while True:
#    message = input('Usuário: ')
#    if message == 'stop_all':
#        break
#    ans = bot.get_response(message)
#    print(f'{bot.name}: {ans}')
