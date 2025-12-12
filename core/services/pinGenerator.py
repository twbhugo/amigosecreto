#Generate Random PIN from 111111 to 999999

import random
def generate_random_pin() -> str:
    return str(random.randint(111111, 999999))