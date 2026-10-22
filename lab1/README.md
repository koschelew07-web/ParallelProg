# Лабораторная работа: Перемножение квадратных матриц на C++ с верификацией и бенчмаркингом

## 1. Постановка задачи
Реализовать программу на C/C++ для перемножения двух квадратных матриц. 
*   **Входные данные:** файлы с матрицами.
*   **Выходные данные:** файл с результатом, время выполнения, объем задачи.
*   **Верификация:** проверка правильности с помощью сторонней библиотеки (Python/NumPy).
*   **Исследование:** построение зависимости времени от размера задачи.

---

## 2. Структура проекта
```text
lab1/
├── cpp/                     
│   ├── matrix_io.cppm       
│   ├── matrix_ops.cppm    
│   └── main.cpp             
├── data/                    
├── out/                     
├── verify_and_bench.py      
└── README.md
```
---

## 3. Разбор кода C++
3.1 matrix_io.cppm
Этот модуль изолирует работу с файловой системой
```
export using Matrix = std::vector<std::vector<double>>;

export Matrix readMatrix(const std::string& filename, int& N) {
    std::ifstream fin(filename);
    if (!fin.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        std::exit(1); // Аварийное завершение, если файла нет
    }
    
    fin >> N; 
    
    Matrix matrix(N, std::vector<double>(N));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fin >> matrix[i][j]; // Читаем элементы построчно
        }
    }
    return matrix;
}

export void writeMatrix(const std::string& filename, const Matrix& matrix) {
    std::ofstream fout(filename);
    int N = matrix.size();
    fout << N << "\n";
    fout << std::fixed << std::setprecision(4); // Округляем до 4 знаков
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fout << matrix[i][j] << " ";
        }
        fout << "\n";
    }
}
```
3.2 matrix_ops.cppm
Здесь реализован классический алгоритм (ijk-алгоритм) со сложностью O(N³).
```
export module matrix_ops;
import std;
import matrix_io; // Используем тип Matrix из предыдущего модуля

export Matrix multiplyMatrices(const Matrix& A, const Matrix& B) {
    int N = A.size();
    Matrix C(N, std::vector<double>(N, 0.0)); // Результат инициализируем нулями

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                C[i][j] += A[i][k] * B[k][j]; // Накопление суммы
            }
        }
    }
    return C;
}
```
3.3 main.cpp
В этой части происходит оркестрация и чистый замер времени.
```
import std;
import matrix_io;
import matrix_ops;

int main(int argc, char* argv[]) {
    std::string fileA = (argc > 1) ? argv[1] : "matrix_A.txt";
    std::string fileB = (argc > 2) ? argv[2] : "matrix_B.txt";
    std::string fileC = (argc > 3) ? argv[3] : "matrix_C.txt";

    int N = 0;
    Matrix A = readMatrix(fileA, N);
    int N_B = 0;
    Matrix B = readMatrix(fileB, N_B);

    auto start = std::chrono::high_resolution_clock::now();
    
    Matrix C = multiplyMatrices(A, B);
    
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

    writeMatrix(fileC, C);

    double ops = 2.0 * N * N * N; 
    double gflops = (ops / (duration / 1000000.0)) / 1e9;

    std::cout << "Размер матрицы: " << N << "x" << N << "\n";
    std::cout << "Время выполнения: " << duration << " мкс\n";
    std::cout << "Производительность: " << gflops << " GFLOPS\n";

    return 0;
}
```
## 4. verify_and_bench.py
Python-скрипт выполняет роль умного ассистента: генерирует данные, запускает C++ программу, проверяет её и строит графики.
4.1 Верификация
```
def verify(fileA, fileB, fileC):
    # Загружаем текстовые файлы в массивы NumPy
    A = np.loadtxt(fileA, skiprows=1)
    B = np.loadtxt(fileB, skiprows=1)
    C_cpp = np.loadtxt(fileC, skiprows=1)
    
    C_numpy = A @ B
    
    # atol=1e-3 (допуск 0.001), так как C++ и NumPy могут складывать числа в разном порядке.
    ok = np.allclose(C_cpp, C_numpy, atol=1e-3)
    print("Верификация пройдена" if ok else "Ошибка верификации")
```
4.2. Бенчмаркинг
Для каждого размера N скрипт генерирует случайные матрицы, вызывает matrix_mul.exe через subprocess и вытаскивает время из консольного вывода:
```
result = subprocess.run([str(BIN), str(fileA), str(fileB), str(fileC)], capture_output=True, text=True)
for line in result.stdout.split("\n"):
    if "Время" in line:
        t = float(line.split(":")[1].replace("мкс", "").strip()) / 1000 # перевод в мс
        times.append(t)
```
## 5. Анализ графика

<img width="640" height="480" alt="benchmark" src="https://github.com/user-attachments/assets/8e918704-6ba1-4a2b-865b-2b6e1cb3c3b7" />

На графике представлены две линии: Сплошная линия (Эксперимент): Реальное время работы C++ программы для N = 100 , 200 , 400 , 600 , 800 N=100,200,400,600,800. Пунктирная линия (Теория O(N³)): Математическая модель, нормированная по первой точке. Формула: \[
 t(N) = t(100) \cdot \left(\frac{N}{100}\right)^3 
\]

На графике видно, что экспериментальная точка для N=800 чуть выше теоретической. Это связано с эффектом кэш-памяти (Cache Miss). При размере 800x800 матрица занимает около 5 МБ (800 * 800 * 8 байт). Процессор перестает помещать её в сверхбыстрый кэш (L3), и данные начинают подгружаться из более медленной оперативной памяти. Поэтому время немного возрастает, а линия чуть отклоняется вверх. Это нормальное поведение для реальных вычислительных систем.
