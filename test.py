def replace_chars(s, r):
    for c in r:
        s = s.replace(c, "$")
    print(s)


replace_chars("elephant", "ae")
