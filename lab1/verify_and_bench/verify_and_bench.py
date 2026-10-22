import numpy as np
import subprocess
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(r"D:\ParallelProg-main\lab1")

BIN = Path(r"D:\ParallelProg-main\lab1\out\build\x64-Debug\matrix_mul.exe")
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True) 

def generate_matrix(path, N):
    matrix = np.random.rand(N, N) * 10
    with open(path, 'w') as f:
        f.write(f"{N}\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")

def verify(fileA, fileB, fileC):
    A = np.loadtxt(fileA, skiprows=1)
    B = np.loadtxt(fileB, skiprows=1)
    C_cpp = np.loadtxt(fileC, skiprows=1)
    C_numpy = A @ B
    ok = np.allclose(C_cpp, C_numpy, atol=1e-3)
    print("Верификация пройдена" if ok else 
    return ok

def benchmark(sizes):
    times = []
    fileA = DATA_DIR / "mat_A.txt"
    fileB = DATA_DIR / "mat_B.txt"
    fileC = DATA_DIR / "mat_C.txt"
    
    for N in sizes:
        generate_matrix(fileA, N)
        generate_matrix(fileB, N)
        
        result = subprocess.run(
            [str(BIN), str(fileA), str(fileB), str(fileC)],
            capture_output=True, text=True
        )
        
        found = False
        for line in result.stdout.split("\n"):
            if "Время" in line:
                times.append(float(line.split(":")[1].replace("мкс", "").strip()) / 1000)
                found = True
                break
        if not found:
            print(f"Ошибка при N={N}. Вывод программы:\n{result.stdout}\n{result.stderr}")
            return []
            
        print(f"N={N}: {times[-1]:.2f} мс")
    return times

if __name__ == "__main__":
    print("--- Тест верификации (N=50) ---")
    testA = DATA_DIR / "test_A.txt"
    testB = DATA_DIR / "test_B.txt"
    testC = DATA_DIR / "test_C.txt"
    generate_matrix(testA, 50)
    generate_matrix(testB, 50)
    
    subprocess.run([str(BIN), str(testA), str(testB), str(testC)])
    verify(testA, testB, testC)

    print("\n--- Запуск бенчмарка ---")
    sizes = [100, 200, 400, 600, 800]
    times = benchmark(sizes)

    if times:
        # 3. График
        plt.plot(sizes, times, 'o-', label='Эксперимент')
        plt.plot(sizes, [(n**3 / sizes[0]**3) * times[0] for n in sizes], '--', label='Теория O(N³)')
        plt.xlabel('Размер N')
        plt.ylabel('Время (мс)')
        plt.grid(True)
        plt.legend()
        plt.savefig(ROOT / "benchmark.png")
        print(f"\nГрафик сохранен: {ROOT / 'benchmark.png'}")
