#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'



/* Task-1 start here */
/* struct Node { */
/*     int data; */
/*     Node* left; */
/*     Node* right; */
/*     Node(int val){ */
/*         this->data=val; */
/*         this->left=nullptr; */
/*         this->right=nullptr; */
/*     } */
/* }; */
/**/
/* void mirror(Node* root) { */
/*     if (root == nullptr) return; */
/*     swap(root->left, root->right); */
/*     mirror(root->left); */
/*     mirror(root->right); */
/* } */
/**/
/* void inorderTraversal(Node* root) { */
/*     if (root == nullptr) return; */
/*     inorderTraversal(root->left); */
/*     cout << root->data << " "; */
/*     inorderTraversal(root->right); */
/* } */
/**/
/* signed main(void) { */
/*     Node* root = new Node(10); */
/*     root->left = new Node(20); */
/*     root->right = new Node(30); */
/*     root->left->left = new Node(40); */
/*     root->left->right = new Node(60); */
/**/
/*     mirror(root); */
/**/
/*     inorderTraversal(root); */
/*     cout << endl; */
/**/
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */

/* struct Node{ */
/*     int data; */
/*     Node* left,*right; */
/**/
/*     Node(int val){ */
/*         this->data=val; */
/*         this->left=nullptr,this->right=nullptr; */
/*     } */
/* }; */
/**/
/**/
/* vector<int> levelMin(Node *root){ */
/*     queue<Node*> q; */
/*     q.push(root); */
/*     vector<int> ans; */
/**/
/*     while(!q.empty()){ */
/*         int size=q.size(); */
/*         int curMin=INT_MAX; */
/*         for(int i=0;i<size;i++){ */
/*             Node* node=q.front(); */
/*             q.pop(); */
/**/
/*             curMin=min(curMin,node->data); */
/*             if(node->left)q.push(node->left); */
/*             if(node->right)q.push(node->right); */
/*         } */
/*         ans.push_back(curMin); */
/*     } */
/*     return ans; */
/* } */
/**/
/**/
/* signed main(void) { */
/*     Node* root = new Node(4); */
/*     root->left = new Node(9); */
/*     root->right = new Node(2); */
/*     root->left->left = new Node(3); */
/*     root->right->right = new Node(7); */
/*     root->right->left = new Node(-5); */
/**/
/*     vector<int> result = levelMin(root); */
/**/
/*     for (int val : result) { */
/*         cout << val << " "; */
/*     } */
/*     cout << endl; */
/**/
/*     return 0; */
/* } */
/**/
/* Task-2 end here */


/* Task-3 start here */

/* struct Node { */
/*     int data; */
/*     Node* left; */
/*     Node* right; */
/*     Node(int val){ */
/*         this->data=val; */
/*         this->left=nullptr; */
/*         this->right=nullptr; */
/*     } */
/* }; */
/**/
/* int calculateSum(Node* root) { */
/*     if (root == nullptr) return 0; */
/**/
/*     queue<pair<Node*, int>> q; */
/*     q.push({root, 0}); */
/*     int totalSum = 0; */
/**/
/*     while (!q.empty()) { */
/*         auto [node, level] = q.front(); */
/*         q.pop(); */
/**/
/*         if (level == 0) { */
/*             totalSum += node->data;  */
/*         } else { */
/*             totalSum += node->data % level;  */
/*         } */
/**/
/*         if (node->left) q.push({node->left, level + 1}); */
/*         if (node->right) q.push({node->right, level + 1}); */
/*     } */
/**/
/*     return totalSum; */
/* } */
/**/
/**/
/* signed main(void) { */
/*     Node* root = new Node(9); */
/*     root->left = new Node(4); */
/*     root->right = new Node(5); */
/*     root->left->left = new Node(18); */
/*     root->left->right = new Node(14); */
/*     root->right->left = new Node(3); */
/*     root->left->left->left = new Node(54); */
/*     root->left->left->right = new Node(12); */
/*     root->right->left->left = new Node(8); */
/*     root->left->left->left->left = new Node(91); */
/*     root->left->left->left->right = new Node(56); */
/**/
/*     int result = calculateSum(root); */
/**/
/*     cout << result << endl; */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */


/* Task-4 start here */

/* struct Node { */
/*     char data; */
/*     Node* left; */
/*     Node* right; */
/**/
/*     Node(char val){ */
/*         data=val; */
/*         left=nullptr; */
/*         right=nullptr; */
/*     } */
/* }; */
/**/
/* void swap_child(Node* root, int level, int M) { */
/*     if (root == nullptr) return; */
/*     if (level < M) { */
/*         swap(root->left, root->right); */
/*     } */
/*     swap_child(root->left, level + 1, M); */
/*     swap_child(root->right, level+1, M); */
/* } */
/**/
/* void inorderTraversal(Node* root) { */
/*     if (root == nullptr) return; */
/*     inorderTraversal(root->left); */
/*     cout << root->data << " "; */
/*     inorderTraversal(root->right); */
/* } */
/**/
/* signed main(void) { */
/*     Node* root = new Node('A'); */
/*     root->left = new Node('B'); */
/*     root->right = new Node('C'); */
/*     root->left->left = new Node('D'); */
/*     root->left->right = new Node('E'); */
/*     root->right->right=new Node('F'); */
/*     root->left->left->left=new Node('G'); */
/*     root->left->left->right=new Node('H'); */
/*     root->left->right->left=new Node('I'); */
/*     root->right->right->left=new Node('J'); */
/**/
/*     int M = 2; */
/*     swap_child(root, 0, M); */
/**/
/*     inorderTraversal(root); */
/*     cout << endl; */
/**/
/* } */
/* Task-4 end here */

/* Task-6 start here */
struct Node {
    int elem;
    Node* left;
    Node* right;

    Node(int val) {
        elem = val;
        left = nullptr;
        right = nullptr;
    }
};

int difference_of_level_sum(Node* root, int level) {
    if (root == nullptr) return 0;

    if (level % 2 != 0) {
        return root->elem + difference_of_level_sum(root->left, level + 1) + difference_of_level_sum(root->right, level + 1);
    }
    else {
        return -root->elem + difference_of_level_sum(root->left, level + 1) + difference_of_level_sum(root->right, level + 1);
    }
}


signed main(void) {
    Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);
    root->right->left = new Node(5);
    root->right->right = new Node(6);
    root->right->left->left = new Node(7);
    root->right->left->right = new Node(8);

    int result = difference_of_level_sum(root, 0);

    cout << result << endl;

    return 0;
}

/* Task-5 end here */






