import numpy as np
import matplotlib.pyplot as plt


def draw_bishops(board):
    """Affiche un plateau et les fous qui s'y trouvent."""
    size = board.shape[0]
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    for row in range(size):
        for col in range(size):
            square = plt.Rectangle(
                (col, size - 1 - row), 1, 1,
                facecolor="white" if (row + col) % 2 == 0 else "gray"
            )
            ax.add_patch(square)

            if board[row, col] == 1:
                ax.text(col + 0.5, size - row - 0.5, "♗",
                        ha="center", va="center", fontsize=24)

    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.axis("off")
    plt.show()


# 1. Place 6 fous au hasard sur un plateau 4x4.
def random_six_bishops():
    # Crée une matrice 4 x 4 remplie de zéros : 0 signifie « case vide ».
    # Un tableau NumPy est utilisé car il permet de représenter simplement
    # le plateau et de modifier plusieurs cases efficacement.
    board = np.zeros((4, 4), dtype=int)

    # Génère une permutation aléatoire des indices 0 à 15. Ces indices
    # représentent les 16 cases quand la matrice est aplatie. La permutation
    # évite de choisir deux fois la même case ; les six premiers indices
    # donnent donc six cases distinctes.
    positions = np.random.permutation(16)[:6]

    # ravel() ne crée pas une nouvelle liste : il donne une vue de la matrice
    # sous forme d'une seule suite de 16 cases. Modifier cette vue modifie donc
    # directement board. On place 1 dans les six positions sélectionnées pour
    # représenter les six fous, sans créer de doublon sur une même case.
    board.ravel()[positions] = 1
    return board


# 2. Vérifie si aucun fou n'en attaque un autre.
def bishops_are_safe(board):
    # np.where renvoie les coordonnées (ligne, colonne) de chaque case
    # contenant un fou. Les coordonnées servent ensuite à tester les diagonales.
    rows, cols = np.where(board == 1)

    # Sur une diagonale, la différence ligne - colonne est constante.
    # Si deux fous ont la même différence, ils partagent donc une diagonale.
    # set supprime les doublons ; sa taille doit rester égale au nombre de fous.
    #
    # Sur l'autre direction diagonale, la somme ligne + colonne est constante.
    # Même raisonnement : une somme répétée signifie que deux fous s'attaquent.
    # Le ET logique impose que les deux familles de diagonales soient libres.
    return (len(set(rows - cols)) == len(rows) and
            len(set(rows + cols)) == len(rows))


# 3. Cherche une solution en recommençant au hasard.
def six_bishops():
    attempts = 0

    while True:
        attempts += 1
        board = random_six_bishops()

        if bishops_are_safe(board):
            return board, attempts


if __name__ == "__main__":

    board, attempts = six_bishops()
    print(f"Solution trouvée en {attempts} essais :")
    print(board)
    draw_bishops(board)

    print(f"Nombre total d'essais : {attempts}")




def random_6_bishups():
    board = np.zeros((4,4), dtype=int)
    posi= np.random.permutation(16)[:6]
    board.ravel()[posi] =1
    return board

def bishops_are_safe(board):
    row, col = np.where(board ==1)
    return (len(set(row-col))==len(row) and len(set(row+col))==len(row))

def six_bishops():
    attemps =0

    while True:
        attemps +=1
        board = random_6_bishups()

        if bishops_are_safe(board):
            return board, attemps


    