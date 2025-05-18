#include <iostream>
#include <string>

using namespace std;

bool check_language(const string& word) {
    int state = 0; // 0 - S0, 1 - S1, 2 - S2

    for (char c : word) {
        if (state == 2) break; 

        switch (state) {
        case 0:
            if (c != 'a' and c != 'b' and c != 'c' and c != 'd') {
                return false;
            }
            if (c == 'a') {
                state = 1;
            }   
            break;
        case 1:
            if (c != 'a' and c != 'b' and c != 'c' and c != 'd') {
                return false;
            }
            if (c == 'a') {
                state = 2;
            }
            else {
                state = 0;
            }
            break;
        }
    }

    return state != 2;
}

int main() {
    string input;
    cout << "Enter a word: ";
    cin >> input;
    


    if (check_language(input)) {
        cout << "yes" << endl;
    }
    else {
        cout << "no" << endl;
    }

    return 0;
}