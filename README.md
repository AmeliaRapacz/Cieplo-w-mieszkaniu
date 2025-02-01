requirements.txt – Korzystam jedynie z podstawowych bibliotek Pythona: numpy i matplotlib, dlatego zdecydowałam się nie przygotowywać tego pliku

---
Plik dane.py

1. Wczytuję pliki csv z tempaturami rozpisanymi co do godziny z jedno z poratli meteorologicznych(więcej w pdf z osstecznym raportem) i zaminiema temperaturę na Kelwiny
   oraz plik json ze stałymi fizycznymi, które znazłam w interncie (również więcej w pdf)
2. Dyskretyzacja dziedziny: ustwaim krok $h_t=0.5$ i $h_x=0.5$ (wyjaśnienie w pdf z raportem), dlatego jeśli rozwiązuję równanie ciepła w okresie całej doby to potzrebuje rozpiski, co do kazdej pół-sekundy,
   co robię za pomocą funkcji iteration_temperature
   
---

Plik funkcje.py

1. `f(P, ro, Ri, cw)`
P - moc gzrejnika
ro- gęstość powietrza
Ri - obszar umiejscowienia gzrejnika
cw - pojemność cieplna 

2. `matrix(n)`
Funkcja tworzy macierz o wymiarach $n \times n$, w której na przekątnej są wartości -2, a obok przekątnej 1. 

3. `diff_matrix(N, M)`
Funkcja łączy dwie macierze jedną dla osi X (o rozmiarze N) i drugą dla osi Y (o rozmiarze M). Tworzy macierz, która jest używana do obliczeń w dwóch wymiarach

---

FOLDER szkice

Szkice mieszkań, które wykorzystuję w projekcie: 

1. szkic mieszkania 1: szkic z losowymi usatwionymi oknami i kaloryferami(wykorzystany przy prezentacji ideii projektu i w 2 problemie badawczym)
2. szkic mieszkania 2: grzejniki usatwione bezpośrednio przed oknami (wykorzystany w 1 problemie badawczym)
3. szkic mieszkania 3: grzejniki usatwione bezpośrednio blisko okien (wykorzystany w 1 problemie badawczym)
4. szkic mieszkania 4: grzejniki usatwione bezpośrednio daleko od oknien (wykorzystany w 1 problemie badawczym)

opis działania kodu, uznaję tutaj za mało istotny, jest to bardziej baza konieczna do odnaleznia się w indeksach w późniejszych etapach przygotowywania symulacji

---

PLIK elementy_mieszkania.py

1. W tym pliku definiujemy *klasy poszczególnych elemntów mieszkania*: pojedynczy pokój, drzwi, okna, grzejniki
2. **Klasa Room**: tutaj będę definiowała każdy z pokoi, każdy pokój będzie miał różne wymiary(każdy pokój jest prostokątem), nakładała temepraturę początkową(ja nakładam jako temperaturę początkową temperaturę panującą na zewnątrz), w tej klasie definije brzegi czyli ściany, na kóre jest nałożony warunek brzegowy Neumanna, zatem definiuje też sąsiadów brzegów. Wyznaczam w formie listy ściany. Funkcja `def step` pozwala obliczyć wartości rozwiązania w czasie t na podstawie poprzedniego kroku t-1, z uwzględniem korku $h_t$ i $h_x$. Następnie aktualizyjemy wartości na brzegach przypisując im odpowiednie wartości sąsiadów tych brzegów
3. **Klasa Window**: tutaj w zależności od pokoju, w którym znajduje się okno będę wyznaczała jego wspórzedne, czyli numer indeksu, jakbyśmy ponumerali nasz cały pokój od 0 do $N*M$, okna będą miały przypisaną temepraturę, któa w danej chwili panuje na zewnątrz (ta temeratura zmeinia się w czasie) stąd pojawia się użycie funcji `outside_temperature`
4. **Klasa Heater**:  Podobnie jak w przypadku okien, grzejniki są przypisane do konkretnego pokoju i mają określoną lokalizację w tym pokoju. Zasada działania grzejników polega na tym, że będą one grzały do momentu, aż temperatura w ich otoczeniu osiągnie temperaturę ustawioną na termostacie. Oprócz lokalizacji grzejnika, musimy również określić lokalizację punktów, które znajdują się w pobliżu grzejnika (ale nie obejmują ścian). Klasa zawiera również możliwość ustawienia termostatu, który pozwala na wybór temperatury. Termostaty mają kilka ustawień, a szczegóły dotyczące tych ustawień znajdują się w pliku PDF z projektem. Maksymalna temperatura grzejnika zależy od ustawienia termostatu. Jako domyślną wartość przyjmuję ustawienie na 24°C, które zostało przyjęte w kontekście problemu badawczego nr 1. Dodatkowo, w klasie wykorzystuję funkcję f, odpowiedzialną za obliczanie zużycia energii, która została opisana zarówno w raporcie, jak i w pliku funkcje.py.
5. **Klasa Door**: drzwi łączą dwa pokoje i oczekujamy, że w jakiś sposób ciepło będzie przechidziło przez drzwi. Dlatefo w każdym kroku czasowym, będziemy brali temperaturę z poki, które te drzwi łączą i uśredniali te temaparatury, a następnie taką uśrednioną temperaturę nakładamy na drzwi.

---

PLIK mieszkanie.py

**UWAGA**: Nadanie grzejnikom lokalizacji, to rzecz, którą wpisuję ręcznie dlatego, żeby nie pogubić się dla każdej symulacji,\ stworzyłam osobny plik typu mieszkanie.py, zasada działa jest niemal identyczna. Różnią się między sobą: lokalizacją gzrejników i pól otaczających grzejniki, lokalizacją okien, dla symulacji dotyczącej 2 problemu badawczego pojawią zmiany w funkcji main()

1. **Klasa House** reprezentuje cały dom, który składa się z kilku pokoi, okien, grzejników i drzwi. Elemnty te implemnyuję z pliku elementy_mieszkania.py W tej klasie odbywa się symulacja temperatury w domu w czasie, przy uwzględnieniu początkowej temperatury, temperatury zewnętrznej oraz działania grzejników i okien.
2. `create_house_matrix(t)`: Tworzy macierz przedstawiającą temperatury w całym domu w czasie t.
3. W każdym kroku czasowym, temperatura w pokojach jest aktualizowana, grzejniki podgrzewają pokoje, a okna uwzględniają temperaturę zewnętrzną. Na koniec generowane są wykresy pokazujące zmiany temperatury w domu oraz zużycie energii przez grzejniki. Tutaj przy wywoływaniu wykresów, dobierałam sobie dla jakich czasów chciałabym otrzymać odpowiednią mapę ciepła. Na początku generowałam sobie animację, żeby zwrócić uwagę jak w ciagu doby zmienia się temperatura w mieszkaniu, by później wybrać najabrdziej repreznetywne momenty do raportu.

---

Symulacje: podzieliłam symualcje z odpiawdającymi im plikami mieszkanie.py na osobne foldery 

---

Uwagi

1. Przyznaję się, że dużą część pracy (zwłaszcza pomoc na początkowym etapie pisnia kodu) wykonałam po konsulatcji z kolegą Adrianem, którego pomoc przy projekcie była niestąpiona, stąd możliwe, że będą podobieństwa w zasadzie funkcjonowania kodu. Pomoc ta nie była przekopiowaniem pracy innego studenta, a jedynie kierowaniem się trafnymi wskazówki, dzięki którym samodzielnie wykonałam projekt i jestem świadoma każdej linijki tego kodu.
2. Przyznaję się, że część pracy przy generowniu wykresów zawdzięczam sztucznej inteligencji, która potrafiła pięknie zastosować się do moich wsakzówek, by polepszyć estetykę generownych obrazków, zwłszcza wyświetlanie na `cbar` zarówno temperatury w stopniach Celcjusza jak i Kelwinach (i potencjalnie jest to jedyna rzecz, której z biegu bym nie odtworzyła)
3. Przyznaję się, że projekt zajął mi koszmarnie dużo czasu i nieraz wywoł łzy w moich oczach, ale ostetcznie przyniósł dużo satysfakcji. Gdyby nie ogranicznie czasowe, chętnie udoskonaliłabym kod, żeby nie twozryc za kazdym razem pliku mieszkanie.py i sparwdziałbym kilka innych problemów badawczych (pomysły w podsumownaiu pdf z projektem)
