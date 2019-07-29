from cryptography.fernet import Fernet

key = "TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM="

# Oh no! The code is going over the edge! What are you going to do?
message = (
    b"gAAAAABdPv9WLka6lNobkDOProai-joKrZ6CEUVpm50RCXog4_W3Hvc-PTdCcJC8lqW0RW1kR9Zj-22E0xxTRVlohMk0"
    b"fm3-W37B7f-Kv_D2kx7LEOEoFkE5TP7Qwc9dUh29AXLbBEhyCEnncVrLvks1U1p9xRvKlepSZIUtl0M70u-qnhEOuvE="
)


numbers = [
    104,
    116,
    116,
    112,
    115,
    58,
    47,
    47,
    101,
    110,
    103,
    105,
    110,
    101,
    101,
    114,
    105,
    110,
    103,
    45,
    97,
    112,
    112,
    108,
    105,
    99,
    97,
    116,
    105,
    111,
    110,
    46,
    98,
    114,
    105,
    116,
    101,
    99,
    111,
    114,
    101,
    46,
    99,
    111,
    109,
    47,
    113,
    117,
    105,
    122,
    47,
    119,
    101,
    102,
    102,
    107,
    102,
    112,
    102,
    108,
    101,
    109,
    115,
    105,
    115,
    111,
    100,
    100,
]


def main():
    print('step 1: ', ''.join(chr(i) for i in numbers))
    f = Fernet(key)
    print('step 2: ', f.decrypt(message))


if __name__ == "__main__":
    main()
