from .legacy.brute_force import gen_all

def generate():
    for item in gen_all():
        yield item
