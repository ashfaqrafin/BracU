#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'


/* Task-1 start here */
/**/
/* class Patient { */
/*     public: */
/*         int id; */
/*         string name; */
/*         int age; */
/*         string bloodgroup; */
/**/
/*         Patient(int id, string name, int age, string bloodgroup) { */
/*             this->id = id; */
/*             this->name = name; */
/*             this->age = age; */
/*             this->bloodgroup = bloodgroup; */
/*         } */
/* }; */
/**/
/* class Node { */
/*     public: */
/*         Patient* patient; */
/*         Node* next; */
/*         Node* prev; */
/**/
/*         Node(Patient* patient) { */
/*             this->patient = patient; */
/*             this->next = this; */
/*             this->prev = this; */
/*         } */
/* }; */
/**/
/* class WRM { */
/*     private: */
/*         Node* dummyHead; */
/**/
/*     public: */
/*         WRM() { */
/*             dummyHead = new Node(nullptr); */
/*         } */
/**/
/*         void RegisterPatient(int id, string name, int age, string bloodgroup) { */
/*             Patient* newPatient = new Patient(id, name, age, bloodgroup); */
/*             Node* newNode = new Node(newPatient); */
/*             Node* tail = dummyHead->prev; */
/**/
/*             tail->next = newNode; */
/*             newNode->prev = tail; */
/*             newNode->next = dummyHead; */
/*             dummyHead->prev = newNode; */
/**/
/*             cout << "Success" << endl; */
/*         } */
/**/
/*         void ServePatient() { */
/*             if (dummyHead->next == dummyHead) { */
/*                 cout << "No patients to serve" << endl; */
/*                 return; */
/*             } */
/**/
/*             Node* firstPatientNode = dummyHead->next; */
/*             cout << "Serving Patient: " << firstPatientNode->patient->name << endl; */
/**/
/*             dummyHead->next = firstPatientNode->next; */
/*             firstPatientNode->next->prev = dummyHead; */
/**/
/*             delete firstPatientNode->patient; */
/*             delete firstPatientNode; */
/*         } */
/**/
/*         void CancelAll() { */
/*             Node* current = dummyHead->next; */
/*             while (current != dummyHead) { */
/*                 Node* temp = current; */
/*                 current = current->next; */
/*                 delete temp->patient; */
/*                 delete temp; */
/*             } */
/*             dummyHead->next = dummyHead; */
/*             dummyHead->prev = dummyHead; */
/*             cout << "Success" << endl; */
/*         } */
/**/
/*         bool CanDoctorGoHome() { */
/*             return dummyHead->next == dummyHead; */
/*         } */
/**/
/*         void ShowAllPatient() { */
/*             Node* current = dummyHead->next; */
/*             while (current != dummyHead) { */
/*                 cout << current->patient->id << " "; */
/*                 current = current->next; */
/*             } */
/*             cout << endl; */
/*         } */
/**/
/*         void ReverseTheLine() { */
/*             Node* current = dummyHead; */
/*             do { */
/*                 swap(current->next, current->prev); */
/*                 current = current->prev; */
/*             } while (current != dummyHead); */
/*             cout << "Success" << endl; */
/*         } */
/* }; */
/**/
/* signed  main(void) { */
/*     WRM wrm; */
/*     int choice, id, age; */
/*     string name, bloodgroup; */
/**/
/*     while (true) { */
/*         cout << "1. Add Patient\n2. Serve Patient\n3. Show All Patients\n4. Can Doctor go Home?\n5. Cancel All Appointments\n6. Reverse The Line\n7. Exit\n"; */
/*         cin >> choice; */
/**/
/*         switch (choice) { */
/*             case 1: */
/*                 cout << "Enter ID, Name, Age, Bloodgroup: "; */
/*                 cin >> id >> name >> age >> bloodgroup; */
/*                 wrm.RegisterPatient(id, name, age, bloodgroup); */
/*                 break; */
/*             case 2: */
/*                 wrm.ServePatient(); */
/*                 break; */
/*             case 3: */
/*                 wrm.ShowAllPatient(); */
/*                 break; */
/*             case 4: */
/*                 cout << (wrm.CanDoctorGoHome() ? "Yes" : "No") << endl; */
/*                 break; */
/*             case 5: */
/*                 wrm.CancelAll(); */
/*                 break; */
/*             case 6: */
/*                 wrm.ReverseTheLine(); */
/*                 break; */
/*             case 7: */
/*                 return 0; */
/*             default: */
/*                 cout << "Invalid choice" << endl; */
/*         } */
/*     } */
/* } */

/* Task-1 end here */


/* Part-2(stack) */

/* Task=1 start here */
/* int count_diamond(stack<char>&st, string& input) { */
/*     int diamondCount = 0; */
/**/
/*     for (char c : input) { */
/*         if (c == '<') { */
/*             st.push(c); */
/*         } else if (c == '>') { */
/*             if (!st.empty() && st.top() == '<') { */
/*                 st.pop(); */
/*                 diamondCount++; */
/*             } */
/*         } */
/*     } */
/**/
/*     return diamondCount; */
/* } */
/**/
/* signed main(void){ */
/**/
/*     stack<char> st; */
/**/
/*     string s=".<...<<..>>....>....>>>."; */
/*     cout<<count_diamond(st,s)<<endl; */
/**/
/*     return 0; */
/* } */
/* Task-1 end here */

/* Task-2 start here */
/* void removeNthFromTop(stack<int>& st, int n) { */
/*     stack<int> temp; */
/**/
/*     n--; */
/*     while(!st.empty()){ */
/*         if(n)temp.push(st.top()); */
/*         st.pop(); */
/*         n--; */
/*     } */
/**/
/*     while(!temp.empty()){ */
/*         cout<<temp.top()<<" "; */
/*         temp.pop(); */
/*     } */
/*     cout<<endl; */
/* } */
/**/
/* signed main(void) { */
/*     stack<int> st; */
/*     st.push(4); */
/*     st.push(19); */
/*     st.push(23); */
/*     st.push(17); */
/*     st.push(5); */
/**/
/*     int n = 2; */
/*     removeNthFromTop(st, n); */
/*     return 0; */
/* } */

/* Task-2 end here */


/* Task-3 start here */
/* stack<int> conditional_reverse(stack<int> &st){ */
/**/
/*     stack<int> new_st; */
/*     while(!st.empty()){ */
/*         if(new_st.empty() or st.top()!=new_st.top()){ */
/*             new_st.push(st.top()); */
/*         } */
/*         st.pop(); */
/*     } */
/*     while(!new_st.empty()){ */
/*         st.push(new_st.top()); */
/*         new_st.pop(); */
/*     } */
/*     return st; */
/* } */
/**/
/* signed main(void){ */
/**/
/*     stack<int> st; */
/**/
/*     st.push(10); */
/*     st.push(10); */
/*     st.push(20); */
/*     st.push(20); */
/*     st.push(30); */
/*     st.push(10); */
/*     st.push(50); */
/**/
/*     stack<int> new_st=conditional_reverse(st); */
/**/
/*     while(!new_st.empty()){ */
/*         cout<<new_st.top()<<" "; */
/*         new_st.pop(); */
/*     } */
/*     cout<<endl; */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */


