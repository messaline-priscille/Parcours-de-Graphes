import customtkinter as ctk

#       PARCOURS EN PROFONDEUR (DFS)
# Variables globales
Marque = []
pi = []
Deb = []
Fin = []
Parcours = []
tps = 0
Pile = []
File = []


# 1. VERIFICATION DE LA MATRICE
def verifier_matrice(M, n, oriente):

    if len(M) != n:
        return False

    for ligne in M:

        if len(ligne) != n:
            return False

        for valeur in ligne:
            if valeur not in (0, 1):
                return False

    # Un graphe non orienté doit avoir une matrice symétrique
    if not oriente:
        for i in range(n):
            for j in range(i + 1, n):

                if M[i][j] != M[j][i]:
                    return False

    return True

def construire_adjacence(M):
    return [
        [j for j, valeur in enumerate(ligne) if valeur == 1]
        for ligne in M
    ]


# 2. FONCTION MARQUER
def Marquer(s):
    global tps
    if Marque[s] == 0:
        Marque[s] = 1
        tps += 1
        Deb[s] = tps
        return True
    return False

# 3. FONCTION TRAITER
def Traiter(s):
    Parcours.append(s)

# 4. INITIALISATION DFS
def InitParcours(n):
    global Marque, pi, Deb, Fin, Parcours, tps, Pile, File
    Marque = [0] * n
    pi = [None] * n
    Deb = [0] * n
    Fin = [0] * n
    Parcours = []
    Pile = []
    File = []
    tps = 0


def InitDFS(n):
    InitParcours(n)


def InitBFS(n):
    InitParcours(n)

# 5. PARCOURS EN PROFONDEUR RECURSIF
def DFSREC(graphe, s):
    global tps
    # Marquer le sommet
    if not Marquer(s):
        return

    # Traiter le sommet
    Traiter(s)
    # Parcourir les successeurs
    for si in graphe[s]:
        if Marque[si] == 0:
            pi[si] = s
            DFSREC(graphe, si)
    # Fin du traitement
    Marque[s] = 2
    tps += 1
    Fin[s] = tps

# 6. PARCOURS EN PROFONDEUR ITERATIF
def DFSITER(graphe, s):
    global tps, Pile
    n = len(graphe)
    # Marquer le sommet de départ
    if not Marquer(s):
        return
    # Traiter le sommet
    Traiter(s)
    # Empiler le sommet de départ
    Pile.append(s)
    # Mémoriser le prochain successeur à examiner
    suivant = [0] * n
    while Pile:
        sommet = Pile[-1]
        trouve = False
        # Rechercher un successeur non visité
        while suivant[sommet] < len(graphe[sommet]):
            si = graphe[sommet][suivant[sommet]]
            suivant[sommet] += 1

            if Marque[si] == 0:
                # Enregistrer le prédécesseur
                pi[si] = sommet
                # Marquer le successeur
                Marquer(si)
                # Traiter le successeur
                Traiter(si)
                # Empiler le successeur
                Pile.append(si)
                trouve = True
                break

        # Si aucun successeur non visité n'est trouvé
        if not trouve:
            # Retirer le sommet de la pile
            Pile.pop()
            # Terminer son exploration
            Marque[sommet] = 2
            tps += 1
            Fin[sommet] = tps


# 7. PARCOURS EN LARGEUR RECURSIF
def BFSREC(graphe, s):
    global File

    if not Marquer(s):
        return

    File.append(s)
    _traiter_file_bfs(graphe, 0)


def _traiter_file_bfs(graphe, position):
    global tps

    if position >= len(File):
        File.clear()
        return

    sommet = File[position]
    Traiter(sommet)

    for si in graphe[sommet]:
        if Marque[si] == 0:
            pi[si] = sommet
            Marquer(si)
            File.append(si)

    Marque[sommet] = 2
    tps += 1
    Fin[sommet] = tps

    _traiter_file_bfs(graphe, position + 1)


# 8. PARCOURS EN LARGEUR ITERATIF
def BFSITER(graphe, s):
    global tps, File

    if not Marquer(s):
        return

    File.append(s)
    position = 0

    while position < len(File):
        sommet = File[position]
        position += 1
        Traiter(sommet)

        for si in graphe[sommet]:
            if Marque[si] == 0:
                pi[si] = sommet
                Marquer(si)
                File.append(si)

        Marque[sommet] = 2
        tps += 1
        Fin[sommet] = tps

    File.clear()

def lancer_parcours():
    try:
        n = int(champ_nombre.get())
        s = int(champ_depart.get())
        matrice = [[int(v) for v in ligne.split()]
                   for ligne in champ_matrice.get("1.0", "end").splitlines() if ligne.strip()]
    except ValueError:
        afficher("Entre un nombre de sommets, un sommet de départ et une matrice valide.")
        return

    oriente = choix_graphe.get() == "Orienté"
    if n <= 0 or not verifier_matrice(matrice, n, oriente):
        afficher("Matrice invalide : elle doit être carrée, binaire et symétrique si non orientée.")
        return
    if not 1 <= s <= n:
        afficher(f"Le sommet de départ doit être entre 1 et {n}.")
        return

    graphe = construire_adjacence(matrice)
    s_indice = s - 1
    parcours = choix_parcours.get()
    methode = choix_methode.get()

    if parcours == "Profondeur":
        InitDFS(n)
        (DFSREC if methode == "Récursif" else DFSITER)(graphe, s_indice)
    else:
        InitBFS(n)
        (BFSREC if methode == "Récursif" else BFSITER)(graphe, s_indice)

    lignes = [
        f"{parcours} ({methode})",
        "Ordre : " + " -> ".join(str(v + 1) for v in Parcours),
        "",
        f"{'Sommet':>7} {'Prédécesseur':>14} {'Marque':>8} {'Début':>8} {'Fin':>8}",
        "-" * 49,
    ]
    for i in range(n):
        pred = "NIL" if pi[i] is None else str(pi[i] + 1)
        lignes.append(
            f"{i + 1:>7} {pred:>14} {Marque[i]:>8} {Deb[i]:>8} {Fin[i]:>8}"
        )
    afficher("\n".join(lignes))


def afficher(texte):
    sortie.configure(state="normal")
    sortie.delete("1.0", "end")
    sortie.insert("1.0", texte)
    sortie.configure(state="disabled")


ctk.set_appearance_mode("system")
fenetre = ctk.CTk()
fenetre.title("Parcours de graphes")
fenetre.geometry("1180x840")
fenetre.minsize(1000, 700)
fenetre.grid_columnconfigure(0, weight=1)
fenetre.grid_columnconfigure(1, weight=1)

ctk.CTkLabel(fenetre, text="Parcours de graphes", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, padx=20, pady=(18, 8))

choix_graphe = ctk.CTkSegmentedButton(
    fenetre,
    values=["Non orienté", "Orienté"],
    height=42,
    font=("Segoe UI", 15, "bold"),
    selected_color="#176B73",
    selected_hover_color="#12575E",
    unselected_hover_color=("#DCEDEF", "#34494B"),
    border_width=2,
)
choix_graphe.set("Non orienté")
choix_graphe.grid(row=1, column=0, padx=16, pady=4, sticky="ew")

reglages = ctk.CTkFrame(fenetre)
reglages.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
reglages.grid_columnconfigure((1, 3), weight=1)
ctk.CTkLabel(reglages, text="Sommets").grid(row=0, column=0, padx=(10, 4), pady=8)
champ_nombre = ctk.CTkEntry(reglages, placeholder_text="n")
champ_nombre.grid(row=0, column=1, padx=4, pady=8, sticky="ew")
ctk.CTkLabel(reglages, text="Départ").grid(row=0, column=2, padx=(10, 4), pady=8)
champ_depart = ctk.CTkEntry(reglages, placeholder_text="s")
champ_depart.grid(row=0, column=3, padx=(4, 10), pady=8, sticky="ew")

ctk.CTkLabel(fenetre, text="1. Saisie de la matrice d'adjacence").grid(row=3, column=0, padx=16, pady=(4, 2), sticky="w")
ctk.CTkLabel(fenetre, text="Valeurs séparées par des espaces; uniquement 0 et 1.").grid(row=4, column=0, padx=16, pady=(0, 2), sticky="w")
champ_matrice = ctk.CTkTextbox(fenetre, height=115)
champ_matrice.grid(row=5, column=0, padx=16, pady=2, sticky="ew")
champ_matrice.insert("1.0", "0 1 0\n1 0 1\n0 1 0")

ctk.CTkLabel(fenetre, text="2. Choix du parcours").grid(row=6, column=0, padx=16, pady=(4, 2), sticky="w")
choix_parcours = ctk.CTkSegmentedButton(
    fenetre,
    values=["Profondeur", "Largeur"],
    height=44,
    font=("Segoe UI", 16, "bold"),
    selected_color="#176B73",
    selected_hover_color="#12575E",
    unselected_hover_color=("#DCEDEF", "#34494B"),
    border_width=2,
)
choix_parcours.set("Profondeur")
choix_parcours.grid(row=7, column=0, padx=16, pady=3, sticky="ew")
choix_methode = ctk.CTkSegmentedButton(
    fenetre,
    values=["Récursif", "Itératif"],
    height=44,
    font=("Segoe UI", 16, "bold"),
    selected_color="#176B73",
    selected_hover_color="#12575E",
    unselected_hover_color=("#DCEDEF", "#34494B"),
    border_width=2,
)
choix_methode.set("Récursif")
choix_methode.grid(row=8, column=0, padx=16, pady=3, sticky="ew")

ctk.CTkButton(
    fenetre,
    text="Lancer le parcours",
    command=lancer_parcours,
    height=44,
    font=("Segoe UI", 16, "bold"),
    hover_color="#12575E",
).grid(row=9, column=0, padx=16, pady=6)

ctk.CTkLabel(fenetre, text="Résultats", font=("Segoe UI", 18, "bold")).grid(
    row=0, column=1, padx=(8, 20), pady=(18, 8), sticky="w"
)
sortie = ctk.CTkTextbox(fenetre, height=700, state="disabled", font=("Consolas", 14))
sortie.grid(row=1, column=1, rowspan=10, padx=(8, 20), pady=(0, 18), sticky="nsew")
fenetre.grid_rowconfigure(5, weight=1)
fenetre.grid_rowconfigure(10, weight=1)

fenetre.mainloop()