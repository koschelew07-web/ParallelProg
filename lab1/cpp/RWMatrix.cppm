// Функция для чтения матрицы из файла
vector<vector<double>> readMatrix(const string& filename, int& N) {
    ifstream fin(filename);
    if (!fin.is_open()) {
        // В модулях std::cerr доступен через std::
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        std::exit(1);
    }
    fin >> N;
    vector<vector<double>> matrix(N, vector<double>(N));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fin >> matrix[i][j];
        }
    }
    fin.close();
    return matrix;
}

// Функция для записи матрицы в файл
void writeMatrix(const string& filename, const vector<vector<double>>& matrix) {
    ofstream fout(filename);
    if (!fout.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << filename << "\n";
        std::exit(1);
    }
    int N = matrix.size();
    fout << N << "\n";
    fout << std::fixed << std::setprecision(4); // Формат вывода
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            fout << matrix[i][j] << " ";
        }
        fout << "\n";
    }
    fout.close();
}
