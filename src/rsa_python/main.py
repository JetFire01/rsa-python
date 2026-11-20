import random

p_A = 13280088505642389747520384591513377632328532070608031357249975374919340106830514897144925405477087396287773080269283127066739537518630456260984213974485221
q_A = 11682619078275215713794513285785301319180550136642351219882272632802866988795535011054530433469191291674614925441602006391813030380365293421580367983762821
n_A = p_A * q_A
e_A = 18171582484455818149
m_1 = 889160867553528548

# Résultats attendus

d_A = 142344935243824339677319890783058676554585896618193331010073159693755671840361864949801588542177133964454383406606951246899652177124029544378212873717218461022612446977084145630969954283472880161579325638007340308623736878273549985679503360811584834982877796130952032674220448328046457160841761285727937491549
CIPHER = 152555937684495359471827428462018259580643721900068931799071633626221530445105966799781184327690458419551807578471499476624839513130973275913499915506715238744733513639436942411351751608618468442626434739706743210694059554888710396762471171752387024041288763316498048580913019998964648959265884798026184228534


# Exponentiation rapide

def exponentiation_rapide(base: int, exponent: int, modulus: int) -> int:

    if modulus == 1:
        return 0

    # On cherche d'abord la plus grande puissance de 2
    p = 1
    while p <= exponent:
        p *= 2
    p //= 2

    # Puis on la retire tant que possible, en descendant
    puissances_de_2 = []
    reste = exponent
    while reste > 0:
        if p <= reste:
            puissances_de_2.append(p)
            reste -= p
        p //= 2

    # Сalculons le valeur pour chaque puissance
    table = {}
    p = 1
    valeur = base % modulus
    while p <= exponent:
        table[p] = valeur
        valeur = (valeur * valeur) % modulus
        p *= 2

    # Multiplions que les puissances nécessaires
    result = 1
    for p in puissances_de_2:
        result = (result * table[p]) % modulus
    return result


# Test de primalité de Fermat

def test_de_primalite(n: int) -> bool:

    # Cas triviaux
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # 20 répétitions (cas difficile)
    for _ in range(20):
        a = random.randint(2, n - 1)
        if exponentiation_rapide(a, n - 1, n) != 1:
            return False  # n composé
    return True


# Algorithme étendu d'Euclide

def euclid_etendu(a: int, b: int) -> tuple[int, int, int]:

    r_prec = a
    r_act = b
    s_prec = 1
    s_act = 0
    t_prec = 0
    t_act = 1

    # On s'arrête dès que le prochain reste vaut 0 (r_prec est le pgcd)
    while r_act != 0:
        q = r_prec // r_act

        r_prec, r_act = r_act, r_prec - q * r_act
        s_prec, s_act = s_act, s_prec - q * s_act
        t_prec, t_act = t_act, t_prec - q * t_act

    # Quand r_act = 0, les valeurs précédentes sont r_i, s_i, t_i
    return r_prec, s_prec, t_prec


# Inverse modulaire de e via Euclide étendu

def mod_inverse(e: int, modulus: int) -> int:

    r, s, t = euclid_etendu(modulus, e)
    if r != 1: # on peut inverser e seulement si le pgcd = 1
        raise ValueError(f"e n'est pas inversible modulo {modulus} (pgcd = {r})")
    return t % modulus


# Génération des clés

def generer_cles(p: int, q: int, e: int) -> tuple[tuple[int, int], tuple[int, int]]:

    n = p * q
    f_n = (p - 1) * (q - 1)
    d = mod_inverse(e, f_n)
    return (e, n), (d, n)


# Chiffrement et déchiffrement

def chiffrement(message: int, publique_cle: tuple[int, int]) -> int:

    e, n = publique_cle
    if not 0 <= message < n:
        raise ValueError("Le message doit vérifier 0 <= m < n")
    return exponentiation_rapide(message, e, n)


def dechiffrement(cipher: int, privee_cle: tuple[int, int]) -> int:

    d, n = privee_cle
    return exponentiation_rapide(cipher, d, n)



# Programme principal

def separer_section(title: str) -> None:

    print()
    print("-" * 70)
    print(title)
    print("-" * 70)



# 1) Vérification de la primalité de p et q

separer_section("1) Vérification de la primalité (test de Fermat)")
p_ok = test_de_primalite(p_A)
q_ok = test_de_primalite(q_A)
print(f"p = {p_A}")
print(f"  -> {'probablement premier' if p_ok else 'COMPOSÉ'}")
print(f"q = {q_A}")
print(f"  -> {'probablement premier' if q_ok else 'COMPOSÉ'}")

if not (p_ok and q_ok):
    print("\nErreur : p et q doivent être premiers.")


# Message initial
separer_section("Message initial")
print(f"message = {m_1}")

# 2) Génération des clés
separer_section("2) Génération des clés")
public_key, private_key = generer_cles(p_A, q_A, e_A)
d_A = private_key[0]
print(f"n = p * q = {n_A}")
print(f"e = {e_A}")
print(f"d = {d_A}")
print(f"\nclé publique  (e, n) = ({public_key[0]}, {public_key[1]})")
print(f"\nclé privée    (d, n) = ({private_key[0]}, {private_key[1]})")

# 3) Chiffrement
separer_section("3) Chiffrement (c = m^e mod n)")
cipher = chiffrement(m_1, public_key)
print(f"c = {cipher}")

# 4) Déchiffrement
separer_section("4) Déchiffrement (m' = c^d mod n)")
decrypted = dechiffrement(cipher, private_key)
print(f"messame' = {decrypted}")
print(f"message' == message ? {decrypted == m_1}")

# Vérification par rapport aux valeurs attendues
separer_section("Vérification avec les résultats attendus")
print(f"d correct      : {d_A == d_A}")
print(f"chiffré correct: {cipher == CIPHER}")
# Comparaison avec pow()
print(f"contrôle pow() : {cipher == pow(m_1, e_A, n_A)}")