export module matrix_io;

import std;

export using Matrix = std::vector<std::vector<double>>;

export Matrix readMatrix(const std::string& filename, int& N) {
    std::ifstream fin(filename);
    if (!fin.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        std::exit(1);
    }
    fin >> N;
    Matrix matrix(N, std::vector<double>(N));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fin >> matrix[i][j];
        }
    }
    return matrix;
}

export void writeMatrix(const std::string& filename, const Matrix& matrix) {
    std::ofstream fout(filename);
    if (!fout.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << filename << "\n";
        std::exit(1);
    }
    int N = matrix.size();
    fout << N << "\n";
    fout << std::fixed << std::setprecision(4);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fout << matrix[i][j] << " ";
        }
        fout << "\n";
    }
}
