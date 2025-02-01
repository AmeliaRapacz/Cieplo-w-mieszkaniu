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

3.`diff_matrix(N, M)`
Funkcja łączy dwie macierze jedną dla osi X (o rozmiarze N) i drugą dla osi Y (o rozmiarze M). Tworzy macierz, która jest używana do obliczeń w dwóch wymiarach

---

FOLDER szkice

tam mam szkice mieszkań, które wykorzystuję w projekcie: 
szkic mieszkania 1: szkic z losowymi usatwionymi oknami i kaloryferami(wykorzystany przy prezentacji ideii projektu i w 2 problemie badawczym)
szkic mieszkania 2: grzejniki usatwione bezpośrednio przed oknami (wykorzystany w 1 problemie badawczym)
szkic mieszkania 3: grzejniki usatwione bezpośrednio blisko okien (wykorzystany w 1 problemie badawczym)
szkic mieszkania 4: grzejniki usatwione bezpośrednio daleko od oknien (wykorzystany w 1 problemie badawczym)
