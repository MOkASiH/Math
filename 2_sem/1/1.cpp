#include <iostream>
#include <vector>
#include <stack>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

// Функция для выполнения поиска в глубину (DFS)
void performDFS(int vertex, const vector<vector<int>>& adjacency, vector<bool>& visited, vector<int>& component) {
    stack<int> stack;
    stack.push(vertex);
    visited[vertex] = true;
    component.push_back(vertex);

    while (!stack.empty()) {
        int current = stack.top();
        stack.pop();
        for (int neighbor = 0; neighbor < adjacency.size(); neighbor++) {
            if (adjacency[current][neighbor] && !visited[neighbor]) {
                visited[neighbor] = true;
                component.push_back(neighbor);
                stack.push(neighbor);
            }
        }
    }
}

// Функция для поиска компонент связности
void findComponents(const vector<vector<int>>& adjacency, vector<vector<int>>& components) {
    int size = adjacency.size();
    vector<bool> visited(size, false);

    for (int i = 0; i < size; i++) {
        if (!visited[i]) {
            vector<int> component;
            performDFS(i, adjacency, visited, component);
            components.push_back(component);
        }
    }
}

// Функция перемножения матриц
vector<vector<int>> multiplyMatrices(const vector<vector<int>>& A, const vector<vector<int>>& B) {
    int size = A.size();
    vector<vector<int>> result(size, vector<int>(size, 0));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            for (int k = 0; k < size; k++) {
                result[i][j] |= (A[i][k] && B[k][j]);
            }
        }
    }
    return result;
}

// Функция расчета матрицы достижимости
vector<vector<int>> calculateReachability(const vector<vector<int>>& adjacency) {
    int size = adjacency.size();
    vector<vector<int>> reachability = adjacency;
    vector<vector<int>> temp = adjacency;

    for (int power = 1; power < size; power++) {
        temp = multiplyMatrices(temp, adjacency);
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                reachability[i][j] |= temp[i][j];
            }
        }
    }

    for (int i = 0; i < size; i++) {
        reachability[i][i] |= adjacency[i][i];
    }

    return reachability;
}

// Функция чтения матрицы смежности из файла
vector<vector<int>> readAdjacencyMatrix(const string& filename, int& size) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: Не удалось открыть файл " << filename << endl;
        exit(EXIT_FAILURE);
    }

    vector<vector<int>> adjacency;
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        vector<int> row;
        int value;
        while (ss >> value) {
            if (value < 0 || value > 1) {
                cerr << "Ошибка: Недопустимое значение " << value << " в файле" << endl;
                exit(EXIT_FAILURE);
            }
            row.push_back(value);
        }
        if (!row.empty()) adjacency.push_back(row);
    }
    file.close();

    size = adjacency.size();
    for (const auto& row : adjacency) {
        if (row.size() != size) {
            cerr << "Ошибка: Матрица должна быть квадратной" << endl;
            exit(EXIT_FAILURE);
        }
    }

    return adjacency;
}

int main() {
    // Установка кодировки для Windows
#ifdef _WIN32
    system("chcp 1251 > nul");
    setlocale(LC_ALL, "Rus");
#else
    setlocale(LC_ALL, "ru_RU.UTF-8");
#endif

    cout << "**********************************************" << endl;
    cout << "*        Анализ графа с помощью матриц        *" << endl;
    cout << "**********************************************" << endl;

    string filename;
    cout << "\nВведите имя файла (например, graph.txt): ";
    getline(cin, filename);

    int size;
    vector<vector<int>> adjacencyMatrix = readAdjacencyMatrix(filename, size);

    cout << "\n--- Исходная матрица смежности ---" << endl;
    for (int i = 0; i < size; i++) {
        cout << "Вершина " << i << ": ";
        for (int j = 0; j < size; j++) {
            cout << adjacencyMatrix[i][j] << " ";
        }
        cout << endl;
    }

    // Создаем неориентированный граф
    vector<vector<int>> undirectedMatrix = adjacencyMatrix;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (adjacencyMatrix[i][j] || adjacencyMatrix[j][i]) {
                undirectedMatrix[i][j] = undirectedMatrix[j][i] = 1;
            }
        }
    }

    cout << "\n--- Неориентированный граф ---" << endl;
    for (int i = 0; i < size; i++) {
        cout << "Вершина " << i << ": ";
        for (int j = 0; j < size; j++) {
            cout << undirectedMatrix[i][j] << " ";
        }
        cout << endl;
    }

    // Поиск компонент связности
    vector<vector<int>> connectedComponents;
    findComponents(undirectedMatrix, connectedComponents);

    // Расчет матрицы достижимости
    vector<vector<int>> reachabilityMatrix = calculateReachability(adjacencyMatrix);

    cout << "\n--- Матрица достижимости ---" << endl;
    cout << "    ";
    for (int i = 0; i < size; i++) cout << '\t' << "v" << i << " ";
    cout << endl;
    for (int i = 0; i < size; i++) {
        cout << "v" << i << " | ";
        for (int j = 0; j < size; j++) {
            cout << '\t' << reachabilityMatrix[i][j];
        }
        cout << endl;
    }

    cout << "\n--- Результаты анализа ---" << endl;
    cout << "Обнаружено " << connectedComponents.size() << " компонент связности:" << endl;
    for (size_t i = 0; i < connectedComponents.size(); i++) {
        cout << "  * Компонента " << i + 1 << " ("
            << connectedComponents[i].size() << " вершин): ";
        for (int v : connectedComponents[i]) {
            cout << v << " ";
        }
        cout << endl;
    }

    return 0;
}