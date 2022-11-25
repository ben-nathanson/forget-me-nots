SPECIAL_CHARACTERS = " !\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"


def is_strong_password(password: str) -> bool:
    if not isinstance(password, str):
        return False

    contains_lowercase: bool = password.upper() != password
    contains_uppercase: bool = password.lower() != password
    contains_numbers: bool = any(
        [character for character in password if character.isnumeric()]
    )
    contains_special_characters: bool = any(
        [character for character in password if character in SPECIAL_CHARACTERS]
    )
    is_longer_than_six_characters = len(password) >= 6
    if (
        contains_lowercase
        and contains_uppercase
        and contains_numbers
        and contains_special_characters
        and is_longer_than_six_characters
    ):
        return True
    else:
        return False
