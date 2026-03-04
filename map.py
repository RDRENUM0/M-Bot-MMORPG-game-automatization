from collections import deque
from typing import Optional

cities = ["Ithan", "Torneg", "Werbin", "Karka-han", "Eder", "Nithal", "Trupia Przełęcz", "Tuzmer", "Thuzal", "Liściaste Rozstaje"]  

map_graph = {

        

    "Ithan": ["Zniszczone Opactwo", "Porzucone Pasieki", "Dolina Yss", "Dom Aukcyjny"],
    "Dom Aukcyjny": ["Ithan"],
    "Zniszczone Opactwo": ["Zburzona Twierdza", "Uroczysko", "Ithan", "Leśny Bród"],
    "Porzucone Pasieki": ["Ithan"],
    "Dolina Yss": ["Ithan", "Orla Grań", "Leśny Bród"],
    "Leśny Bród": ["Dolina Yss", "Zniszczone Opactwo"],
    "Uroczysko": ["Zapomniany Szlak", "Zniszczone Opactwo", "Wichrowe Szczyty"],
    "Mroczny Przesmyk": ["Zapomniany Szlak", "Nawiedzony Jar"],
    "Nawiedzony Jar": ["Zburzona Twierdza", "Mroczny Przesmyk"],
    "Zburzona Twierdza": ["Nawiedzony Jar", "Opuszczony Bastion", "Zniszczone Opactwo"],
    "Opuszczony Bastion": ["Zburzona Twierdza"],
    "Zapomniany Szlak": ["Uroczysko", "Mroczny Przesmyk", "Kamienna Jaskinia - sala 1"],
    "Kamienna Jaskinia - sala 1": ["Zapomniany Szlak", "Kamienna Jaskinia - sala 2"],
    "Kamienna Jaskinia - sala 2": ["Andarum Ilami", "Kamienna Jaskinia - sala 1"],
    


    "Andarum Ilami": ["Skały Mroźnych Śpiewów", "Skały Mroźnych Śpiewów", "Zdradzieckie Przejście p.1", "Śnieżna Grota p.1", "Świątynia Andarum", "Kamienna Jaskinia - sala 2"],
    "Świątynia Andarum": ["Świątynia Andarum - zejście lewe", "Świątynia Andarum - zejście lewe", "Andarum Ilami", "Andarum Ilami", "Świątynia Andarum - zejście prawe", "Świątynia Andarum - zejście prawe"],
    "Świątynia Andarum - zejście prawe": ["Świątynia Andarum", "Świątynia Andarum", "Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia"],
    "Świątynia Andarum - podziemia": ["Świątynia Andarum - magazyn p.1", "Świątynia Andarum - magazyn p.1", "Świątynia Andarum - zejście lewe", "Świątynia Andarum - zejście lewe", "Świątynia Andarum - lokum mnichów", "Świątynia Andarum - lokum mnichów", "Świątynia Andarum - lokum mnichów", "Świątynia Andarum - zejście prawe", "Świątynia Andarum - zejście prawe", "Świątynia Andarum - biblioteka", "Świątynia Andarum - biblioteka"],
    "Świątynia Andarum - biblioteka": ["Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia"],
    "Świątynia Andarum - zejście lewe": ["Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia", "Świątynia Andarum", "Świątynia Andarum"],
    "Świątynia Andarum - magazyn p.1": ["Świątynia Andarum - magazyn p.2", "Świątynia Andarum - magazyn p.2", "Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia"],
    "Świątynia Andarum - magazyn p.2": ["Erem Czarnego Słońca p.4 - sala 2", "Erem Czarnego Słońca p.4 - sala 2", "Świątynia Andarum - zbrojownia", "Świątynia Andarum - zbrojownia", "Świątynia Andarum - magazyn p.1", "Świątynia Andarum - magazyn p.1", "Świątynia Andarum - lokum mnichów", "Świątynia Andarum - lokum mnichów"],
    "Świątynia Andarum - zbrojownia": ["Świątynia Andarum - magazyn p.2", "Świątynia Andarum - magazyn p.2"],
    "Erem Czarnego Słońca p.4 - sala 2": ["Erem Czarnego Słońca p.3", "Erem Czarnego Słońca p.3", "Erem Czarnego Słońca p.3 - południe", "Świątynia Andarum - magazyn p.2", "Świątynia Andarum - magazyn p.2", "Świątynia Andarum - magazyn p.2"],
    "Świątynia Andarum - lokum mnichów": ["Świątynia Andarum - magazyn p.2", "Świątynia Andarum - magazyn p.2", "Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia", "Świątynia Andarum - podziemia", "Krypty Dusz Śniegu p.3", "Krypty Dusz Śniegu p.3"], 
    "Krypty Dusz Śniegu p.3": ["Świątynia Andarum - lokum mnichów", "Świątynia Andarum - lokum mnichów", "Krypty Dusz Śniegu p.2", "Krypty Dusz Śniegu p.2"],
    "Krypty Dusz Śniegu p.2": ["Krypty Dusz Śniegu p.3", "Krypty Dusz Śniegu p.3", "Krypty Dusz Śniegu p.3 - komnata Lisza<br>Przejście dostępne do 88 poziomu", "Krypty Dusz Śniegu p.1"],
    "Krypty Dusz Śniegu p.1": ["Krypty Dusz Śniegu p.2", "Cmentarzysko Szerpów", "Cmentarzysko Szerpów"],
    "Cmentarzysko Szerpów": ["Śnieżna Granica", "Śnieżna Granica", "Skały Mroźnych Śpiewów", "Skały Mroźnych Śpiewów", "Skały Mroźnych Śpiewów", "Krypty Dusz Śniegu p.1"],
    "Skały Mroźnych Śpiewów": ["Jaskinia Lodowego Czaru", "Cmentarzysko Szerpów", "Cmentarzysko Szerpów", "Cmentarzysko Szerpów", "Erem Czarnego Słońca p.3 - południe", "Firnowa Grota p.1", "Firnowa Grota p.2", "Erem Czarnego Słońca p.1 - północ", "Erem Czarnego Słońca p.1 - północ", "Lodowa Wyrwa p.1 s.1", "Lodowa Wyrwa p.2", "Zmarzlina Amaimona Soplorękiego - przedsionek<br>Przejście dostępne od 69 do 108 poziomu", "Andarum Ilami", "Andarum Ilami"],
    "Erem Czarnego Słońca p.1 - północ": ["Erem Czarnego Słońca p.2", "Skały Mroźnych Śpiewów", "Erem Czarnego Słońca p.2", "Skały Mroźnych Śpiewów"],
    "Erem Czarnego Słońca p.2": ["Erem Czarnego Słońca p.1 - północ", "Erem Czarnego Słońca p.3", "Erem Czarnego Słońca p.1 - północ", "Erem Czarnego Słońca p.3"],
    "Erem Czarnego Słońca p.3": ["Erem Czarnego Słońca p.4 - sala 1", "Erem Czarnego Słońca p.4 - sala 1", "Erem Czarnego Słońca p.2", "Erem Czarnego Słońca p.2", "Erem Czarnego Słońca p.4 - sala 2", "Erem Czarnego Słońca p.4 - sala 2"],
    "Erem Czarnego Słońca p.3 - południe": ["Skały Mroźnych Śpiewów", "Skały Mroźnych Śpiewów", "Erem Czarnego Słońca p.4 - sala 2"],
    "Lodowa Wyrwa p.1 s.1": ["Skały Mroźnych Śpiewów", "Lodowa Wyrwa p.1 s.2", "Lodowa Wyrwa p.2"],
    "Lodowa Wyrwa p.2": ["Lodowa Wyrwa p.1 s.1", "Skały Mroźnych Śpiewów"],
    "Lodowa Wyrwa p.1 s.2": ["Sala Lodowych Iglic", "Lodowa Wyrwa p.1 s.1"],
    "Sala Lodowych Iglic": ["Lodowa Wyrwa p.1 s.2"],
    "Zdradzieckie Przejście p.1": ["Wylęgarnia Choukkerów p.1", "Zdradzieckie Przejście p.2", "Głębokie Skałki p.2", "Głębokie Skałki p.1", "Andarum Ilami"],



    "Eder": ["Spokojne Przejście", "Spokojne Przejście", "Spokojne Przejście", "Dom Mrocznego Zgrzyta", "Teatr Monticolo - foyer", "Opuszczony dom<br>(Wymaga klucza)", "Dom Schadzek", "Dom Schadzek", "Teatr Monticolo - wejście od zaplecza<br>(Wymaga klucza)", "Dom Burmistrza", "Magazyn Eder", "Fort Eder", "Fort Eder", "Fort Eder", "Fort Eder", "Siedziba Kultystów", "Rudera<br>(Wymaga klucza)", "Karczma pod Posępnym Czerepem", "Dom Mikliniosa", "Pracownia Bonifacego", "Gościniec Bardów", "Gościniec Bardów", "Gościniec Bardów", "Dom Artenii i Tafina", "Targ Poszukiwaczy Przygód", "Dom Erniego", "Zbójecka spiżarnia<br>(Wymaga klucza)", "Siedziba Maga", "Siedziba Maga", "Dom Etrefana", "Grota Złoczyńców p.1"],
    "Spokojne Przejście": ["Zasłonięte Jezioro", "Zasłonięte Jezioro", "Racicowy Matecznik", "Racicowy Matecznik", "Eder", "Eder", "Eder"],
    "Racicowy Matecznik": ["Ukwiecona Skarpa", "Ukwiecona Skarpa", "Ukwiecona Skarpa", "Pieczara Kwiku - sala 1", "Spokojne Przejście", "Spokojne Przejście", "Gościniec Bardów", "Gościniec Bardów"],
    "Ukwiecona Skarpa": ["Kwieciste Przejście", "Kwieciste Przejście", "Racicowy Matecznik", "Racicowy Matecznik", "Racicowy Matecznik"],
    "Pieczara Kwiku - sala 1": ["Racicowy Matecznik", "Pieczara Kwiku - sala 2<br>Przejście dostępne do 72 poziomu"],
    "Gościniec Bardów": ["Racicowy Matecznik", "Racicowy Matecznik", "Eder", "Eder", "Nizina Wieśniaków", "Eder", "Nizina Wieśniaków", "Nizina Wieśniaków", "Wertepy Rzezimieszków", "Wertepy Rzezimieszków"],
    "Fort Eder": ["Las Goblinów", "Las Goblinów", "Pieczara Niepogody p.2 - sala 2", "Pieczara Niepogody p.1", "Fortyfikacja p.3", "Fortyfikacja p.1", "Fortyfikacja p.3", "Fortyfikacja p.1", "Eder", "Fortyfikacja p.5", "Eder", "Mokradła", "Eder", "Mokradła", "Eder", "Mokradła", "Ciemnica Szubrawców p.1 - sala 1", "Stary Kupiecki Trakt", "Stary Kupiecki Trakt"],
    "Las Goblinów": ["Podmokła Dolina", "Podmokła Dolina", "Fort Eder", "Fort Eder"],
    "Stary Kupiecki Trakt": ["Fort Eder", "Fort Eder", "Ciemnica Szubrawców p.1 - sala 3", "Stukot Widmowych Kół", "Stukot Widmowych Kół", "Moczary Rybiego Oka", "Moczary Rybiego Oka"],
    "Stukot Widmowych Kół": ["Wertepy Rzezimieszków", "Wertepy Rzezimieszków", "Wertepy Rzezimieszków", "Stary Kupiecki Trakt", "Stary Kupiecki Trakt"],
    "Wertepy Rzezimieszków": ["Gościniec Bardów", "Gościniec Bardów", "Stukot Widmowych Kół", "Stukot Widmowych Kół", "Stukot Widmowych Kół", "Chata szabrowników", "Źródło Narumi", "Źródło Narumi"],
    "Źródło Narumi": ["Wertepy Rzezimieszków", "Wertepy Rzezimieszków", "Uroczysko Wodnika", "Uroczysko Wodnika", "Podgrodzie Nithal", "Podgrodzie Nithal"],
    "Uroczysko Wodnika": ["Moczary Rybiego Oka", "Źródło Narumi", "Źródło Narumi"],
    "Moczary Rybiego Oka": ["Stary Kupiecki Trakt", "Stary Kupiecki Trakt", "Uroczysko Wodnika"],
    "Mokradła": ["Podmokła Dolina", "Dolina Rozbójników", "Dolina Rozbójników", "Dolina Rozbójników", "Fort Eder", "Fort Eder", "Fort Eder", "Zajazd pod Zielonym Jednorożcem", "Polana Ścierwojadów", "Polana Ścierwojadów", "Skarpiska Tolloków", "Skarpiska Tolloków"],
    "Podmokła Dolina": ["Jaskinia Pogardy<br>Przejście dostępne do 70 poziomu", "Morwowe Przejście", "Morwowe Przejście", "Morwowe Przejście", "Las Goblinów", "Las Goblinów", "Mokradła"],
    "Polana Ścierwojadów": ["Mokradła", "Mokradła", "Ghuli Mogilnik", "Skarpiska Tolloków", "Skarpiska Tolloków", "Legowisko Wilczej Hordy", "Legowisko Wilczej Hordy"],
    "Ghuli Mogilnik": ["Dolina Rozbójników", "Dolina Rozbójników", "Polana Ścierwojadów", "Zapomniany Grobowiec p.1", "Warczące Osuwiska", "Warczące Osuwiska"],
    "Warczące Osuwiska": ["Ghuli Mogilnik", "Ghuli Mogilnik", "Legowisko Wilczej Hordy", "Legowisko Wilczej Hordy", "Wilcza Nora p.1<br>Przejście dostępne do 75 poziomu", "Wilcza Skarpa", "Wilcza Skarpa"],
    "Wilcza Skarpa": ["Warczące Osuwiska", "Warczące Osuwiska", "Legowisko Wilczej Hordy", "Legowisko Wilczej Hordy"],
    "Legowisko Wilczej Hordy": ["Polana Ścierwojadów", "Polana Ścierwojadów", "Skalne Turnie", "Skalne Turnie", "Warczące Osuwiska", "Warczące Osuwiska", "Krasowa Pieczara p.3", "Krasowa Pieczara p.2", "Krasowa Pieczara p.1", "Wilcza Skarpa", "Wilcza Skarpa"],    
    "Krasowa Pieczara p.2": ["Legowisko Wilczej Hordy", "Krasowa Pieczara p.3", "Krasowa Pieczara p.1"],
    "Krasowa Pieczara p.3": ["Krasowa Pieczara p.2", "Legowisko Wilczej Hordy"],
    "Krasowa Pieczara p.1": ["Krasowa Pieczara p.2", "Legowisko Wilczej Hordy"],
    "Skalne Turnie": ["Skarpiska Tolloków", "Skarpiska Tolloków", "Legowisko Wilczej Hordy", "Legowisko Wilczej Hordy"],
    "Skarpiska Tolloków": ["Mokradła", "Mokradła", "Polana Ścierwojadów", "Polana Ścierwojadów", "Skalne Turnie", "Skalne Turnie"],
    "Dolina Rozbójników": ["Przełęcz Łotrzyków", "Przełęcz Łotrzyków", "Przełęcz Łotrzyków", "Mokradła", "Mokradła", "Mokradła", "Kamienna Kryjówka", "Ghuli Mogilnik", "Ghuli Mogilnik"],
    "Kamienna Kryjówka": ["Dolina Rozbójników"],
    "Przełęcz Łotrzyków": ["Dolina Rozbójników", "Dolina Rozbójników", "Dolina Rozbójników", "Orla Grań", "Orla Grań", "Orla Grań", "Pagórki Łupieżców", "Pagórki Łupieżców"],
    "Pagórki Łupieżców": ["Przełęcz Łotrzyków", "Przełęcz Łotrzyków", "Skład Grabieżców", "Schowek na Łupy", "Namiot Bandytów<br>Przejście dostępne do 62 poziomu"],
    "Skład Grabieżców": ["Pagórki Łupieżców"],
    "Schowek na Łupy": ["Pagórki Łupieżców"],

    "Torneg": ["Leśna Przełęcz", "Stare Ruiny", "Łany Zboża"],
    "Orla Grań": ["Dolina Yss", "Dolina Yss", "Przełęcz Łotrzyków", "Przełęcz Łotrzyków", "Przełęcz Łotrzyków", "Spustoszona jaskinia", "Stare Ruiny", "Stare Ruiny", "Przejście Myśliwych p.2", "Przeklęta Strażnica p.2", "Przeklęta Strażnica", "Przeklęta Strażnica", "Przejście Myśliwych p.1", "Dziewicza Knieja", "Dziewicza Knieja"],
    "Przejście Myśliwych p.1": ["Orla Grań", "Przejście Myśliwych p.2"],
    "Przejście Myśliwych p.2": ["Przejście Myśliwych p.1", "Orla Grań"],
    "Dziewicza Knieja": ["Orla Grań", "Orla Grań", "Siedlisko Nietoperzy p.5", "Stare Ruiny", "Stare Ruiny", "Siedlisko Nietoperzy p.1", "Grota Malowanej Śmierci", "Las Tropicieli", "Las Tropicieli"],
    "Las Tropicieli": ["Dziewicza Knieja", "Dziewicza Knieja", "Osada Mulusów"],
    "Osada Mulusów": ["Las Tropicieli", "Pradawne Wzgórze Przodków"],
    "Pradawne Wzgórze Przodków": ["Osada Mulusów", "Dzikie Pagórki", "Dzikie Pagórki"],
    "Dzikie Pagórki": ["Tygrysia Polana", "Jaskinia Dzikich Kotów", "Pradawne Wzgórze Przodków", "Pradawne Wzgórze Przodków"],
    "Jaskinia Dzikich Kotów": ["Tygrysia Polana", "Dzikie Pagórki<br>Przejście dostępne od 20 poziomu"],
    "Tygrysia Polana": ["Leśna Przełęcz", "Leśna Przełęcz", "Jama Kocich Ślepi", "Jaskinia Dzikich Kotów", "Dzikie Pagórki<br>Przejście dostępne od 20 poziomu"],
    "Leśna Przełęcz": ["Torneg", "Torneg", "Dom Vincenta", "Zatopiony Szczyt", "Zatopiony Szczyt", "Lisia jama", "Kryjówka Dzikich Kotów", "Kryjówka Dzikich Kotów", "Tygrysia Polana", "Tygrysia Polana"],
    "Zatopiony Szczyt": ["Stare Ruiny", "Stare Ruiny", "Wóz Vadomy", "Wóz kapeli", "Wóz starego Fonsa i Perhany", "Leśna Przełęcz<br>Przejście dostępne od 18 poziomu", "Leśna Przełęcz<br>Przejście dostępne od 18 poziomu", "Ruiny Szabrowników", "Ruiny Szabrowników"],
    "Stare Ruiny": ["Wilczy Szpic", "Wilczy Szpic", "Wilczy Szpic", "Dom Grambera", "Przeklęty Zamek - wejście północne", "Orla Grań", "Orla Grań", "Torneg", "Torneg", "Torneg", "Przeklęty Zamek - wejście południowe", "Przeklęty Zamek - wejście wschodnie", "Przeklęty Zamek p.2", "Dziewicza Knieja", "Dziewicza Knieja", "Zatopiony Szczyt", "Zatopiony Szczyt"],
    "Wilczy Szpic": ["Łany Zboża", "Łany Zboża", "Dolina Yss", "Dolina Yss", "Jaskinia Wilczego Zamętu p.2", "Jaskinia Wilczego Zamętu p.1", "Stare Ruiny", "Stare Ruiny", "Stare Ruiny"],
    "Łany Zboża": ["Mrowisko", "Wilczy Szpic", "Młyn", "Wilczy Szpic", "Młyn", "Piekarnia", "Piekarnia", "Magazyn", "Magazyn", "Kopiec Mrówek", "Dom Mazteni i Ułtana", "Oberża pod Złotym Kłosem", "Oberża pod Złotym Kłosem", "Torneg", "Torneg"],
    "Mrowisko": ["Mrowisko p.1", "Łany Zboża"],
    "Mrowisko p.1": ["Mrowisko", "Mrowisko p.2"],
    "Mrowisko p.2": ["Mrowisko p.1", "Kopiec Mrówek p.2"],
    "Kopiec Mrówek p.2": ["Mrowisko p.2", "Kopiec Mrówek p.1"],
    "Kopiec Mrówek p.1": ["Kopiec Mrówek p.2", "Kopiec Mrówek"],
    "Kopiec Mrówek": ["Kopiec Mrówek p.1", "Łany Zboża"],
    "Łany Zboża": ["Mrowisko", "Wilczy Szpic", "Młyn", "Wilczy Szpic", "Młyn", "Piekarnia", "Piekarnia", "Magazyn", "Magazyn", "Kopiec Mrówek", "Dom Mazteni i Ułtana", "Oberża pod Złotym Kłosem", "Oberża pod Złotym Kłosem", "Torneg", "Torneg"],
    "Werbin": ["Orcza Wyżyna", "Orcza Wyżyna", "Namiot Amry", "Dom Gepperta - warsztat", "Dom Enoliana", "Kopalnia Latimeria p.1", "Dom Barnesa", "Dom Paratoka", "Namiot wiedźmy", "Karczma pod Fioletowym Kryształem", "Kopalnia Inlefi p.1", "Karczma pod Fioletowym Kryształem", "Dom Rozalii", "Dom Gindera", "Magazyn Krasnoludów", "Wrzosowiska", "Wrzosowiska", "Wrzosowiska", "Dom Jalena i Tafii", "Mury - kwatera główna", "Dom Idropusa", "Dom Idropusa", "Kopalnia Fretar - sala 1", "Opuszczony dom", "Dom Alabraskana", "Brama Północy", "Brama Północy"],
    "Brama Północy": ["Werbin", "Werbin", "Góry Zrębowe", "Góry Zrębowe", "Góry Zrębowe", "Kuźnia na Rozstajach", "Zapomniana kopalnia p.1", "Włości rodu Kruzo", "Włości rodu Kruzo", "Siedziba główna klanu Uchiha<br>(Wymaga klucza)", "Zaginiona Dolina", "Zaginiona Dolina", "Liściasta kryjówka<br>(Wymaga klucza)", "Liściasta kryjówka<br>(Wymaga klucza)", "Skalista Wyżyna", "Skalista Wyżyna"],
    "Góry Zrębowe": ["Namiot pustelnika", "Brama Północy", "Brama Północy", "Brama Północy", "Solna Grota p.1", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Zaginiona Dolina", "Zaginiona Dolina", "Opuszczona Twierdza", "Opuszczona Twierdza"],
    "Zaginiona Dolina": ["Góry Zrębowe", "Góry Zrębowe", "Brama Północy", "Brama Północy", "Opuszczona Twierdza", "Opuszczona Twierdza", "Grobowiec Przodków", "Grobowiec Przodków"],

    "Grobowiec Przodków": ["Zaginiona Dolina", "Zaginiona Dolina", "Czarcie Oparzeliska", "Czarcie Oparzeliska", "Cenotaf Berserkerów - przejście przodków", "Śnieżna Granica"],
    "Cenotaf Berserkerów - przejście przodków": ["Cenotaf Berserkerów p.1 - sala 1", "Grobowiec Przodków", "Grobowiec Przodków"],
    "Cenotaf Berserkerów p.1 - sala 1": ["Cenotaf Berserkerów p.1 - sala 2", "Cenotaf Berserkerów p.1 - sala 2", "Cenotaf Berserkerów - przejście przodków"],
    "Cenotaf Berserkerów p.1 - sala 2": ["Cenotaf Berserkerów p.1 - sala 1", "Cenotaf Berserkerów p.1 - sala 1"],
    "Czarcie Oparzeliska": ["Opuszczona Twierdza", "Opuszczona Twierdza", "Grobowiec Przodków", "Grobowiec Przodków"],
    "Opuszczona Twierdza": ["Góry Zrębowe", "Góry Zrębowe", "Góry Zrębowe", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Mała Twierdza - wieża zachodnia", "Mała Twierdza - mały barak", "Mała Twierdza - mury zachodnie", "Mała Twierdza - mały barak", "Wyjący Wąwóz", "Wyjący Wąwóz", "Mała Twierdza - sala wejściowa", "Mała Twierdza - wieża strażnicza", "Mała Twierdza - wieża wschodnia", "Zaginiona Dolina", "Zaginiona Dolina", "Czarcie Oparzeliska", "Czarcie Oparzeliska"],
    "Mała Twierdza - mały barak": ["Opuszczona Twierdza", "Opuszczona Twierdza"],
    "Mała Twierdza - mury zachodnie": ["Mała Twierdza - wieża zachodnia", "Mała Twierdza - wieża zachodnia", "Opuszczona Twierdza", "Opuszczona Twierdza", "Mała Twierdza - korytarz zachodni", "Mała Twierdza - korytarz zachodni"],
    "Mała Twierdza - wieża zachodnia": ["Mała Twierdza - mury zachodnie", "Opuszczona Twierdza", "Mała Twierdza - mury zachodnie", "Opuszczona Twierdza"],
    "Mała Twierdza - korytarz zachodni": ["Mała Twierdza - mury zachodnie", "Mała Twierdza - mury zachodnie", "Mała Twierdza - sala wejściowa", "Mała Twierdza - sala wejściowa"],
    "Mała Twierdza - sala wejściowa": ["Mała Twierdza - korytarz zachodni", "Mała Twierdza - korytarz zachodni", "Mała Twierdza - magazyn", "Mała Twierdza - sala główna<br>Przejście dostępne do 180 poziomu", "Opuszczona Twierdza", "Mała Twierdza - sala główna<br>Przejście dostępne do 180 poziomu", "Opuszczona Twierdza", "Mała Twierdza p.1", "Mała Twierdza - mury wschodnie", "Mała Twierdza - mury wschodnie"],
    "Mała Twierdza - magazyn": ["Mała Twierdza - sala wejściowa"],
    "Mała Twierdza p.1": ["Mała Twierdza - sala wejściowa"],
    "Mała Twierdza - mury wschodnie": ["Mała Twierdza - sala wejściowa", "Mała Twierdza - sala wejściowa", "Mała Twierdza - wieża wschodnia", "Mała Twierdza - wieża wschodnia"],
    "Mała Twierdza - wieża wschodnia": ["Mała Twierdza - mury wschodnie", "Opuszczona Twierdza", "Mała Twierdza - mury wschodnie", "Opuszczona Twierdza"],
    "Zachodnie Rozdroża": ["Ustronie Widzących Drzew", "Ustronie Widzących Drzew", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór", "Przepastna Grota p.1", "Góry Zrębowe", "Góry Zrębowe", "Góry Zrębowe", "Pieczara Wiatru p.1", "Siedziba Gothic Palladins<br>(Wymaga klucza)", "Opuszczona Twierdza", "Opuszczona Twierdza", "Wyjący Wąwóz"],
    "Ustronie Widzących Drzew": ["Domek Enyi", "Domek Enyi", "Wrzosowiska", "Wrzosowiska", "Zachodnie Rozdroża", "Zachodnie Rozdroża"],
    "Cienisty Bór": ["Ostępy Szalbierskich Lasów", "Ostępy Szalbierskich Lasów", "Ostępy Szalbierskich Lasów", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Zachodnie Rozdroża", "Las Dziwów", "Las Dziwów", "Las Dziwów", "Las Dziwów", "Wyjący Wąwóz", "Wyjący Wąwóz"],
    "Ostępy Szalbierskich Lasów": ["Iglaste Ścieżki", "Siedziba rekieterów", "Chata bandytów", "Błędny Szlak", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór"],
    "Las Dziwów": ["Złowrogie Bagna", "Złowrogie Bagna", "Namiot Kambiona<br>Przejście dostępne do 131 poziomu", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór", "Jaskinia Magów<br>(Wymaga klucza)", "Jezioro Ważek", "Jezioro Ważek", "Liściaste Rozstaje", "Liściaste Rozstaje", "Liściaste Rozstaje"],
    "Złowrogie Bagna": ["Mythar", "Mythar", "Zagrzybiałe Ścieżki p.1 - sala 1", "Błędny Szlak", "Błędny Szlak", "Gadzia Kotlina", "Gadzia Kotlina", "Las Dziwów", "Las Dziwów"],
    "Gadzia Kotlina": ["Wzgórze Płaczek", "Wzgórze Płaczek", "Zagrzybiałe Ścieżki p.1 - sala 2", "Złowrogie Bagna", "Złowrogie Bagna", "Mglista Polana Vesy"],
    "Błędny Szlak": ["Zawiły Bór", "Zawiły Bór", "Zawiły Bór", "Złowrogie Bagna", "Złowrogie Bagna", "Ostępy Szalbierskich Lasów"],
    "Ostępy Szalbierskich Lasów": ["Iglaste Ścieżki", "Siedziba rekieterów", "Chata bandytów", "Błędny Szlak", "Cienisty Bór", "Cienisty Bór", "Cienisty Bór"],
    "Chata bandytów": ["Bandyckie Chowisko", "Ostępy Szalbierskich Lasów", "Chata bandytów p.1"],
    "Chata bandytów p.1": ["Chata bandytów"],
    "Bandyckie Chowisko": ["Bandyckie Chowisko - skarbiec<br>Przejście dostępne od 88 do 114 poziomu", "Chata bandytów"],
    "Siedziba rekieterów": ["Ostępy Szalbierskich Lasów", "Ostępy Szalbierskich Lasów", "Siedziba rekieterów p.1"],
    "Siedziba rekieterów p.1": ["Siedziba rekieterów"],
    "Iglaste Ścieżki": ["Dolina Centaurów", "Dolina Centaurów", "Dolina Centaurów", "Zawiły Bór", "Zawiły Bór", "Zawiły Bór", "Ostępy Szalbierskich Lasów"],
    "Zawiły Bór": ["Selva Oscura", "Selva Oscura", "Selva Oscura", "Solny Szyb p.1", "Mythar", "Mythar", "Mythar", "Zabłocona Jama p.1 - sala 1", "Iglaste Ścieżki", "Iglaste Ścieżki", "Iglaste Ścieżki", "Błędny Szlak", "Błędny Szlak", "Błędny Szlak"],
    "Dolina Centaurów": ["Selva Oscura", "Selva Oscura", "Iglaste Ścieżki", "Iglaste Ścieżki", "Iglaste Ścieżki"],
    "Selva Oscura": ["Przełaz olbrzymów", "Ruiny Wieży Magów - przedsionek", "Dolina Centaurów", "Dolina Centaurów", "Smocze Góry", "Smocze Góry", "Smocze Góry", "Zawiły Bór", "Zawiły Bór", "Zawiły Bór"],
    "Mythar": ["Smocze Góry", "Smocze Góry", "Dom Saprasa", "Zawiły Bór", "Zawiły Bór", "Zawiły Bór", "Dom Walasara", "Izba Pamięci", "Dom Jemenossa", "Dom Felkissiana", "Kuźnia Frassona", "Kuźnia Frassona", "Dom Krassa", "Dom Essy i Frassona", "Dom Węży", "Dom Węży", "Siedziba Ergassaj", "Dom Umplecji i Kiliona", "Dom Trajnaloka", "Dom Lussa", "Dom Angussa", "Dom Lassindy i Limerusa", "Alabastrowy Hotel", "Sala Zgromadzeń", "Dom Liszli i Semkosa", "Dom Presztreka", "Urwisko Zdrewniałych", "Złowrogie Bagna", "Złowrogie Bagna"],
    "Solny Szyb p.1": ["Zawiły Bór", "Solny Szyb p.2"],
    "Solny Szyb p.2": ["Solny Szyb p.1", "Solny Szyb p.3"],
    "Solny Szyb p.3": ["Solny Szyb p.2"],
    "Smocze Góry": ["Przełaz olbrzymów", "Smocza Jaskinia", "Selva Oscura", "Selva Oscura", "Selva Oscura", "Mythar", "Mythar"],
    "Liściaste Rozstaje": ["Las Dziwów", "Las Dziwów", "Las Dziwów", "Sosnowe Odludzie", "Sosnowe Odludzie", "Sosnowe Odludzie", "Jezioro Ważek", "Jezioro Ważek", "Grota Samotnych Dusz p.3 - sala wyjściowa", "Zapomniana Ścieżyna", "Zapomniana Ścieżyna"],
    "Grota Samotnych Dusz p.3 - sala wyjściowa": ["Liściaste Rozstaje", "Grota Samotnych Dusz p.3"],
    "Grota Samotnych Dusz p.3": ["Grota Samotnych Dusz p.3 - sala wyjściowa", "Ślepe Wyrobisko", "Grota Samotnych Dusz p.4", "Grota Samotnych Dusz p.2"],
    "Grota Samotnych Dusz p.4": ["Grota Samotnych Dusz p.3", "Grota Samotnych Dusz p.5"],
    "Grota Samotnych Dusz p.5": ["Grota Samotnych Dusz p.4", "Grota Samotnych Dusz p.6"],
    "Grota Samotnych Dusz p.6": ["Grota Samotnych Dusz p.5", "Opuszczony Szyb", "Opuszczony Szyb"],
    "Opuszczony Szyb": ["Grota Samotnych Dusz p.6", "Mirvenis-Adur"],
    "Mirvenis-Adur": ["Browar Bimberara - warzelnia", "Thorpela zachodnia", "Thorpela zachodnia", "Browar Bimberara - magazyn", "Trakt Moradrana", "Browar Bimberara - garkuchnia", "Szyb transportowy", "Thorpela wschodnia", "Kuźnia Giriela - manufaktura", "Kuźnia Giriela - warsztat", "Opuszczony Szyb<br>Przejście dostępne od 60 poziomu", "Dom Uzdrowień", "Kuźnia Giriela - pracownia", "Dom Jakiego", "Dom Merakliego", "Szlak Thorpa p.6<br>Przejście dostępne od 90 poziomu", "Szlak Thorpa p.6<br>Przejście dostępne od 90 poziomu", "Dom Ypsliego", "Dom Ulryka", "Dom Tozruka", "Kwatery u Morcera", "Gammel Khazad Gravkammer", "Gammel Khazad Gravkammer", "Szyb Zdrajców<br>Przejście dostępne od 60 poziomu", "Dom Reby"],
    "Trakt Moradrana": ["Zasypane Ograbar-dun<br>Przejście dostępne od 60 poziomu", "Chwilowe Schronienie Browarników", "Chwilowe Schronienie Browarników", "Tymczasowa Pracownia Kowali", "Mirvenis-Adur"],
    "Szlak Thorpa p.6": ["Szlak Thorpa p.5", "Mirvenis-Adur", "Mirvenis-Adur"],
    "Grota Samotnych Dusz p.2": ["Grota Samotnych Dusz p.1", "Grota Samotnych Dusz p.3"],
    "Grota Samotnych Dusz p.1": ["Grota Samotnych Dusz p.2", "Trupia Przełęcz"],
    "Trupia Przełęcz": ["Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Kamienna Strażnica - zach. baszta p.2", "Zabłocona Jama p.1 - sala 2", "Namiot kościarza", "Płaskowyż Arpan", "Płaskowyż Arpan", "Grota Samotnych Dusz p.1", "Wzgórze Płaczek", "Wzgórze Płaczek", "Kamienna Strażnica - wsch. baszta p.1", "Księżycowe Wzniesienie", "Księżycowe Wzniesienie"],
    "Wzgórze Płaczek": ["Gadzia Kotlina", "Gadzia Kotlina", "Płacząca Grota p.1 - sala 1", "Trupia Przełęcz", "Trupia Przełęcz", "Płacząca Grota p.1 - sala 2", "Mglista Polana Vesy", "Mglista Polana Vesy"],
    "Księżycowe Wzniesienie": ["Trupia Przełęcz", "Trupia Przełęcz", "Mglista Polana Vesy", "Mglista Polana Vesy", "Zapomniany Święty Gaj p.1", "Sosnowe Odludzie", "Sosnowe Odludzie"],
    "Sosnowe Odludzie": ["Księżycowe Wzniesienie", "Księżycowe Wzniesienie", "Chodniki Mrinding", "Liściaste Rozstaje", "Liściaste Rozstaje", "Liściaste Rozstaje", "Podziemne Rozpadliny"],
    "Tuzmer": ["Ruchome Piaski", "Ruchome Piaski", "Łaźnia damska - szatnia", "Dom Wirkliusza Runaberda", "Dom Wirkliusza Runaberda", "Łaźnia p.1", "Łaźnia męska - szatnia", "Kamienica Bursztynek<br>(Wymaga klucza)", "Dom Mei Shang Lii", "Dom Randala Rotguta", "Dom Rajwosa", "Dom Randala Rotguta", "Dom Rajwosa", "Dom Keftii", "Dom Toramidamusa", "Arena Gladiatorów", "Dom Bernarda", "Dom Toramidamusa", "Arena Gladiatorów", "Dom Bernarda", "Dom dziadka Jeżyka", "Tawerna pod Beczką Śledzi - mieszkanie", "Tawerna pod Beczką Śledzi", "Dom Piwocji", "Dom Piwocji", "Dom Flopka", "Dom Telsara", "Warsztat kowala Kalpusa", "Dom Adanny", "Dom Adanny", "Dom Horsfei", "Dom Horsfei", "Dom Erkora", "Dom Hengadze", "Port Tuzmer", "Port Tuzmer", "Stare Sioło", "Magistrat p.2", "Magistrat", "Port Tuzmer", "Stare Sioło", "Magistrat p.2", "Magistrat", "Port Tuzmer", "Stare Sioło", "Posterunek", "Dom Senekjusza", "Posterunek", "Dom Senekjusza", "Dom Seridiusza", "Dom Krosnego", "Dom Anecji", "Dom Losso Minewita", "Dom Losso Minewita", "Dom Aurusa", "Dom Aurusa", "Dom Mii", "Dom Jallosa", "Dom Klacynii", "Dom Leksosa", "Dom Leksosa", "Kamienica Wernaidy", "Wartownia", "Wartownia p.1", "Wartownia", "Zajazd pod Różą Wiatrów", "Zajazd pod Różą Wiatrów", "Zajazd pod Różą Wiatrów p.1", "Ciche Rumowiska", "Ciche Rumowiska"],
    "Stare Sioło": ["Piachy Zniewolonych", "Dom Namianaszi", "Dom Namianaszi", "Gospodarstwo Balko", "Magazyn rodziny Balko", "Magazyn rodziny Balko", "Siedziba Straży Bramy", "Siedziba Straży Bramy", "Tuzmer", "Tuzmer", "Tuzmer", "Gospodarstwo Erdy", "Gospodarstwo Erdy", "Sucha Dolina", "Sucha Dolina", "Sucha Dolina", "Dom Cynamonii", "Oaza Siedmiu Wichrów", "Oaza Siedmiu Wichrów"],        
    "Piachy Zniewolonych": ["Piaszczysta Grota p.1 - sala 1", "Ruchome Piaski", "Ruchome Piaski", "Piaskowa Gęstwina", "Piaskowa Gęstwina", "Dolina Pustynnych Kręgów", "Dolina Pustynnych Kręgów", "Stare Sioło"],
    "Ruchome Piaski": ["Piachy Zniewolonych", "Piachy Zniewolonych", "Magazyn", "Kuchnia polowa", "Namiot", "Namiot", "Namiot kapitana", "Latarniane Wybrzeże", "Latarniane Wybrzeże", "Tuzmer", "Tuzmer"],
    "Piaskowa Gęstwina": ["Źródło Zakorzenionego Ludu", "Źródło Zakorzenionego Ludu", "Piachy Zniewolonych", "Piachy Zniewolonych", "Dolina Pustynnych Kręgów", "Dolina Pustynnych Kręgów"],
    "Dolina Pustynnych Kręgów": ["Piaskowa Gęstwina", "Piaskowa Gęstwina", "Źródło Zakorzenionego Ludu", "Źródło Zakorzenionego Ludu", "Piachy Zniewolonych", "Piachy Zniewolonych", "Kopalnia Żółtego Kruszcu p.1 - sala 1", "Kopalnia Żółtego Kruszcu p.1 - sala 1", "Altepetl Mahoptekan<br>Przejście dostępne od 200 poziomu", "Altepetl Mahoptekan<br>Przejście dostępne od 200 poziomu", "Siedziba goblinów", "Sucha Dolina", "Sucha Dolina"],
    "Sucha Dolina": ["Dolina Pustynnych Kręgów", "Dolina Pustynnych Kręgów", "Grobowiec Nieznających Spokoju", "Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Stare Sioło", "Stare Sioło", "Stare Sioło", "Płaskowyż Arpan", "Płaskowyż Arpan"],
    "Płaskowyż Arpan": ["Sucha Dolina", "Sucha Dolina", "Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Niecka Xiuh Atl<br>Przejście dostępne od 200 poziomu", "Oaza Siedmiu Wichrów", "Oaza Siedmiu Wichrów", "Oaza Siedmiu Wichrów", "Trupia Przełęcz", "Trupia Przełęcz", "Złote Piaski", "Skalne Cmentarzysko p.1", "Złote Piaski", "Grzęzawisko Rozpaczy<br>Przejście dostępne od 200 poziomu", "Grzęzawisko Rozpaczy<br>Przejście dostępne od 200 poziomu"],
    "Oaza Siedmiu Wichrów": ["Stare Sioło", "Stare Sioło", "Płaskowyż Arpan", "Płaskowyż Arpan", "Płaskowyż Arpan", "Ciche Rumowiska", "Ciche Rumowiska", "Złote Piaski", "Złote Piaski"],
    "Złote Piaski": ["Oaza Siedmiu Wichrów", "Oaza Siedmiu Wichrów", "Ciche Rumowiska", "Ciche Rumowiska", "Płaskowyż Arpan", "Płaskowyż Arpan", "Piramida Pustynnego Władcy p.1", "Dolina Suchych Łez", "Dolina Suchych Łez", "Grzęzawisko Rozpaczy<br>Przejście dostępne od 200 poziomu", "Grzęzawisko Rozpaczy<br>Przejście dostępne od 200 poziomu", "Ruiny Pustynnych Burz", "Ruiny Pustynnych Burz"],
    "Ciche Rumowiska": ["Tuzmer", "Tuzmer", "Oaza Siedmiu Wichrów", "Oaza Siedmiu Wichrów", "Wioska Rybacka", "Wioska Rybacka", "Złote Piaski", "Złote Piaski", "Dolina Suchych Łez", "Dolina Suchych Łez", "Dolina Suchych Łez"],
    "Brama Północy": ["Werbin", "Werbin", "Góry Zrębowe", "Góry Zrębowe", "Góry Zrębowe", "Kuźnia na Rozstajach", "Zapomniana kopalnia p.1", "Włości rodu Kruzo", "Włości rodu Kruzo", "Siedziba główna klanu Uchiha<br>(Wymaga klucza)", "Zaginiona Dolina", "Zaginiona Dolina", "Liściasta kryjówka<br>(Wymaga klucza)", "Liściasta kryjówka<br>(Wymaga klucza)", "Skalista Wyżyna", "Skalista Wyżyna"],
    "Skalista Wyżyna": ["Brama Północy", "Brama Północy", "Ognista Rozpadlina", "Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron"],
    "Przełęcz Dwóch Koron": ["Skalista Wyżyna", "Skalista Wyżyna", "Skalista Wyżyna", "Posterunek", "Posterunek", "Przedmieścia Karka-han", "Przedmieścia Karka-han", "Przedmieścia Karka-han", "Kryształowa Grota p.1", "Domek Pioruna<br>(Wymaga klucza)", "Wichrowe Szczyty", "Wichrowe Szczyty", "Wichrowe Szczyty"],
    "Przedmieścia Karka-han": ["Święty Zagajnik", "Skład Kluspa", "Huta żelaza", "Warsztat miecznika", "Skład surowców", "Przeklęta Pieczara p.1", "Dom Kluspa", "Kopalnia Faluntamir p.1", "Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron", "Lokum krasnoludów", "Dom Torina", "Karka-han", "Karka-han", "Karka-han", "Karka-han", "Szyb Mahnior p.1", "Dom Aberyta", "Namiot leśniczego", "Dom Maryśki", "Mistyczny Bór"],
    "Wichrowe Szczyty": ["Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron", "Przełęcz Dwóch Koron", "Sowia Dziupla", "Podziemne Przejście - sala wyjściowa", "Podziemne Przejście p.6 - sala wyjściowa", "Mistyczny Bór", "Podziemne Przejście p.1", "Mistyczny Bór", "Uroczysko", "Uroczysko", "Uroczysko"],
    "Podgrodzie Nithal": ["Nizina Wieśniaków", "Nizina Wieśniaków", "Nizina Wieśniaków", "Dom Rózi", "Zajazd pod Tęczowym Żukiem", "Zajazd pod Tęczowym Żukiem", "Dom Edny", "Młyn", "Nithal", "Nithal", "Dom Młynarza", "Stajnie<br>(Wymaga klucza)", "Stajnie<br>(Wymaga klucza)", "Źródło Narumi", "Źródło Narumi", "Dom Almonda", "Gospodarstwo Łucji i Jana", "Stodoła", "Stodoła", "Bagna Chojraków", "Drewutnia", "Chlew"],
    "Nizina Wieśniaków": ["Pieczara Czaszek", "Gościniec Bardów", "Gościniec Bardów", "Gościniec Bardów", "Zachodnia Rubież", "Zachodnia Rubież", "Dom Chlasta", "Szopa", "Podgrodzie Nithal", "Podgrodzie Nithal", "Podgrodzie Nithal"],
    "Nithal": ["Mury Nithal - Baszta Koronna", "Kwatera żołnierska", "Akademia wojskowa p.1", "Akademia wojskowa p.1", "Akademia wojskowa - stajnia", "Izba chorych płn.", "Izba chorych płd.", "Akademia wojskowa - stajnia", "Izba chorych płn.", "Izba chorych płd.", "Dom Rezarda", "Kwatera żołnierska", "Kamienica Lukrecji", "Kamienica Tanenbara", "Gildia Kupców - część zachodnia", "Kwatera żołnierska", "Kamienica Zagadek", "Kamienica Furii Infernalis<br>(Wymaga klucza)", "Gildia Kupców - część północna", "Gildia Kupców - część północna", "Kamienica Vilgara<br>(Wymaga klucza)", "Kamienica de Waldenów<br>(Wymaga klucza)", "Gildia Kupców - część wschodnia", "Kamienica Tamena", "Kamienica Prokusi", "Kamienica Krynii Lufis", "Cytadela", "Cytadela", "Kamienica Nitrusa", "Kamienica Cecylii", "Kamienica Pireza", "Kamienica Nandraroka", "Kamienica Broka", "Południowe mury Nithal - część zachodnia", "Kamienica Flawiana", "Podgrodzie Nithal", "Podgrodzie Nithal", "Ratusz Nithal", "Winnica Meflakasti", "Podgrodzie Nithal", "Południowe mury Nithal - część wschodnia", "Zajazd pod Złamanym Dukatem", "Zajazd pod Złamanym Dukatem", "Knajpa pod Czarnym Tulipanem", "Pizzeria", "Knajpa pod Czarnym Tulipanem", "Kamienica Rewii", "Zajazd pod Złamanym Dukatem - pokój właściciela", "Kamienica Eklektusa", "Kamienica Miona", "Kamienica Uliany i Arsena", "Rezydencja Vonikur - kuchnia", "Kamienica Mirutki<br>(Wymaga klucza)", "Opuszczona kamienica<br>(Wymaga klucza)", "Kamienica Kandelia<br>(Wymaga klucza)", "Rezydencja Vonikur", "Kamienica Galeny i Sarda", "Rezydencja Trafalgar", "Kamienica Andronikusa", "Rezydencja Vonikur - biblioteczka", "Rezydencja Trafalgar", "Uniwersytet płn.", "Dormitorium - część akolitów", "Uniwersytet płn.", "Dormitorium - część akolitów", "Uniwersytet płd.", "Świątynia Czterech Bóstw", "Uniwersytet płd.", "Dormitorium - część westalek", "Dormitorium - część westalek"],
    "Karka-han": ["Dom Lenki", "Drukarnia Zenka", "Kamienica Slina", "Dom Remiusza", "Dom Johana", "Dom Zeiny", "Dom Azalii", "Dom Nufrexa", "Dom Kalicji i Apoksa", "Dom Befry", "Dom Befry", "Magazyn", "Dom rzeźnika", "Magazyn", "Dom Aurelii i Dionizego", "Kamienica Kleofasa", "Tawerna pod Kocim Wąsem", "Prastara Puszcza", "Prastara Puszcza", "Dom Hergata i Halfinii", "Dom Hergata i Halfinii", "Rozładownia", "Kamienica Newalda", "Rozładownia", "Dom Anulisa", "Karmazynowa siedziba", "Ratusz Karka-han", "Ratusz Karka-han", "Lochy miejskie<br>(Wymaga klucza)", "Dom Roszana", "Przedmieścia Karka-han", "Przedmieścia Karka-han", "Przedmieścia Karka-han", "Przedmieścia Karka-han", "Karczma pod Złotą Wywerną", "Dom Menarika<br>(Wymaga klucza)", "Gildia Kupców", "Miejska biblioteka", "Dom Inetora", "Dom Konstantego i Forsycji", "Dom Konstantego i Forsycji", "Dom płatnerza", "Dom Anzelma", "Pracownia Inetora", "Pracownia płatnerza", "Pracownia płatnerza", "Lecznica dla zwierząt", "Dom Kaliposa", "Nekropolia Karka-han", "Nekropolia Karka-han", "Nekropolia Karka-han"],   

    "Dziewicza Knieja": ["Orla Grań", "Orla Grań", "Siedlisko Nietoperzy p.5", "Stare Ruiny", "Stare Ruiny", "Siedlisko Nietoperzy p.1", "Grota Malowanej Śmierci", "Las Tropicieli", "Las Tropicieli"],
    "Siedlisko Nietoperzy p.1": ["Dziewicza Knieja", "Siedlisko Nietoperzy p.2"],
    "Siedlisko Nietoperzy p.2": ["Siedlisko Nietoperzy p.1", "Siedlisko Nietoperzy p.3 - sala 1"],
    "Siedlisko Nietoperzy p.3 - sala 1": ["Siedlisko Nietoperzy p.4", "Siedlisko Nietoperzy p.2", "Siedlisko Nietoperzy p.3 - sala 2"],
    "Siedlisko Nietoperzy p.3 - sala 1": ["Siedlisko Nietoperzy p.4", "Siedlisko Nietoperzy p.2", "Siedlisko Nietoperzy p.3 - sala 2"],
    "Siedlisko Nietoperzy p.3 - sala 2": ["Siedlisko Nietoperzy p.3 - sala 1"],
    "Siedlisko Nietoperzy p.4": ["Siedlisko Nietoperzy p.5", "Siedlisko Nietoperzy p.3 - sala 1"],
    "Siedlisko Nietoperzy p.5": ["Dziewicza Knieja", "Siedlisko Nietoperzy p.4"],
    "Las Tropicieli": ["Dziewicza Knieja", "Dziewicza Knieja", "Osada Mulusów"],
    "Przeklęta Strażnica": ["Przeklęta Strażnica - podziemia p.1 s.1", "Przeklęta Strażnica p.1", "Orla Grań", "Przeklęta Strażnica p.1", "Orla Grań", "Przeklęta Strażnica - podziemia p.1 s.2"],
    "Przeklęta Strażnica - podziemia p.1 s.1": ["Przeklęta Strażnica", "Przeklęta Strażnica - podziemia p.2 s.1<br>Przejście dostępne do 43 poziomu"],
    "Przeklęta Strażnica p.1": ["Przeklęta Strażnica", "Przeklęta Strażnica", "Przeklęta Strażnica p.2"],
    "Przeklęta Strażnica p.2": ["Orla Grań", "Przeklęta Strażnica p.1", "Przeklęta Strażnica p.1"],
    "Przeklęta Strażnica - podziemia p.1 s.2": ["Przeklęta Strażnica", "Przeklęta Strażnica - podziemia p.2 s.2"],
    "Przeklęta Strażnica - podziemia p.2 s.2": ["Przeklęta Strażnica - podziemia p.1 s.2", "Przeklęta Strażnica - podziemia p.2 s.3<br>Przejście dostępne do 43 poziomu", "Przeklęta Strażnica - podziemia p.2 s.3<br>Przejście dostępne do 43 poziomu"],

}

def find_path(start: str, map_graph, cities: set[str], destination: Optional[str] = None) -> list[str] | None:
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)

        if (destination and current == destination) or (not destination and current in cities and current != start):
            print(f"[Ścieżka] Znaleziona ścieżka: {path[1:]}")
            return path[1:]

        for neighbor in map_graph.get(current, []):
            if neighbor not in visited:
                queue.append(path + [neighbor])

    print("[Ścieżka] Nie znaleziono ścieżki.")
    return None



def find_closest_city(start: str, map_graph, cities) -> list[str] | None:

    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)

        if current in cities and current != start:
            print(f"[Ścieżka] Najkrótsza ścieżka do najbliższego miasta: {path[1:]}")
            return path[1:]

        for neighbor in map_graph.get(current, []):
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    print("[Ścieżka] Nie znaleziono drogi do żadnego miasta.")
    return None

#find_closest_city("Skalista Wyżyna", map_graph, cities)

#find_path("Tuzmer", map_graph, cities, "Nithal")