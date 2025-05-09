#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>   // Для std::setw
#include <windows.h>  // Для SetConsoleOutputCP()

using namespace std;

// Большое значение для имитации бесконечности
const long long INF = 1e18;

// Функция для чтения матрицы из файла
vector<vector<long long>> readMatrix(const string& filename) {
    vector<vector<long long>> matrix;
    ifstream file(filename);
    if (!file) {
        cerr << "Ошибка открытия файла: " << filename << endl;
        exit(1);
    }

    string line;
    while (getline(file, line)) {
        vector<long long> row;
        stringstream ss(line);
        long long value;
        while (ss >> value) {
            row.push_back(value);
        }
        matrix.push_back(row);
    }
    return matrix;
}

// Функция для умножения матриц с учётом режима (min или max)
vector<vector<long long>> multiply(const vector<vector<long long>>& A, const vector<vector<long long>>& B, const string& mode) {
    int n = A.size();
    vector<vector<long long>> result(n, vector<long long>(n, 0));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mode == "min") {
                long long minVal = INF;
                for (int m = 0; m < n; ++m) {
                    if (A[i][m] != 0 && B[m][j] != 0) {
                        long long current = A[i][m] + B[m][j];
                        if (current < minVal) {
                            minVal = current;
                        }
                    }
                }
                result[i][j] = (minVal != INF) ? minVal : 0;
            }
            else if (mode == "max") {
                long long maxVal = -INF;
                for (int m = 0; m < n; ++m) {
                    if (A[i][m] != 0 && B[m][j] != 0) {
                        long long current = A[i][m] + B[m][j];
                        if (current > maxVal) {
                            maxVal = current;
                        }
                    }
                }
                result[i][j] = (maxVal != -INF) ? maxVal : 0;
            }
        }
    }
    return result;
}

// Алгоритм Шимбелла
vector<vector<long long>> shimbel(const vector<vector<long long>>& matrix, int k, const string& mode) {
    int n = matrix.size();
    vector<vector<long long>> result = matrix;

    for (int step = 0; step < k - 1; ++step) {
        result = multiply(result, matrix, mode);
    }
    return result;
}

// Функция для вывода матрицы с выравниванием
void printMatrix(const vector<vector<long long>>& matrix) {
    for (const auto& row : matrix) {
        for (long long val : row) {
            cout << setw(4) << val;  // Фиксированная ширина 4 символа
        }
        cout << endl;
    }
}

int main() {
    // Установка кодировки консоли на Windows-1251 (кириллица)
    SetConsoleOutputCP(1251);

    char choice;
    do {
        string filename;
        cout << "Введите имя файла: ";
        cin >> filename;

        if (filename.find(".txt") == string::npos) {
            filename += ".txt";
        }

        vector<vector<long long>> matrix = readMatrix(filename);

        // Вывод исходной матрицы
        cout << "\nИсходная матрица:\n";
        printMatrix(matrix);

        int k;
        string mode;

        cout << "Введите количество переходов: ";
        cin >> k;
        cin.ignore(1000, '\n');  // Очистка буфера ввода

        cout << "Введите режим (max/min): ";
        cin >> mode;
        cin.ignore(1000, '\n');  // Очистка буфера ввода

        for (auto& c : mode) {
            c = tolower(c);
        }

        vector<vector<long long>> result = shimbel(matrix, k, mode);
        cout << "\nРезультат для " << k << " переходов и режима '" << mode << "':\n";
        printMatrix(result);

        cout << "Хотите сделать еще ввод? (y/n): ";
        cin >> choice;
    } while (choice == 'y' || choice == 'Y');

    return 0;
}