import std;
import matrix_io;
import matrix_ops;

using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::microseconds;

int main(int argc, char* argv[]) {
    std::string fileA = "matrix_A.txt";
    std::string fileB = "matrix_B.txt";
    std::string fileC = "matrix_C.txt";

    if (argc > 3) {
        fileA = argv[1];
        fileB = argv[2];
        fileC = argv[3];
    }

    int N = 0;
    Matrix A = readMatrix(fileA, N);
    int N_B = 0;
    Matrix B = readMatrix(fileB, N_B);

    if (N != N_B) {
        std::cerr << "Ошибка: размеры матриц не совпадают!\n";
        return 1;
    }

    auto start = high_resolution_clock::now();
    Matrix C = multiplyMatrices(A, B);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start).count();

    writeMatrix(fileC, C);

    double ops = 2.0 * N * N * N;
    std::cout << "Размер матрицы: " << N << "x" << N << "\n";
    std::cout << "Время выполнения: " << duration << " мкс\n";
    std::cout << "Объем задачи (операций): " << std::scientific << ops << "\n";
    std::cout << "Производительность: " << (ops / (duration / 1000000.0)) / 1e9 << " GFLOPS\n";

    return 0;
}
