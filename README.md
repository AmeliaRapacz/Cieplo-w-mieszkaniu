# Dokumentacja projektu

## requirements.txt
Korzytam jedynie z podstawowych bibliotek Pythona: `numpy` i `matplotlib`, dlatego zdecydowałam się nie przygotowywać pliku typu requirements

---

## Plik dane.py

1. Wczytuję pliki CSV z temperaturami, które są rozpisane co do godziny, z jednego z portali meteorologicznych (więcej informacji znajduje się w PDF z raportem), i zamieniam temperaturę na Kelwiny, a także wczytuję plik JSON ze stałymi fizycznymi, które znalazłam w internecie (szczegóły w PDF).
2. Dyskretyzacja dziedziny: ustawiam krok $h_t = 0.5$ oraz $h_x = 0.5$ (wyjaśnienie w PDF z raportem). Dlatego, gdy rozwiązuję równanie ciepła przez całą dobę, potrzebuję rozpiski co do każdej pół-sekundy, co realizuję za pomocą funkcji `iteration_temperature`.

---

## Plik funkcje.py

1. **`f(P, ro, Ri, cw)`**  
   - `P`: moc grzejnika  
   - `ro`: gęstość powietrza  
   - `Ri`: obszar umiejscowienia grzejnika  
   - `cw`: pojemność cieplna  

2. **`matrix(n)`**  
   Funkcja tworzy macierz o wymiarach \(n \times n\), w której na przekątnej są wartości -2, a obok przekątnej 1.

3. **`diff_matrix(N, M)`**  
   Funkcja łączy dwie macierze: jedną dla osi X (o rozmiarze N) i drugą dla osi Y (o rozmiarze M). Tworzy macierz, która jest używana do obliczeń w dwóch wymiarach.

---

## FOLDER szkice

Szkice mieszkań, które wykorzystuję w projekcie:

1. **Szkic mieszkania 1**: szkic z losowo ustawionymi oknami i kaloryferami (wykorzystany przy prezentacji idei projektu oraz w 2. problemie badawczym)
2. **Szkic mieszkania 2**: grzejniki ustawione bezpośrednio przed oknami (wykorzystany w 1. problemie badawczym)
3. **Szkic mieszkania 3**: grzejniki ustawione bezpośrednio blisko okien (wykorzystany w 1. problemie badawczym)
4. **Szkic mieszkania 4**: grzejniki ustawione bezpośrednio daleko od okien (wykorzystany w 1. problemie badawczym)

Opis działania kodu uznaję za mało istotny – jest to bardziej baza, która pomaga w odnalezieniu się w indeksach podczas późniejszych etapów przygotowywania symulacji.

---

## PLIK elementy_mieszkania.py

1. W tym pliku definiujemy *klasy poszczególnych elementów mieszkania*: pojedynczy pokój, drzwi, okna, grzejniki.
2. **Klasa Room**: Tutaj definiuję każdy z pokoi. Każdy pokój ma różne wymiary (każdy pokój jest prostokątem) oraz temperaturę początkową (ustawiam ją na temperaturę panującą na zewnątrz). W tej klasie definiuję również brzegi, czyli ściany, na które nałożony jest warunek brzegowy Neumanna, a także sąsiadów brzegów. Ściany wyznaczam w formie listy. Funkcja `step` pozwala obliczyć wartości rozwiązania w czasie $t$ na podstawie poprzedniego kroku $t-1$, uwzględniając krok $h_t$ i $h_x$. Następnie aktualizujemy wartości na brzegach, przypisując im odpowiednie wartości sąsiadów tych brzegów.
3. **Klasa Window**: W zależności od pokoju, w którym znajduje się okno, wyznaczam jego współrzędne, czyli numer indeksu, jakbyśmy ponumerowali cały pokój od 0 do $N \times M$. Okna mają przypisaną temperaturę, która zmienia się w czasie, dlatego używam funkcji `outside_temperature`.
4. **Klasa Heater**: Podobnie jak w przypadku okien, grzejniki są przypisane do konkretnego pokoju i mają określoną lokalizację w tym pokoju. Grzejniki grzeją do momentu, aż temperatura w ich otoczeniu osiągnie temperaturę ustawioną na termostacie. Oprócz lokalizacji grzejnika musimy również określić lokalizację punktów, które znajdują się w pobliżu grzejnika (ale nie obejmują ścian). Klasa zawiera również możliwość ustawienia termostatu, który pozwala na wybór temperatury. Termostaty mają kilka ustawień, a szczegóły dotyczące tych ustawień znajdują się w pliku PDF z projektem. Maksymalna temperatura grzejnika zależy od ustawienia termostatu. Jako domyślną wartość przyjmuję ustawienie na 24°C, które zostało przyjęte w kontekście problemu badawczego nr 1. Dodatkowo w klasie wykorzystuję funkcję `f`, odpowiedzialną za obliczanie zużycia energii, która została opisana zarówno w raporcie, jak i w pliku funkcje.py.
5. **Klasa Door**: Drzwi łączą dwa pokoje, a ciepło przechodzi przez drzwi. W każdym kroku czasowym bierzemy temperatury z pokoi, które te drzwi łączą, i uśredniamy je. Taką uśrednioną temperaturę nakładamy na drzwi.

---

## PLIK mieszkanie.py

**UWAGA**: Nadanie grzejnikom lokalizacji to czynność, którą wykonuję ręcznie. Dlatego, aby nie pogubić się podczas symulacji, stworzyłam dla każdej z symulacji osobny plik typu `mieszkanie.py`. Zasada działania jest niemal identyczna. Różnią się między sobą: lokalizacją grzejników i pól otaczających grzejniki, lokalizacją okien, a dla symulacji dotyczącej 2. problemu badawczego wprowadziłam zmiany w funkcji `main()`.

1. **Klasa House** reprezentuje cały dom, który składa się z kilku pokoi, okien, grzejników i drzwi. Elementy te implementuję z pliku `elementy_mieszkania.py`. W tej klasie odbywa się symulacja temperatury w domu w czasie, uwzględniając początkową temperaturę, temperaturę zewnętrzną oraz działanie grzejników i okien.
2. **`create_house_matrix(t)`**: Tworzy macierz przedstawiającą temperatury w całym domu w czasie $t$.
3. W każdym kroku czasowym temperatura w pokojach jest aktualizowana, grzejniki podgrzewają pokoje, a okna uwzględniają temperaturę zewnętrzną. Na koniec generowane są wykresy pokazujące zmiany temperatury w domu oraz zużycie energii przez grzejniki. Przy generowaniu wykresów dobieram czasy, w których chciałabym otrzymać odpowiednią mapę ciepła. Początkowo generowałam animację, aby zobaczyć, jak zmienia się temperatura w ciągu doby, a później wybrałam najbardziej reprezentatywne momenty do raportu.

---

## Symulacje

Symulacje są powiązane z odpowiadającymi im plikami `mieszkanie.py`. Jak pisałam w mailu, nie do końca wiem, jak połączyć wszystkie symulacje w jeden plik `run_experiments.py`, ale otwarcie 6 plików typu `symulacja.py` gwarantuje generowanie wszystkich wykresów zawartych w raporcie.

---

## Uwagi

1. Przyznaję się, że dużą część pracy (zwłaszcza pomoc na początkowym etapie pisania kodu) wykonałam po konsultacji z kolegą Adrianem, którego pomoc przy projekcie była nieoceniona. Stąd możliwe, że będą podobieństwa w zasadzie funkcjonowania kodu. Pomoc ta nie polegała na przekopiowywaniu pracy innego studenta, lecz na udzieleniu trafnych wskazówek, dzięki którym samodzielnie wykonałam projekt i jestem świadoma każdej linijki tego kodu.
2. Przyznaję się, że część pracy przy generowaniu wykresów zawdzięczam sztucznej inteligencji, która pięknie zastosowała się do moich wskazówek, by poprawić estetykę generowanych obrazków, zwłaszcza wyświetlanie na `cbar` zarówno temperatury w stopniach Celsjusza, jak i Kelwinach (i potencjalnie jest to jedyna rzecz, której z biegu bym nie odtworzyła).
3. Przyznaję się, że projekt zajął mi koszmarnie dużo czasu i nieraz wywołał łzy w oczach, ale ostatecznie przyniósł dużo satysfakcji. Gdyby nie ograniczenia czasowe, chętnie udoskonaliłabym kod, aby nie tworzyć za każdym razem pliku `mieszkanie.py` i sprawdziłabym kilka innych problemów badawczych (pomysły znajdują się w podsumowaniu PDF z projektem).
4. Przeprszam za rozległość tesktu readme i za długość raportu, dopiero przy ostecznej kontroli zauważyłam punkt, żeby raport był zwięzły. 
