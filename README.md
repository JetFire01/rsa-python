# rsa-python

A from-scratch implementation of the RSA cryptosystem in Python

All number-theory building blocks are implemented by hand. No cryptography
library is used, and the built-in three-argument `pow(base, exp, mod)` is used
only once, at the very end, to cross-check the results.

## What it does

Using the example values provided with the assignment (`p`, `q`, `e` and the
message `m`), the program:

1. Checks that `p` and `q` are (probably) prime with the Fermat primality test
   (20 random bases).
2. Generates the keys: `n = p·q`, `φ(n) = (p−1)(q−1)` and `d = e⁻¹ mod φ(n)`.
3. Encrypts the message: `c = mᵉ mod n`.
4. Decrypts the ciphertext: `m' = cᵈ mod n`, and checks that `message' = message`.
5. Compares `d` and `c` with the expected values.

## Implementation overview

All functions live in `src/rsa_python/main.py`:

| Function | Purpose |
|---|---|
| `exponentiation_rapide` | Fast modular exponentiation (square-and-multiply) |
| `test_de_primalite` | Fermat primality test |
| `euclid_etendu` | Extended Euclidean algorithm (gcd and Bézout coefficients) |
| `mod_inverse` | Modular inverse built on the extended Euclidean algorithm |
| `generer_cles` | Computes `d` and returns the public `(e, n)` and private `(d, n)` keys |
| `chiffrement` / `dechiffrement` | RSA encryption and decryption |

## Requirements

- Python 3.9 or newer
- No third-party dependencies (only the standard `random` module)

## Running

```bash
python3 -m venv .venv
source .venv/bin/activate
PYTHONPATH=src python -m rsa_python.main
```

The program runs almost instantly (well under a second), even with the
1024-bit modulus.

