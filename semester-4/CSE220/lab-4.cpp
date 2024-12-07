#include <bits/stdc++.h>
using namespace std;
/* #define int long long */
#define endl '\n'

const int mod = 1e9+7;

/* Task-1 start here */
/* class VehicleNode { */
/*     public: */
/*         string brand; */
/*         string vehicle_type; */
/*         int rent; */
/*         int passenger; */
/*         VehicleNode* next; */
/**/
/*         VehicleNode(string brand, string vehicle_type, int rent, int passenger) { */
/*             this->brand = brand; */
/*             this->vehicle_type = vehicle_type; */
/*             this->rent = rent; */
/*             this->passenger = passenger; */
/*             this->next = nullptr; */
/*         } */
/* }; */

/* class VehicleHashTable { */
/*     public: */
/*         vector<VehicleNode*> vehicleTable; */
/*         int size; */
/**/
/*         VehicleHashTable(int size) { */
/*             this->size = size; */
/*             vehicleTable.resize(size, nullptr); */
/*         } */
/**/
/*         int __hash_function(string brand) { */
/*             int sum = 0; */
/*             for (char c : brand) { */
/*                 sum += int(c); */
/*             } */
/*             int index = sum % size; */
/*             return index; */
/*         } */
/**/
/*         void insert_vehicle(vector<string> vehicle) { */
/*             string brand = vehicle[0]; */
/*             string vehicle_type = vehicle[1]; */
/*             int rent = stoi(vehicle[2]); */
/*             int passenger = stoi(vehicle[3]); */
/**/
/*             int index = __hash_function(brand); */
/*             VehicleNode* newNode = new VehicleNode(brand, vehicle_type, rent, passenger); */
/**/
/*             if (vehicleTable[index] == nullptr) { */
/*                 vehicleTable[index] = newNode; */
/*             } else { */
/*                 VehicleNode* current = vehicleTable[index]; */
/*                 while (current->next != nullptr) { */
/*                     if (current->brand == brand) { */
/*                         break; */
/*                     } */
/*                     current = current->next; */
/*                 } */
/*                 if (current->brand == brand) { */
/*                     newNode->next = current->next; */
/*                     current->next = newNode; */
/*                 } else { */
/*                     int emptyIndex = find_empty_slot(); */
/*                     vehicleTable[emptyIndex] = newNode; */
/*                 } */
/*             } */
/*         } */
/**/
/*         int find_empty_slot() { */
/*             for(int i=0;i<size;i++)if(!vehicleTable[i])return i; */
/*             return -1; */
/*         } */
/**/
/*         void create_from_vehicle_info_array(vector<vector<string>> arr) { */
/*             for (auto& vehicle : arr) { */
/*                 insert_vehicle(vehicle); */
/*             } */
/*         } */
/**/
/*         void print_vehicle_hashtable() { */
/*             int idx = 0; */
/*             for (auto& head : vehicleTable) { */
/*                 cout << idx << ": "; */
/*                 while (head != nullptr) { */
/*                     cout << "(Brand: " << head->brand << ", Type: " << head->vehicle_type << ", Rent: " << head->rent << ", No. of Passengers: " << head->passenger << ")---->"; */
/*                     head = head->next; */
/*                 } */
/*                 cout << "None" << endl; */
/*                 idx++; */
/*             } */
/*         } */
/* }; */
/**/
/* signed  main(void) { */
/*     vector<vector<string>> vehicle_info = { */
/*         {"Toyota", "Private Car", "500", "4"}, */
/*         {"Jeep", "SUV", "950", "6"}, */
/*         {"Lamborghini", "SUV", "6900", "6"}, */
/*         {"Hyundai", "Bike", "100", "1"}, */
/*         {"BMW", "Private Car", "1000", "8"}, */
/*         {"Honda", "Bike", "150", "1"}, */
/*         {"Ferrari", "Private Car", "2500", "4"}, */
/*         {"BMW", "Minivan", "5800", "7"} */
/*     }; */
/**/
/*     VehicleHashTable vht(8); */
/*     vht.create_from_vehicle_info_array(vehicle_info); */
/*     vht.print_vehicle_hashtable(); */
/**/
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */
/* class NodePair { */
/*     public: */
/*         string key; */
/*         int value; */
/*         NodePair* next; */
/**/
/*         NodePair(string key, int value, NodePair* next = nullptr) { */
/*             this->key = key; */
/*             this->value = value; */
/*             this->next = next; */
/*         } */
/* }; */
/**/
/* class Hashtable { */
/*     public: */
/*         vector<NodePair*> ht; */
/**/
/*         Hashtable(int size) { */
/*             ht.resize(size, nullptr); */
/*         } */
/**/
/*         int __hash_function(string key) { */
/*             if (key.length() % 2 != 0) { */
/*                 key += 'N'; */
/*             } */
/*             int sum = 0; */
/*             for (size_t i = 0; i < key.length(); i += 2) { */
/*                 int concatenated = int(key[i]) * 1000 + int(key[i + 1]); */
/*                 sum += concatenated; */
/*             } */
/*             int index = sum % ht.size(); */
/*             return index; */
/*         } */
/**/
/*         void insert(pair<string, int> s) { */
/*             if (search_hashtable(s) == "Found") { */
/*                 cout << s.first << " Already Inserted. Cannot reinsert." << endl; */
/*                 cout << "===============================" << endl; */
/*                 return; */
/*             } */
/*             int hashed_index = __hash_function(s.first); */
/*             NodePair* pair = new NodePair(s.first, s.second); */
/*             if (ht[hashed_index] == nullptr) { */
/*                 ht[hashed_index] = pair; */
/*             } else { */
/*                 pair->next = ht[hashed_index]; */
/*                 ht[hashed_index] = pair; */
/*             } */
/*         } */
/**/
/*         void create_from_array(vector<pair<string, int>> arr) { */
/*             for (auto& i : arr) { */
/*                 insert(i); */
/*             } */
/*         } */
/**/
/*         void print_hashtable() { */
/*             int idx = 0; */
/*             for (auto& i : ht) { */
/*                 cout << idx << ": "; */
/*                 NodePair* head = i; */
/*                 while (head != nullptr) { */
/*                     cout << "(key: " << head->key << ", value: " << head->value << ")-->"; */
/*                     head = head->next; */
/*                 } */
/*                 cout << "None" << endl; */
/*                 cout << endl; */
/*                 idx++; */
/*             } */
/*         } */
/**/
/*         string search_hashtable(pair<string, int> s) { */
/*             int hashed_index = __hash_function(s.first); */
/*             NodePair* current = ht[hashed_index]; */
/*             while (current != nullptr) { */
/*                 if (current->key == s.first) { */
/*                     return "Found"; */
/*                 } */
/*                 current = current->next; */
/*             } */
/*             return "Not Found"; */
/*         } */
/* }; */
/**/
/* signed main(void) { */
/*     vector<pair<string, int>> arr = {{"Colt", 360}, {"Cordelius", 730}, {"Shelly", 300}, {"Doug", 1200}, {"Emz", 520}, {"Bo", 580}}; */
/*     Hashtable ht(5); */
/*     ht.create_from_array(arr); */
/*     ht.print_hashtable(); */
/**/
/*     cout << "======================" << endl; */
/*     string result = ht.search_hashtable({"Doug", 1200}); */
/*     cout << "(Doug, 1200) " << result << endl; */
/**/
/*     cout << "======================" << endl; */
/*     ht.insert({"Doug", 1200}); */
/*     ht.print_hashtable(); */
/**/
/*     cout << "======================" << endl; */
/*     result = ht.search_hashtable({"Edgar", 320}); */
/*     cout << "(Edgar, 320) " << result << endl; */
/**/
/*     cout << "======================" << endl; */
/*     ht.insert({"Edgar", 320}); */
/*     ht.print_hashtable(); */
/**/
/*     cout << "======================" << endl; */
/*     result = ht.search_hashtable({"Edgar", 320}); */
/*     cout << "(Edgar, 320) " << result << endl; */
/**/
/*     return 0; */
/* } */
/* Task-2 end here */


/* Task-3 start here */
/* class Node { */
/*     public: */
/*         pair<string, int> value; */
/*         Node* next; */
/**/
/*         Node(pair<string, int> value, Node* next = nullptr) { */
/*             this->value = value; */
/*             this->next = next; */
/*         } */
/* }; */
/**/
/* class HashTable { */
/*     public: */
/*         vector<Node*> ht; */
/*         int length; */
/**/
/*         HashTable(int length) { */
/*             this->length = length; */
/*             ht.resize(length, nullptr); */
/*         } */
/**/
/*         int __hash_function(string key) { */
/*             int sum = 0; */
/*             if (key.length() % 2 == 0) { */
/*                 for (int i = 0; i < key.length(); i += 2) { */
/*                     sum += int(key[i]); */
/*                 } */
/*             } else { */
/*                 for (int i = 1; i < key.length(); i += 2) { */
/*                     sum += int(key[i]); */
/*                 } */
/*             } */
/*             return sum % length; */
/*         } */
/**/
/*         void insert(string key, int value) { */
/*             int index = __hash_function(key); */
/*             Node* newNode = new Node(make_pair(key, value)); */
/*             if (ht[index] == nullptr) { */
/*                 ht[index] = newNode; */
/*             } else { */
/*                 Node* current = ht[index]; */
/*                 Node* prev = nullptr; */
/*                 while (current != nullptr && current->value.second > value) { */
/*                     prev = current; */
/*                     current = current->next; */
/*                 } */
/*                 if (prev == nullptr) { */
/*                     newNode->next = ht[index]; */
/*                     ht[index] = newNode; */
/*                 } else { */
/*                     newNode->next = current; */
/*                     prev->next = newNode; */
/*                 } */
/*             } */
/*         } */
/**/
/*         void show() { */
/*             int count = 0; */
/*             for (auto& head : ht) { */
/*                 cout << count << " "; */
/*                 Node* temp = head; */
/*                 while (temp != nullptr) { */
/*                     cout << "(" << temp->value.first << ", " << temp->value.second << ")-->"; */
/*                     temp = temp->next; */
/*                 } */
/*                 cout << "None" << endl; */
/*                 count++; */
/*             } */
/*         } */
/* }; */
/**/
/* int main() { */
/*     HashTable ht(3); */
/**/
/*     cout << "------Test#1------" << endl; */
/*     ht.insert("apple", 20); */
/*     ht.insert("coconut", 90); */
/*     ht.insert("cherry", 50); */
/*     ht.show(); */
/**/
/*     cout << "------Test#2------" << endl; */
/*     ht.insert("banana", 30); */
/*     ht.insert("pineapple", 50); */
/*     ht.show(); */
/**/
/*     cout << "------Test#3------" << endl; */
/*     ht.insert("apple", 100); */
/*     ht.insert("Guava", 10); */
/*     ht.show(); */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */

/* Task-4 start here */

class Node {
    public:
        int key;
        string value;
        Node* next;

        Node(int key, string value, Node* next = nullptr) {
            this->key = key;
            this->value = value;
            this->next = next;
        }
};

class Hashtable {
    public:
        vector<Node*> ht;

        Hashtable(int size) {
            ht.resize(size, nullptr);
        }

        int __hash_function(int key) {
            return (key + 3) % ht.size();
        }

        void insert(pair<int, string> s) {
            int hashed_index = __hash_function(s.first);
            Node* pair = new Node(s.first, s.second);
            if (ht[hashed_index] == nullptr) {
                ht[hashed_index] = pair;
            } else {
                pair->next = ht[hashed_index];
                ht[hashed_index] = pair;
            }
        }

        void create_from_array(vector<pair<int, string>> arr) {
            for (auto& i : arr) {
                insert(i);
            }
        }

        void print_hashtable() {
            int idx = 0;
            for (auto& i : ht) {
                cout << idx << ": ";
                Node* head = i;
                while (head != nullptr) {
                    cout << "(" << head->key << ", " << head->value << ")-->";
                    head = head->next;
                }
                cout << "None" << endl;
                idx++;
            }
        }

        void remove(int key) {
            int hashed_index = __hash_function(key);
            Node* current = ht[hashed_index];
            Node* prev = nullptr;

            while (current != nullptr && current->key != key) {
                prev = current;
                current = current->next;
            }

            if (current == nullptr) {
                return; // Key not found
            }

            if (prev == nullptr) {
                ht[hashed_index] = current->next;
            } else {
                prev->next = current->next;
            }

            delete current;
        }
};

signed main(void) {
    vector<pair<int, string>> arr = {{34, "Abid"}, {4, "Rafi"}, {6, "Karim"}, {3, "Chitra"}, {22, "Nilu"}, {18, "Niloy"}, {30, "Laima"}};
    Hashtable ht(6);
    ht.create_from_array(arr);
    ht.print_hashtable();

    cout << "======================" << endl;

    ht.remove(22);
    ht.print_hashtable();

    cout << "======================" << endl;

    ht.remove(18);
    ht.print_hashtable();

    cout << "======================" << endl;

    ht.remove(6);
    ht.print_hashtable();

    cout << "======================" << endl;

    ht.remove(3);
    ht.print_hashtable();

    return 0;
}
/* Task-4 end here */
