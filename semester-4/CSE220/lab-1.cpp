
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

const int mod = 1e9+7;



/* Task-1 start from here */
/* const int NONE = INT_MIN; */
/* void  mergeLineup(array<int, 5>& arr1, array<int, 5>& arr2) { */
/*     array<int, 5> result; */
/*     int n = arr1.size(); */
/*     for (int i = 0; i < n; ++i) { */
/*         int hp1 = (arr1[i] == NONE) ? 0 : arr1[i]; */
/*         int hp2 = (arr2[n - 1 - i] == NONE) ? 0 : arr2[n - 1 - i]; */
/*         result[i] = hp1 + hp2; */
/*     } */
/*     for(auto &hp:result)cout<<hp<<" "; */
/*     cout<<endl; */
/* } */
/**/
/* signed main(void) { */
/*     array<int, 5> pokemon_1 = {4, 5, -1, NONE, NONE}; */
/*     array<int, 5> pokemon_2 = {2, 27, 7, 12, NONE}; */
/**/
/*     mergeLineup(pokemon_1,pokemon_2); */
/**/
/*     return 0; */
/* } */
/* Task-1 end here  */


/* Task-2 start from here */
/* void discardCards(vector<int>& cards, int t) { */
/**/
/*     vector<int> result; */
/*     bool check=false; */
/**/
/*     for (int &card : cards) { */
/*         if (card == t) check=!check; */
/**/
/*         if (!check || card != t) result.push_back(card); */
/*     } */
/**/
/*     while (result.size() < cards.size()) result.push_back(0); */
/**/
/*     for(auto &i:result)cout<<i<<" "; */
/*     cout<<endl; */
/**/
/* } */
/**/
/* signed main(void) { */
/*     vector<int> cards1 = {1, 3, 7, 2, 5, 2, 2, 2, 0}; */
/*     discardCards(cards1, 2); */
/*     vector<int> cards2 = {5, 5, 5, 0, 0}; */
/*     discardCards(cards2, 5); */
/**/
/**/
/*     return 0; */
/* } */
/* Task-2 end here  */


/* Task-3 start from here  */
/* vector<int> decrypt_matrix(const vector<vector<int>>& matrix) { */
/**/
/*     int rows = matrix.size(); */
/*     int cols = matrix[0].size(); */
/*     vector<int> column_sums(cols, 0); */
/**/
/*     for (int j = 0; j < cols; ++j) { */
/*         for (int i = 0; i < rows; ++i) { */
/*             column_sums[j] += matrix[i][j]; */
/*         } */
/*     } */
/**/
/*     vector<int> decrypted_array; */
/*     for (int j = 1; j < cols; ++j) { */
/*         decrypted_array.push_back(column_sums[j] - column_sums[j - 1]); */
/*     } */
/**/
/*     return decrypted_array; */
/* } */
/**/
/**/
/**/
/* signed main(void){ */
/*     vector<vector<int>> matrix = { */
/*         {1, 3, 1}, */
/*         {6, 4, 2}, */
/*         {5, 1, 7}, */
/*         {9, 3, 3}, */
/*         {8, 5, 4} */
/*     }; */
/**/
/*     vector<int> result = decrypt_matrix(matrix); */
/**/
/*     for (int val : result) { */
/*         cout << val << " "; */
/*     } */
/*     cout << endl; */
/**/
/*     return 0; */
/**/
/* } */
/* Task-3 end here  */





/* Task-4 start from here */
/* void solution(vector<vector<int>> &matrix){ */
/**/
/*     int rows = matrix.size(); */
/*     int cols = matrix[0].size(); */
/**/
/*     for (int j = 0; j < cols; ++j) { */
/*         if (!(j&1)) { */
/*             for (int i = 0; i < rows; i += 2) { */
/*                 cout << matrix[i][j] << " "; */
/*             } */
/*         } else { */
/*             if(rows&1){ */
/*                 for (int i = rows - 2; i >= 0; i -= 2) { */
/*                     cout << matrix[i][j] << " "; */
/*                 } */
/*             } */
/*             else { */
/*                 for (int i = rows - 1; i >= 0; i -= 2) { */
/*                     cout << matrix[i][j] << " "; */
/*                 } */
/*             } */
/*         } */
/*         cout << endl; */
/*     } */
/**/
/* } */
/* signed main(void){ */
/**/
/*     vector<vector<int>> matrix = { */
/*         {3, 8, 4, 6, 1}, */
/*         {7, 2, 1, 9, 3}, */
/*         {9, 0, 7, 5, 8}, */
/*         {2, 1, 3, 4, 0}, */
/*         {1, 4, 2, 8, 6} */
/*     }; */
/*     vector<vector<int>> matrix2={ */
/*         {3, 8, 4, 6, 1}, */
/*         {7, 2, 1, 9, 3}, */
/*         {9, 0, 7, 5, 8}, */
/*         {2, 1, 3, 4, 0} */
/*     }; */
/**/
/*     solution(matrix); */
/*     cout<<"Matrix-2"<<endl; */
/*     solution(matrix2); */
/* } */
/* Task-4 end here  */




/* Task-5 start from here  */
/* void row_rotation(int exam_week, vector<vector<string>> &seat_status) { */
/*     int rows = seat_status.size(); */
/*     int cols = seat_status[0].size(); */
/*     int rotations = exam_week % rows; */
/*     rotations-=1; */
/*     vector<vector<string>> new_seat_status(rows, vector<string>(cols)); */
/**/
/*     for (int i = 0; i < rows; ++i) { */
/*         new_seat_status[(i + rotations) % rows] = seat_status[i]; */
/*     } */
/*     for (const auto &row : new_seat_status) { */
/*         for (const auto &seat : row) { */
/*             cout << seat << " "; */
/*         } */
/*         cout << endl; */
/*     } */
/*     for (int i = 0; i < rows; ++i) { */
/*         for (int j = 0; j < cols; ++j) { */
/*             if (new_seat_status[i][j] == "AA") { */
/*                 cout << "Your friend AA will be on row " << i + 1 << "." << endl; */
/*                 return; */
/*             } */
/*         } */
/*     } */
/* } */
/**/
/**/
/* signed main(void){ */
/*     int exam_week = 3; */
/**/
/*     vector<vector<string>> seat_status = { */
/*         {"A", "B", "C", "D", "E"}, */
/*         {"F", "G", "H", "I", "J"}, */
/*         {"K", "L", "M", "N", "O"}, */
/*         {"P", "Q", "R", "S", "T"}, */
/*         {"U", "V", "W", "X", "Y"}, */
/*         {"Z", "AA", "BB", "CC", "DD"} */
/*     }; */
/**/
/*     row_rotation(exam_week,seat_status); */
/* } */
/* Task-5 end here */


/* Task-6 start here */
void compress_matrix(vector<vector<int>>&mat){
    int r=mat.size();
    int c=mat[0].size();

    vector<vector<int>> result(r>>1,vector<int> (c>>1,0));
    for(int i=0;i<r;i++){
        for(int j=0;j<c;j++){
            result[i>>1][j>>1]+=mat[i][j];
        }
    }
    for(auto &i:result){
        for(int &j:i)cout<<j<<" ";
        cout<<endl;
    }
}

signed main(void){

    vector<vector<int>> mat={ 
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {1, 3, 5, 2},
        {-2 ,0 ,6 ,-3}
    };
    compress_matrix(mat);
    return 0;
}
/* Task-6 end here */


/* Task-7 start from here */
/* void isSurvived(const vector<vector<int>>& arena) { */
/*     int rows = arena.size(); */
/*     int cols = arena[0].size(); */
/*     int totalPoints = 0; */
/**/
/*     vector<pair<int, int>> directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}}; */
/**/
/*     for (int i = 0; i < rows; ++i) { */
/*         for (int j = 0; j < cols; ++j) { */
/*             if (arena[i][j] % 50 == 0 && arena[i][j] != 0) { */
/*                 for (const auto& dir : directions) { */
/*                     int newRow = i + dir.first; */
/*                     int newCol = j + dir.second; */
/*                     if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols && arena[newRow][newCol] == 2) { */
/*                         totalPoints += 2; */
/*                     } */
/*                 } */
/*             } */
/*         } */
/*     } */
/**/
/*     cout << "Points Gained: " << totalPoints << ". "; */
/*     if (totalPoints >= 10) { */
/*         cout << "Your team has survived the game." << endl; */
/*     } else { */
/*         cout << "Your team is out." << endl; */
/*     } */
/* } */
/* signed main(void){ */
/**/
/*     vector<vector<int>> arena1 = { */
/*         {0, 2, 2, 0}, */
/*         {50, 1, 2, 0}, */
/*         {2, 2, 2, 0}, */
/*         {1, 100, 2, 0} */
/*     }; */
/*     vector<vector<int>> arena2 = { */
/*         {0, 2, 2, 0, 2}, */
/*         {1, 50, 2, 1, 100}, */
/*         {2, 2, 2, 0, 2}, */
/*         {0, 200, 2, 0, 0} */
/*     }; */
/**/
/*     isSurvived(arena1); */
/*     isSurvived(arena2); */
/**/
/*     return 0; */
/* } */
/* Task-7 end here */




