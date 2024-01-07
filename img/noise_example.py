from hybrid import make_hybrid

if __name__ == "__main__":
    x = make_hybrid()
    x.scatter([[1.7, 1.6, 0.3, 4.1]])
    x.save()
