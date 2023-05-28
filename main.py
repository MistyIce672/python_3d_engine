def quik_sort(items):
    items.sort(key=lambda f: sum(v[2] for v in f) / len(f),reverse =True)
    return(items)

print(quik_sort([[(1, 2, 5), (3, 4, 1)], [(2, 2, 3), (0, 0, 2)], [(4, 5, 6), (1, 1, 1)]]))