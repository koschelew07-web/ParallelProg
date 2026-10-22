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
// Экспортируем псевдоним типа, чтобы не писать длинную конструкцию везде
export using Matrix = std::vector<std::vector<double>>;

export Matrix readMatrix(const std::string& filename, int& N) {
    std::ifstream fin(filename);
    if (!fin.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        std::exit(1); // Аварийное завершение, если файла нет
    }
    
    fin >> N; // Первое число в файле — размерность N
    
    // Создаем матрицу N x N, заполненную нулями
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
