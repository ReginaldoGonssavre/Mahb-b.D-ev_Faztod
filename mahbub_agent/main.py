from calculator import add_vectors

if __name__ == "__main__":
    vector_a = [1, 2, 3]
    vector_b = [4, 5, 6]
    result = add_vectors(vector_a, vector_b)
    print(f"A soma dos vetores {vector_a} e {vector_b} é {result}")