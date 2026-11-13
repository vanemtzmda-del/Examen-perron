import argparse
import random
import sys

pared = "#"
libre = "."
inicio = "S"
fin = "E"
visitada = "v"
camino = "*"

def crear_fila(m, prob_pared):
    if m == 0:
        return []
    celda = pared if random.random() < prob_pared else libre
    return [celda] + crear_fila(m - 1, prob_pared)

def crear_matriz(n, m, prob_pared):
    if n == 0:
        return []
    return [crear_fila(m, prob_pared)] + crear_matriz(n - 1, m, prob_pared)

def colocar_portales(lab, k):
    if k == 0:
        return 
    f = random.randrange(len(lab))
    c = random.randrange(len(lab[0]))
    if lab[f][c] != libre:
        colocar_portales(lab, k)
        return
    destino_f = random.randrange(len(lab))
    destino_c = random.randrange(len(lab[0]))
    lab[f][c] = ("P", destino_f - f, destino_c - c)
    print (f"Portal en ({f}, {c}) -> ({destino_f}, {destino_c})")
    colocar_portales(lab, k - 1)

def generar_laberinto(n, m, seed, prob_pared=0.25):
    random.seed(seed)
    lab = crear_matriz(n, m, prob_pared)
    lab[0][0] = inicio
    lab [n - 1][m - 1] = fin
    colocar_portales(lab, 3)
    return lab

def solucion(lab, f, c, pila, limite):
    if f < 0 or c < 0 or f >= len(lab) or c >= len(lab[0]):
        return None
    celda = lab[f][c]
    if celda == pared or celda == visitada:
        return None
    if len(pila) + 1 >= limite:
        return None
    if celda == fin:
        return pila + [(f, c)]

    lab[f][c] = visitada
    pila.append((f, c))

    mejor = None

    intento = solucion(lab, f - 1, c, pila, limite)
    if intento is not None:
        mejor, limite = intento, len (intento)

    intento = solucion(lab, f + 1, c, pila, limite)
    if intento is not None:
        mejor, limite = intento, len (intento)

    intento = solucion(lab, f, c - 1, pila, limite)
    if intento is not None:
        mejor, limite = intento, len (intento)

    intento = solucion(lab, f, c + 1, pila, limite)
        if intento is not None:
            mejor, limite = intento, len (intento)
