import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def szkic_mieszkania(kolumny, wiersze):
    macierz = np.zeros((wiersze, kolumny))

    lokalizacja_scian = [
        (0, i) for i in range(kolumny)] + [
        (8, i) for i in range(kolumny)] + [
        (9, i) for i in range(kolumny)] + [
        (19, i) for i in range(kolumny)] + [
        (i, 0) for i in range(wiersze)] + [
        (i, 20) for i in range(0, 9)] + [
        (i, 21) for i in range(0, 9)] + [
        (i, 12) for i in range(8, 19)] + [
        (i, 13) for i in range(8, 19)] + [
        (i, 31) for i in range(wiersze)]
    
    for x, y in lokalizacja_scian:
        if 0 <= x < wiersze and 0 <= y < kolumny:
            macierz[x, y] = 1

    lokalizacja_okien = [
        (0,i) for i in range(13,15)] + [
        (0,i) for i in range(2,4)] + [
        (19,i) for i in range(4,6)] + [
        (19,i) for i in range(20,22)] + [
        (i,0) for  i in range (13,15)] + [
        (i, 31) for i in range(4,6)] + [
        (i, 31) for i in range(14,16)
        ]

    for x, y in lokalizacja_okien:
        if 0 <= x < wiersze and 0 <= y < kolumny:
            macierz[x, y] = 2

    lokalizacja_kaloryfery = [
        (1,i) for i in range(4,6)] + [
        (1,i) for i in range(15,17)] + [
        (18,i) for i in range(6,8)] + [
        (18,i) for i in range(22,24)] + [
        (i,1) for  i in range (11,13)] + [
        (i,14) for  i in range (13,15)] + [
        (i, 30) for i in range(2,4)] + [
        (i, 30) for i in range(12,14)] + [
        ]

    for x, y in lokalizacja_kaloryfery:
        if 0 <= x < wiersze and 0 <= y < kolumny:
            macierz[x, y] = 3
    
    lokalizacja_drzwi_pokoje = [
        (9,i) for i in range(3,5)] + [
        (9,i) for i in range(16,18)] + [
        (i, 21) for i in range(4,6)] + [
        ]

    for x, y in lokalizacja_drzwi_pokoje:
        if 0 <= x < wiersze and 0 <= y < kolumny:
            macierz[x, y] = 4

    lokalizacja_drzwi_korytarz = [
        (8,i) for i in range(3,5)] + [
        (8,i) for i in range(16,18)] + [
        (i, 20) for i in range(4,6)] + [
        ]

    for x, y in lokalizacja_drzwi_korytarz:
        if 0 <= x < wiersze and 0 <= y < kolumny:
            macierz[x, y] = 5

    return macierz

szkic = szkic_mieszkania(32, 20)
colors = {0: "white", 1: "black", 2: "royalblue", 3: "indianred", 4:"yellow", 5:"orange"}

# Dodanie legendy dla kolorów
legend_labels = {
    "Ściany": "black",
    "Okna": "royalblue",
    "Kaloryfery": "indianred",
    "Drzwi do pokoi": "yellow",
    "Drzwi do korytarza": "orange"
}


patches = [mpatches.Patch(color=color, label=label) for label, color in legend_labels.items()]
fig, ax = plt.subplots()
for (i, j), val in np.ndenumerate(szkic):
    ax.add_patch(plt.Rectangle((j, -i), 1, 1, color=colors[val]))

ax.set_xticks(np.arange(0, szkic.shape[1], 1), minor=False)
ax.set_yticks(np.arange(1 - szkic.shape[0], 1, 1), minor=False)
ax.grid(visible=True, which='both', color='darkgrey', linestyle='-', linewidth=1)
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

ax.set_xlim(0, szkic.shape[1])
ax.set_ylim(1 - szkic.shape[0], 1)
ax.set_title('Szkic mieszkania')
ax.set_aspect('equal')

plt.legend(handles=patches, loc='upper left', bbox_to_anchor=(1.05, 1), title="Legenda")

plt.show()
plt.savefig(f"szkic_mieszkania_z_legenda_poza.png", bbox_inches="tight")  # bbox_inches="tight" pozwala uniknąć obcięcia legendy
plt.close()
