import numpy as np
import subprocess
import time
import os
import matplotlib.pyplot as plt

# --- Генерация данных ---
def generate_matrix(filename, N):
    """Генерирует случайную матрицу NxN и сохраняет в файл."""
    matrix = np.random.rand(N, N) * 10 # Числа от 0 до 10
    with open(filename, 'w') as f:
        f.write(f"{N}\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")
    return matrix

# --- Верификация ---
def verify_results(fileA, fileB, fileC):
    """Сравнивает результат C++ с numpy."""
    # Читаем исходные данные
    A = np.loadtxt(fileA, skiprows=1)
    B = np.loadtxt(fileB, skiprows=1)
    # Читаем результат C++
    C_cpp = np.loadtxt(fileC, skiprows=1)
    
    # Считаем эталон на Python
    C_python = np.dot(A, B)
    
    # Сравниваем с допуском (погрешность округления)
    if np.allclose(C_cpp, C_python, atol=1e-3):
        print("✅ Верификация пройдена: результаты совпадают.")
        return True
    else:
        print("❌ Ошибка верификации: результаты не совпадают!")
        # Вывод расхождений для отладки
        diff = np.abs(C_cpp - C_python)
        print(f"Максимальное расхождение: {np.max(diff)}")
        return False

# --- Исследование зависимости времени ---
def run_benchmark():
    sizes = [100, 200, 400, 600, 800] # Размеры матриц
    times = []
    
    print("\nЗапуск исследования зависимости времени...")
    
    for N in sizes:
        print(f"Тест для N={N}...")
        # Генерируем файлы
        generate_matrix("mat_A.txt", N)
        generate_matrix("mat_B.txt", N)
        
        # Запускаем C++ программу
        start = time.time()
        result = subprocess.run(["./matrix_mul", "mat_A.txt", "mat_B.txt", "mat_C.txt"], 
                                capture_output=True, text=True)
        end = time.time()
        
        # Парсим время из вывода C++ (или берем время Python, но лучше из C++)
        # В C++ мы выводим время в мкс, здесь для простоты возьмем разницу
        # Но правильнее парсить stdout C++
        output = result.stdout
        print(output) # Вывод C++ программы
        
        # Извлекаем время из вывода (грубый парсинг)
        # Ищем строку "Время выполнения: X мкс"
        for line in output.split('\n'):
            if "Время выполнения" in line:
                t_mks = float(line.split(':')[1].replace('мкс', '').strip())
                times.append(t_mks / 1000.0) # в миллисекунды
                break

    # Строим график
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label='Эксперимент')
    
    # Теоретическая кривая O(N^3)
    # Нормируем теоретическую кривую под первый эксперимент
    theory = [(n**3) / (sizes[0]**3) * times[0] for n in sizes]
    plt.plot(sizes, theory, '--', label='Теория O(N^3)')
    
    plt.xlabel('Размер матрицы (N)')
    plt.ylabel('Время выполнения (мс)')
    plt.title('Зависимость времени перемножения матриц от размера')
    plt.grid(True)
    plt.legend()
    plt.savefig('benchmark_plot.png')
    print("График сохранен как benchmark_plot.png")
    plt.show()

if __name__ == "__main__":
    # 1. Тест на маленькой матрице для верификации
    N_test = 50
    generate_matrix("test_A.txt", N_test)
    generate_matrix("test_B.txt", N_test)
    
    # Компиляция (если еще не скомпилировано)
    if not os.path.exists("./matrix_mul"):
        os.system("g++ -O2 -o matrix_mul matrix_mul.cpp")
        
    subprocess.run(["./matrix_mul", "test_A.txt", "test_B.txt", "test_C.txt"])
    verify_results("test_A.txt", "test_B.txt", "test_C.txt")
    
    # 2. Бенчмарк
    run_benchmark()
