int main(int argc, char* argv[]) {
    // Параметры по умолчанию
    string fileA = "matrix_A.txt";
    string fileB = "matrix_B.txt";
    string fileC = "matrix_C.txt";

    // Если переданы аргументы командной строки, используем их
    if (argc > 3) {
        fileA = argv[1];
        fileB = argv[2];
        fileC = argv[3];
    }

    int N = 0;
    // 1. Чтение данных
    vector<vector<double>> A = readMatrix(fileA, N);
    int N_B = 0;
    vector<vector<double>> B = readMatrix(fileB, N_B);

    if (N != N_B) {
        std::cerr << "Ошибка: размеры матриц не совпадают!\n";
        return 1;
    }

    // 2. Замер времени и вычисление
    auto start = high_resolution_clock::now();
    
    vector<vector<double>> C = multiplyMatrices(A, B);
    
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start).count();

    // 3. Запись результата
    writeMatrix(fileC, C);

    // 4. Вывод метрик (время, объем задачи)
    // Объем задачи ~ N^3 операций
    double ops = 2.0 * N * N * N; // 2*N^3 (умножение + сложение)
    cout << "Размер матрицы: " << N << "x" << N << "\n";
    cout << "Время выполнения: " << duration << " мкс\n";
    cout << "Объем задачи (операций): " << std::scientific << ops << "\n";
    cout << "Производительность: " << (ops / (duration / 1000000.0)) / 1e9 << " GFLOPS\n";

    return 0;
}
