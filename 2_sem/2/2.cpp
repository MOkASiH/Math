#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>
#include <clocale>
#include <cstdio>
#include <windows.h>

using namespace std;

// Структура для хранения информации о ребре графа
struct Edge {
    int from;   // Начальная вершина (например, 0)
    int to;     // Конечная вершина (например, 1)
    int cost;   // Стоимость соединения между вершинами
};

// Функция для поиска "корня" группы, к которой принадлежит вершина
// Используется для проверки: находятся ли две вершины в одной группе?
int findParent(int v, vector<int>& parent) {
    // Если текущая вершина не является корнем группы, рекурсивно ищем его
    if (parent[v] != v) {
        // Сжатие пути: обновляем ссылку на родителя, чтобы ускорить будущие поиски
        parent[v] = findParent(parent[v], parent);
    }
    return parent[v];
}

// Функция для объединения двух групп вершин
// Используется для соединения двух компонент связности
void unionSets(int a, int b, vector<int>& parent, vector<int>& rank) {
    // Находим корни групп для вершин a и b
    int rootA = findParent(a, parent);
    int rootB = findParent(b, parent);

    // Объединяем группы по рангу (глубине дерева)
    if (rank[rootA] < rank[rootB]) {
        // Группа A меньше, подвешиваем её к группе B
        parent[rootA] = rootB;
    }
    else if (rank[rootA] > rank[rootB]) {
        // Группа B меньше, подвешиваем её к группе A
        parent[rootB] = rootA;
    }
    else {
        // Если группы одинаковой глубины, выбираем одну и увеличиваем её ранг
        parent[rootB] = rootA;
        rank[rootA]++;
    }
}

int main() {
    // Настройка локали для корректного отображения кириллицы
#ifdef _WIN32
    SetConsoleCP(1251);       // Установка кодовой страницы для ввода
    SetConsoleOutputCP(1251); // Установка кодовой страницы для вывода
#endif
    setlocale(LC_ALL, "Russian"); // Поддержка русского языка

    // Ввод имени файла с данными
    string filename;
    cout << "Введите имя файла с матрицей смежности: ";
    cin >> filename;

    // Открытие файла
    ifstream fin(filename);
    if (!fin) {
        cerr << "Ошибка: Не удалось открыть файл!\n";
        return 1;
    }

    // Определение максимального количества вершин
    const int MAX_NODES = 10;
    // Создаём матрицу смежности (MAX_NODES x MAX_NODES)
    int matrix[MAX_NODES][MAX_NODES] = { 0 };

    // Чтение данных из файла в матрицу
    for (int i = 0; i < MAX_NODES; i++) {
        for (int j = 0; j < MAX_NODES; j++) {
            fin >> matrix[i][j]; // Считываем значение из файла
        }
    }
    fin.close();

    // Выводим прочитанную матрицу на экран для проверки
    cout << "\nМатрица смежности:\n";
    for (int i = 0; i < MAX_NODES; i++) {
        for (int j = 0; j < MAX_NODES; j++) {
            cout << matrix[i][j] << " "; // Выводим элементы матрицы
        }
        cout << "\n"; // Переход на новую строку после каждой строки матрицы
    }

    // Создаём список рёбер графа
    vector<Edge> edges;
    for (int i = 0; i < MAX_NODES; i++) {
        // Проходим только по верхнему треугольнику матрицы, чтобы избежать дублирования
        for (int j = i + 1; j < MAX_NODES; j++) {
            if (matrix[i][j] > 0) {  // Если есть ребро (стоимость > 0)
                // Добавляем ребро в список
                edges.push_back({ i, j, matrix[i][j] });
            }
        }
    }

    // Сортируем рёбра по возрастанию стоимости
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.cost < b.cost; // Сортировка по полю cost
        });

    // Создаём структуры для отслеживания связей между вершинами
    vector<int> parent(MAX_NODES); // Хранит родителя для каждой вершины
    vector<int> rank(MAX_NODES, 0); // Хранит глубину дерева для оптимизации

    // Изначально каждая вершина сама себе родитель
    for (int i = 0; i < MAX_NODES; i++) {
        parent[i] = i;
    }

    // Основной алгоритм Краскала для построения минимального остовного дерева
    vector<Edge> mst;   // Хранилище рёбер минимального дерева
    int totalCost = 0;  // Общая стоимость дерева

    for (const Edge& e : edges) {
        // Находим корни групп для начальной и конечной вершин ребра
        int rootFrom = findParent(e.from, parent);
        int rootTo = findParent(e.to, parent);

        // Если вершины находятся в разных группах
        if (rootFrom != rootTo) {
            mst.push_back(e);           // Добавляем ребро в дерево
            totalCost += e.cost;        // Увеличиваем общую стоимость
            unionSets(rootFrom, rootTo, parent, rank);  // Объединяем группы
        }
        // Если корни совпадают - ребро создаёт цикл, пропускаем его
    }

    // Выводим результаты на экран
    cout << "\n--- Минимальное остовное дерево ---\n";
    cout << "+----------------+----------------+---------+\n";
    cout << "| Исходный узел  | Конечный узел  | Стоимость |\n";
    cout << "+----------------+----------------+---------+\n";

    // Форматированный вывод рёбер дерева
    for (const Edge& e : mst) {
        printf("| %-14d | %-14d | %-8d|\n", e.from, e.to, e.cost);
    }

    cout << "+----------------+----------------+---------+\n";
    cout << "\nОбщая стоимость остовного дерева: " << totalCost << "\n";

    return 0;
}