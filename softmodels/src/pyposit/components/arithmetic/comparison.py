def bin_g_u(a: str, b: str):
    if a and b:
        return int(a, 2) > int(b, 2)
    return False

def bin_geq_u(a: str, b: str):
    return int(a, 2) >= int(b, 2)

def bin_eq_u(a: str, b: str):
    return int(a, 2) == int(b, 2)

def bin_g_s(a: str, b: str):
    if a[0] == "1" and b[0] == "1":
        # both negative
        return int(twoc(a, len(a)), 2) < int(twoc(a, len(a)), 2)
    elif a[0] == "1" and b[0] == "0":
        return False
    elif a[0] == "0" and b[0] == "1":
        return True
    else:
        # both positive
        return int(a, 2) > int(b, 2)

def bin_geq_s(a: str, b: str):
    dprint.debug(f"{a} >= {b}?")
    if a[0] == "1" and b[0] == "1":
        # both negative
        return int(twoc(a, len(a)), 2) <= int(twoc(a, len(a)), 2)
    elif a[0] == "1" and b[0] == "0":
        return False
    elif a[0] == "0" and b[0] == "1":
        return True
    else:
        # both positive
        dprint.debug(int(a, 2) >= int(b, 2))
        return int(a, 2) >= int(b, 2)

def bin_eq_s(a: str, b: str):
    return a == b