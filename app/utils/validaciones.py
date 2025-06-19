def validar_tarjeta(numero: str) -> bool:
    numero = numero.replace(" ", "")
    if not numero.isdigit() or not 13 <= len(numero) <= 19:
        return False

    # Algoritmo de Luhn
    total = 0
    reverse_digits = numero[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n = n * 2
            if n > 9:
                n = n - 9
        total += n
    return total % 10 == 0