from bech32 import bech32_encode, bech32_decode


def addr_to_val(addr):
    prefix, data = bech32_decode(addr)
    return bech32_encode(f"{prefix}valoper", data)
