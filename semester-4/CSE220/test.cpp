#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

TreeNode* removeNegativeNodes(TreeNode* root) {
    if (!root) return nullptr;

    root->left = removeNegativeNodes(root->left);
    root->right = removeNegativeNodes(root->right);

    if (root->val < 0) {
        TreeNode* newRoot = root->left ? root->left : root->right;
        delete root;
        return newRoot;
    }

    return root;
}

void inorderTraversal(TreeNode* root) {
    if (!root) return;
    inorderTraversal(root->left);
    std::cout << root->val << " ";
    inorderTraversal(root->right);
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left=new TreeNode(-1);
    root->right=new TreeNode(3);
    root->left->left=new TreeNode(5);
    root->left->right=new TreeNode(6);
    root->left->left->left=new TreeNode(10);
    root->left->left->right=new TreeNode(10);


    std::cout << "Original tree (inorder traversal): ";
    inorderTraversal(root);
    std::cout << std::endl;

    root = removeNegativeNodes(root);

    std::cout << "Tree after removing negative nodes (inorder traversal): ";
    inorderTraversal(root);
    std::cout << std::endl;

    return 0;
}
