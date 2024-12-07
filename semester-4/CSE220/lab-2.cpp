#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

const int mod= 1e9+7;


/* Task-1 start here */
/* struct Node{ */
/*     string color; */
/*     Node* next; */
/**/
/*     Node(string color){ */
/*         this->color=color; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/**/
/* bool check(Node* building1,Node* building2){ */
/**/
/*     while(building1!=nullptr and building2!=nullptr){ */
/*         if(building1->color!=building2->color)return false; */
/*         building1=building1->next; */
/*         building2=building2->next; */
/*     } */
/*     return true; */
/* } */
/**/
/* signed main(void){ */
/**/
/*     Node* building1 = new Node("Red"); */
/*     building1->next = new Node("Green"); */
/*     building1->next->next = new Node("Yellow"); */
/*     building1->next->next->next = new Node("Red"); */
/*     building1->next->next->next->next = new Node("Blue"); */
/*     building1->next->next->next->next->next = new Node("Green"); */
/**/
/*     Node* building2 = new Node("Red"); */
/*     building2->next = new Node("Green"); */
/*     building2->next->next = new Node("Yellow"); */
/*     building2->next->next->next = new Node("Red"); */
/*     building2->next->next->next->next = new Node("Blue"); */
/*     building2->next->next->next->next->next = new Node("Green"); */
/**/
/*     if(check(building1,building2))cout<<"Similar"<<endl; */
/*     else cout<<"Not Similar"<<endl; */
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */
/* struct Node{ */
/*     int data; */
/*     Node* next; */
/**/
/*     Node(int data){ */
/*         this->data=data; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/**/
/* void printList(Node* head) { */
/*     while (head != nullptr) { */
/*         cout << head->data; */
/*         if (head->next != nullptr) { */
/*             cout << "→"; */
/*         } */
/*         head = head->next; */
/*     } */
/*     cout << endl; */
/* } */
/* Node* removeNthFromEnd(Node* head, int n) { */
/**/
/*     Node* dummy = new Node(0); */
/*     dummy->next = head; */
/*     Node* first = dummy; */
/*     Node* second = dummy; */
/*     for (int i = 0; i <= n; ++i) { */
/*         first = first->next; */
/*     } */
/**/
/*     while (first != nullptr) { */
/*         first = first->next; */
/*         second = second->next; */
/*     } */
/**/
/*     Node* nodeToRemove = second->next; */
/*     second->next = second->next->next; */
/*     delete nodeToRemove; */
/**/
/*     Node* newHead = dummy->next; */
/*     delete dummy; */
/*     return newHead;  */
/**/
/* } */
/**/
/* signed main(void){ */
/**/
/*     Node* head = new Node(10); */
/*     head->next = new Node(15); */
/*     head->next->next = new Node(34); */
/*     head->next->next->next = new Node(41); */
/*     head->next->next->next->next = new Node(56); */
/*     head->next->next->next->next->next = new Node(72); */
/**/
/*     int n = 6; */
/*     if(n>6){ */
/*         printList(head); */
/*         return 0; */
/*     } */
/*     head = removeNthFromEnd(head, n); */
/*     printList(head); */
/**/
/*     return 0; */
/* } */
/* Task-2 end here  */



/* Task-3 start here */

/* struct Node{ */
/*     int data; */
/*     Node* next; */
/**/
/*     Node(int data){ */
/*         this->data=data; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/* bool check(Node* head){ */
/**/
/*     head=head->next; */
/*     while(head->next!=nullptr){ */
/*         if(head->data>head->next->data)return false; */
/*         head=head->next; */
/*     } */
/*     return true; */
/* } */
/**/
/**/
/* signed main(void){ */
/**/
/*     Node* head = new Node(10); */
/*     head->next = new Node(15); */
/*     head->next->next = new Node(34); */
/*     head->next->next->next = new Node(41); */
/*     head->next->next->next->next = new Node(56); */
/*     head->next->next->next->next->next = new Node(72); */
/**/
/*     cout<<(check(head)?"True":"False")<<endl; */
/**/
/**/
/*     Node* head2 = new Node(10); */
/*     head2->next = new Node(15); */
/*     head2->next->next = new Node(44); */
/*     head2->next->next->next = new Node(41); */
/*     head2->next->next->next->next = new Node(56); */
/*     head2->next->next->next->next->next = new Node(72); */
/**/
/*     cout<<(check(head2)?"True":"False")<<endl; */
/**/
/**/
/**/
/*     return 0; */
/* } */
/* Task-3 end here */


/* Task-4 start here */
/* struct Node{ */
/*     char data; */
/*     Node* next; */
/*     Node(char data){ */
/*         this->data=data; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/**/
/* Node* reverse(Node* head){ */
/**/
/*     Node* cur=head, *prev=nullptr, *next; */
/**/
/*     while(cur){ */
/*         next=cur->next; */
/*         cur->next=prev; */
/**/
/*         prev=cur; */
/*         cur=next; */
/*     } */
/*     return prev; */
/* } */
/**/
/* Node* decodeWord(Node* head,int len) { */
/*     int jmp=(13%len),cnt=1; */
/*     head=head->next; */
/*     bool flag=true; */
/**/
/*     Node* temp=new Node(0); */
/*     Node* fn= temp; */
/*     while(cnt<len){  */
/*         if(cnt%jmp==0){ */
/*             temp->next=head; */
/*             temp=temp->next; */
/*             head=head->next; */
/*             cnt++; */
/*             continue; */
/*         } */
/*         Node* toremove=head; */
/*         head=head->next; */
/*         delete toremove; */
/*         cnt++; */
/*     } */
/*     temp->next=nullptr; */
/*     Node* remove=fn; */
/*     fn=fn->next; */
/*     delete remove; */
/*     return reverse(fn); */
/* } */
/**/
/* void printList(Node* head) { */
/*     cout<<"None -> "; */
/*     while (head) { */
/*         cout << head->data; */
/*         if (head->next) cout << " -> "; */
/*         head = head->next; */
/*     } */
/*     cout << endl; */
/* } */
/**/
/* signed main() { */
/*     Node* head = new Node('B'); */
/*     head->next = new Node('M'); */
/*     head->next->next = new Node('D'); */
/*     head->next->next->next = new Node('T'); */
/*     head->next->next->next->next = new Node('N'); */
/*     head->next->next->next->next->next = new Node('O'); */
/*     head->next->next->next->next->next->next = new Node('A'); */
/*     head->next->next->next->next->next->next->next = new Node('P'); */
/*     head->next->next->next->next->next->next->next->next = new Node('S'); */
/*     head->next->next->next->next->next->next->next->next->next = new Node('C'); */
/**/
/*     Node* decodedHead = decodeWord(head,10); */
/*     printList(decodedHead); */
/*     return 0; */
/* } */
/* Task-4 end here */


/* Task-5 start here  */

/* struct Node { */
/*     int data; */
/*     Node* next; */
/**/
/*     Node(int data) { */
/*         this->data = data; */
/*         this->next = nullptr; */
/*     } */
/* }; */
/**/
/* Node* alternate_merge(Node* head1, Node* head2) { */
/*     Node* head = head1; */
/*     Node* temp1 = nullptr; */
/*     Node* temp2 = nullptr; */
/**/
/*     while (head1 != nullptr && head2 != nullptr) { */
/*         temp1 = head1->next; */
/*         temp2 = head2->next; */
/**/
/*         head1->next = head2; */
/*         if (temp1 == nullptr) { */
/*             break; */
/*         } */
/*         head2->next = temp1; */
/**/
/*         head1 = temp1; */
/*         head2 = temp2; */
/*     } */
/**/
/*     return head; */
/* } */
/**/
/* void printList(Node* head) { */
/*     while (head) { */
/*         cout << head->data; */
/*         cout << " -> "; */
/*         head = head->next; */
/*     } */
/*     cout<<"None"<<endl; */
/* } */
/**/
/* signed main(void) { */
/*     Node* head1 = new Node(1); */
/*     head1->next = new Node(2); */
/*     head1->next->next = new Node(6); */
/*     head1->next->next->next = new Node(8); */
/*     head1->next->next->next->next = new Node(11); */
/**/
/*     Node* head2 = new Node(5); */
/*     head2->next = new Node(7); */
/*     head2->next->next = new Node(3); */
/*     head2->next->next->next = new Node(9); */
/*     head2->next->next->next->next = new Node(4); */
/**/
/*     Node* result = alternate_merge(head1, head2); */
/**/
/*     printList(result); */
/**/
/*     return 0; */
/* } */

/* Task-5 end here */


/* Task-6 start here */


/* vector<int> check(1e6); */
/**/
/* struct Node{ */
/*     int data; */
/*     Node* next; */
/**/
/*     Node(int data){ */
/*         this->data=data; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/* int sum(Node* head,vector<int> &arr){ */
/*     int count=0,anscount=0,result=0; */
/**/
/*     while(head!=nullptr and anscount<arr.size()){ */
/**/
/*         if(check[count])result+=head->data*check[count],anscount+=check[count]; */
/*         head=head->next; */
/*         count++; */
/*     } */
/*     return result; */
/* } */
/**/
/**/
/* signed main(void){ */
/**/
/**/
/*     node* head=new node(10); */
/*     head->next=new node(16); */
/*     head->next->next=new node(-5); */
/*     head->next->next->next=new node(9); */
/*     head->next->next->next->next=new node(3); */
/*     head->next->next->next->next->next=new node(4); */
/**/
/**/
/*     vector<int> arr={2,0,5,2,8}; */
/*     for(auto &i:arr)check[i]++; */
/**/
/*     cout<<sum(head,arr)<<endl; */
/*     return 0; */
/* } */

/* Task-6 end here  */


/* Bonus Task start here */
/* struct Node{ */
/**/
/*     int data; */
/*     Node* next; */
/**/
/*     Node(int data){ */
/*         this->data=data; */
/*         this->next=nullptr; */
/*     } */
/* }; */
/**/
/**/
/* Node* reverse(Node* head){ */
/**/
/*     if(head->next==nullptr){ */
/*         return head; */
/*     } */
/**/
/*     Node* rest=reverse(head->next); */
/**/
/*     head->next->next=head; */
/*     head->next=nullptr; */
/*     return rest; */
/* } */
/**/
/**/
/* Node* idGenerator(Node *head1,Node *head2, Node *head3){ */
/**/
/*     Node *result=reverse(head1); */
/*     Node *temp=result; */
/**/
/*     int count=0; */
/*     while(count<3){ */
/*         result=result->next; */
/*         count++; */
/*     } */
/**/
/*     while(head2){ */
/**/
/*         result->next= new Node((head2->data+head3->data)%10); */
/*         head2=head2->next; */
/*         head3=head3->next; */
/*         result=result->next; */
/*     } */
/**/
/*     return temp; */
/* } */
/**/
/* void print(Node* head){ */
/**/
/*     while(head){ */
/*         cout<<head->data; */
/*         if(head->next)cout<<"->"; */
/*         head=head->next; */
/*     } */
/*     cout<<endl; */
/* } */
/**/
/**/
/* signed main(void){ */
/**/
/*     Node* head1 = new Node(0); */
/*     head1->next = new Node(3); */
/*     head1->next->next = new Node(2); */
/*     head1->next->next->next = new Node(2); */
/**/
/*     Node* head2 = new Node(5); */
/*     head2->next = new Node(2); */
/*     head2->next->next = new Node(2); */
/*     head2->next->next->next = new Node(1); */
/**/
/*     Node* head3 = new Node(4); */
/*     head3->next = new Node(3); */
/*     head3->next->next = new Node(2); */
/*     head3->next->next->next = new Node(1); */
/**/
/**/
/*     Node* head=idGenerator(head1,head2,head3); */
/*     print(head); */
/**/
/*     return 0; */
/* } */
 
/* Bonus Task end here */



