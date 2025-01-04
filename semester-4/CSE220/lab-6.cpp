#include <bits/stdc++.h>
using namespace std;
/* #define int long long */
#define endl '\n'


/* Task-1 start here */
/* struct Node{ */
/*     int data; */
/*     Node *left,*right; */
/**/
/*     Node(int val){ */
/*         data=val; */
/*         left=nullptr; */
/*         right=nullptr; */
/*     } */
/* }; */
/**/
/* Node* insert(Node* root,int data){ */
/*     if(!root)return new Node(data); */
/**/
/*     if(data<root->data)root->left=insert(root->left,data); */
/*     else root->right=insert(root->right,data); */
/*     return root; */
/* } */
/**/
/* Node* LCA(Node* root,int n1,int n2){ */
/*     if(!root)return nullptr; */
/**/
/*     if(root->data>n1 && root->data>n2)return LCA(root->left,n1,n2); */
/*     if(root->data<n1 && root->data<n2)return LCA(root->right,n1,n2); */
/*     return root; */
/* } */
/**/
/* signed main(void){ */
/**/
/**/
/*     Node *root=new Node(15); */
/*     insert(root, 10); */
/*     insert(root, 25); */
/*     insert(root, 8); */
/*     insert(root, 12); */
/*     insert(root, 20); */
/*     insert(root, 30); */
/*     insert(root, 6); */
/*     insert(root, 9); */
/*     insert(root, 18); */
/*     insert(root, 22); */
/**/
/*     cout<<LCA(root,6,12)->data<<endl; */
/*     cout<<LCA(root,20,6)->data<<endl; */
/*     cout<<LCA(root,18,22)->data<<endl; */
/*     cout<<LCA(root,20,25)->data<<endl; */
/*     cout<<LCA(root,10,12)->data<<endl; */
/**/
/**/
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */

/* struct Node{ */
/*     int data; */
/*     Node *left,*right; */
/**/
/*     Node(int val){ */
/*         data=val; */
/*         left=nullptr; */
/*         right=nullptr; */
/*     } */
/* }; */
/**/
/* Node* insert(Node* root,int data){ */
/*     if(!root)return new Node(data); */
/**/
/*     if(data<root->data)root->left=insert(root->left,data); */
/*     else root->right=insert(root->right,data); */
/*     return root; */
/* } */
/**/
/**/
/* bool find_path(Node* root,vector<int> &path,int key){ */
/*     while(root){ */
/**/
/*         path.push_back(root->data); */
/*         if(key==root->data)return true; */
/*         if(key<root->data)root=root->left; */
/*         else root=root->right; */
/*     } */
/*     return false; */
/* } */
/**/
/* signed main(void){ */
/**/
/*     Node *root=new Node(30); */
/*     insert(root,10); */
/*     insert(root,40); */
/*     insert(root,3); */
/*     insert(root,15); */
/*     insert(root,35); */
/*     insert(root,55); */
/**/
/*     vector<int> path; */
/**/
/*     if(find_path(root,path,15)){ */
/*         for(auto &i:path)cout<<i<<" "; */
/*         cout<<endl; */
/*     }else cout<<"No path found"<<endl; */
/**/
/*     return 0; */
/* } */
/* Task-2 end here */


/* Task-3 start here */
/* struct Node{ */
/*     int data; */
/*     Node *left,*right; */
/**/
/*     Node(int val){ */
/*         data=val; */
/*         left=nullptr; */
/*         right=nullptr; */
/*     } */
/* }; */
/* Node* insert(Node* root,int data){ */
/*     if(!root)return new Node(data); */
/**/
/*     if(data<root->data)root->left=insert(root->left,data); */
/*     else root->right=insert(root->right,data); */
/*     return root; */
/* } */
/**/
/**/
/* int sum_of_leaves(Node *root){ */
/*     if(!root)return 0; */
/*     if(!root->left && !root->right)return root->data; */
/**/
/*     return sum_of_leaves(root->left)+sum_of_leaves(root->right); */
/* } */
/**/
/**/
/* signed main(void){ */
/**/
/*     Node *root=new Node(30); */
/*     insert(root,10); */
/*     insert(root,40); */
/*     insert(root,3); */
/*     insert(root,15); */
/*     insert(root,35); */
/*     insert(root,55); */
/*     insert(root,2); */
/*     insert(root,36); */
/**/
/*     cout<<sum_of_leaves(root)<<endl; */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */


/* Task-4 start here */
struct Node{
    int data;
    Node *left,*right;

    Node(int val){
        data=val;
        left=nullptr;
        right=nullptr;
    }
};

Node* insert(Node* root,int data){
    if(!root)return new Node(data);

    if(data<root->data)root->left=insert(root->left,data);
    else root->right=insert(root->right,data);
    return root;
}



Node* in_order_predecessor(Node* root, Node* x) {
    Node* predecessor = NULL;

    while (root != NULL) {
        if (x->data <= root->data) {
            root = root->left;
        } else {
            predecessor = root;
            root = root->right;
        }
    }
    return predecessor;
}


int main() {
    Node* root = new Node(20);
    insert(root, 8);
    insert(root, 22);
    insert(root, 4);
    insert(root, 12);
    insert(root, 10);
    insert(root, 14);

    Node* node = root->left->right->left; 
    Node* predecessor = in_order_predecessor(root, node);
    cout<<predecessor->data<<endl;

    return 0;
}
/* Task-4 end here */
