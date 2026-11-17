import argparse
import random
import sys

PARED = "#"
LIBRE = "."
INICIO = "S"
FIN = "E"
VISITADA = "v"
CAMINO = "*"

def crear_fila(m, prob_pared):
    if m == 0:
        return []
    celda = PARED if random.random() < prob_pared else LIBRE
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
    if lab[f][c] != LIBRE:
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
    lab[0][0] = INICIO
    lab [n - 1][m - 1] = FIN
    colocar_portales(lab, 3)
    return lab

def solucion(lab, f, c, pila, limite):
    if f < 0 or c < 0 or f >= len(lab) or c >= len(lab[0]):
        return None
    celda = lab[f][c]
    if celda == PARED or celda == VISITADA:
        return None
    if len(pila) + 1 >= limite:
        return None
    if celda == FIN:
        return pila + [(f, c)]

    lab[f][c] = VISITADA
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

    intento = solucion(lab, f, c + 1, pila, limite)  # derecha
    if intento is not None:
        mejor, limite = intento, len(intento)
        
    if isinstance(celda, tuple):
        intento = solucion(lab, f + celda[1], c + celda[2], pila, limite)
        if intento is not None:
            mejor, limite = intento, len(intento)

    pila.pop()
    lab[f][c] = celda
    return mejor

def trazar_camino(lab, camino):
    if not camino:
        return
    f, c = camino[0]
    if lab[f][c] == LIBRE:
        lab[f][c] = CAMINO
    trazar_camino(lab,camino[1:])

def simbolo(celda):
    return "P" if isinstance(celda, tuple) else celda

def fila_a_texto(fila):
    if not fila:
        return ""
    return simbolo(fila[0]) + " " + fila_a_texto(fila[1:])

def imprimir(lab):
    if not lab:
        return 
    print(fila_a_texto(lab[0]))
    imprimir(lab[1:])

def main():
    parser = argparse.ArgumentParser(description="Laberinto con portales")
    parser.add_argument("n", type=int, nargs="?", default=8, help="filas")
    parser.add_argument("m", type=int, nargs="?", default=8, help="columnas")
    parser.add_argument("seed", type=int, nargs="?", default=7)
    args = parser.parse_args()
    if args.n < 4 or args.m < 4:
        sys.exit ("el laberinto debe ser de almenos de 4x4 xd")

    sys.setrecursionlimit(10000)
    lab = generar_laberinto(args.n, args.m, args.seed)

    print("\nLaberinto (I = inicio, F = fin, # = pared, P = portal):")
    imprimir(lab)

    camino = solucion(lab, 0, 0, [], args.n * args.m + 1)
    if camino is None:
        print("\nNo hay camino para esta semilla xd, intenta con otra")
        return

    print(f"\nCamino mas corto: {len(camino) - 1} pasos")
    trazar_camino(lab, camino)
    imprimir(lab)
    print("\nRecorrido:", camino)

if __name__ == "__main__":
    main()