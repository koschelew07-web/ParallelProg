import numpy as np
import subprocess
import matplotlib.pyplot as plt

# --- Генерация матрицы и сохранение в файл ---
def generate_matrix(filename, N):
    matrix = np.random.rand(N, N) * 10
    with open(filename, 'w') as f:
        f.write(f"{N}\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")

# --- Верификация: сравнение C++ с NumPy ---
def verify(fileA, fileB, fileC):
    A = np.loadtxt(fileA, skiprows=1)
    B = np.loadtxt(fileB, skiprows=1)
    C_cpp = np.loadtxt(fileC, skiprows=1)
    C_numpy = A @ B   # оператор @ — матричное умножение
    ok = np.allclose(C_cpp, C_numpy, atol=1e-3)
    print("✅ Верификация пройдена" if ok else "❌ Ошибка верификации")
    return ok

# --- Бенчмарк: замер времени для разных N ---
def benchmark(sizes):
    times = []
    for N in sizes:
        generate_matrix("mat_A.txt", N)
        generate_matrix("mat_B.txt", N)
        result = subprocess.run(
            ["./matrix_mul", "mat_A.txt", "mat_B.txt", "mat_C.txt"],
            capture_output=True, text=True
        )
        # Ищем строку "Время выполнения: X мкс"
        for line in result.stdout.split("\n"):
            if "Время" in line:
                times.append(float(line.split(":")[1].replace("мкс", "").strip()) / 1000)
                break
        print(f"N={N}: {times[-1]:.2f} мс")
    return times

# --- MAIN ---
if __name__ == "__main__":
    # 1. Быстрый тест верификации на маленькой матрице
    generate_matrix("test_A.txt", 50)
    generate_matrix("test_B.txt", 50)
    subprocess.run(["./matrix_mul", "test_A.txt", "test_B.txt", "test_C.txt"])
    verify("test_A.txt", "test_B.txt", "test_C.txt")

    # 2. Бенчмарк
    sizes = [100, 200, 400, 600, 800]
    times = benchmark(sizes)

    # 3. График
    plt.plot(sizes, times, 'o-', label='Эксперимент')
    theory = [(n**3 / sizes[0]**3) * times[0] for n in sizes]
    plt.plot(sizes, theory, '--', label='Теория O(N³)')
    plt.xlabel('Размер N'); plt.ylabel('Время (мс)')
    plt.grid(True); plt.legend()
    plt.savefig('benchmark.png'); plt.show()
