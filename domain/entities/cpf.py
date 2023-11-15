import re


def validate_cpf(cpf: str) -> bool:
    if not cpf:
        return False

    cpf = clean_cpf(cpf)

    if is_invalid_length(cpf):
        return False

    if are_all_digits_same(cpf):
        return False

    dg1 = calculate_digit(cpf, 10)
    dg2 = calculate_digit(cpf, 11)
    extracted_cpf = extract_digit(cpf)
    return extracted_cpf == f"{dg1}{dg2}"


def clean_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)


def is_invalid_length(cpf: str) -> bool:
    return len(cpf) != 11


def are_all_digits_same(cpf: str) -> bool:
    return all(c == cpf[0] for c in cpf)


def calculate_digit(cpf: str, factor: int) -> int:
    total = 0
    for digit in cpf:
        if factor > 1:
            total += int(digit) * factor
            factor -= 1
    rest = total % 11
    return 0 if rest < 2 else 11 - rest


def extract_digit(cpf: str) -> str:
    return cpf[9:]
