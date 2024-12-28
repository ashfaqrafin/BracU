#include <bits/stdc++.h>
using namespace std;
#define endl '\n'


/* Task-1 start here */
/* class MinHeap { */
/*     private: */
/*         vector<int> heap; */
/*         int size; */
/*         int capacity; */
/**/
/*         void swim(int idx) { */
/*             while (idx > 0 && heap[(idx - 1)>>1] > heap[idx]) { */
/*                 swap(heap[(idx - 1)>>1], heap[idx]); */
/*                 idx = (idx - 1) >> 1; */
/*             } */
/*         } */
/**/
/*         void sink(int idx) { */
/*             while (2 * idx + 1 < size) { */
/*                 int j = 2 * idx + 1; */
/*                 if (j + 1 < size && heap[j + 1] < heap[j]) { */
/*                     j++; */
/*                 } */
/*                 if (heap[idx] <= heap[j]) { */
/*                     break; */
/*                 } */
/*                 swap(heap[idx], heap[j]); */
/*                 idx = j; */
/*             } */
/*         } */
/**/
/*     public: */
/*         MinHeap(int capacity) : size(0), capacity(capacity) { */
/*             heap.resize(capacity); */
/*         } */
/**/
/*         void insert(int value) { */
/*             if (size == capacity) { */
/*                 throw overflow_error("Heap is full"); */
/*             } */
/*             heap[size] = value; */
/*             swim(size); */
/*             size++; */
/*         } */
/**/
/*         int extractMin() { */
/*             if (size == 0) { */
/*                 throw underflow_error("Heap is empty"); */
/*             } */
/*             int min = heap[0]; */
/*             heap[0] = heap[--size]; */
/*             sink(0); */
/*             return min; */
/*         } */
/**/
/*         void sort() { */
/*             int orSize = size; */
/*             for (int i = size - 1; i > 0; i--) { */
/*                 swap(heap[0], heap[i]); */
/*                 size--; */
/*                 sink(0); */
/*             } */
/*             size = orSize; */
/*         } */
/**/
/*         void printHeap() { */
/*             for (int i = 0; i < size; i++) { */
/*                 cout << heap[i] << " "; */
/*             } */
/*             cout << endl; */
/*         } */
/* }; */
/**/
/* int main() { */
/*     MinHeap minHeap(10); */
/*     minHeap.insert(3); */
/*     minHeap.insert(1); */
/*     minHeap.insert(6); */
/*     minHeap.insert(5); */
/*     minHeap.insert(2); */
/*     minHeap.insert(4); */
/**/
/*     cout << "Heap elements: "; */
/*     minHeap.printHeap(); */
/**/
/*     cout << "Extracted min: " << minHeap.extractMin() << endl; */
/**/
/*     cout << "Heap elements after extraction: "; */
/*     minHeap.printHeap(); */
/**/
/*     minHeap.sort(); */
/*     cout << "Heap elements after sorting: "; */
/*     minHeap.printHeap(); */
/**/
/*     return 0; */
/* } */
/* Task-1 end here */


/* Task-2 start here */
/* class MaxHeap { */
/*     private: */
/*         vector<int> heap; */
/*         int size; */
/*         int capacity; */
/*         void swim(int idx) { */
/*             while (idx > 0 && heap[(idx - 1) / 2] < heap[idx]) { */
/*                 swap(heap[(idx - 1) / 2], heap[idx]); */
/*                 idx = (idx - 1) / 2; */
/*             } */
/*         } */
/*         void sink(int idx) { */
/*             while (2 * idx + 1 < size) { */
/*                 int j = 2 * idx + 1; */
/*                 if (j + 1 < size && heap[j + 1] > heap[j]) { */
/*                     j++; */
/*                 } */
/*                 if (heap[idx] >= heap[j]) { */
/*                     break; */
/*                 } */
/*                 swap(heap[idx], heap[j]); */
/*                 idx = j; */
/*             } */
/*         } */
/*     public: */
/*         MaxHeap(int capacity) : size(0), capacity(capacity) { */
/*             heap.resize(capacity); */
/*         } */
/*         void insert(int value) { */
/*             if (size == capacity) { */
/*                 throw overflow_error("Heap is full"); */
/*             } */
/*             heap[size] = value; */
/*             swim(size); */
/*             size++; */
/*         } */
/*         int extractMax() { */
/*             if (size == 0) { */
/*                 throw underflow_error("Heap is empty"); */
/*             } */
/*             int max = heap[0]; */
/*             heap[0] = heap[--size]; */
/*             sink(0); */
/*             return max; */
/*         } */
/**/
/*         void sort() { */
/*             int originalSize = size; */
/*             for (int i = size - 1; i > 0; i--) { */
/*                 swap(heap[0], heap[i]); */
/*                 size--; */
/*                 sink(0); */
/*             } */
/*             size = originalSize; */
/*         } */
/**/
/*         void printHeap() { */
/*             for (int i = 0; i < size; i++) { */
/*                 cout << heap[i] << " "; */
/*             } */
/*             cout << endl; */
/*         } */
/* }; */
/**/
/* int main() { */
/*     MaxHeap maxHeap(10); */
/*     maxHeap.insert(3); */
/*     maxHeap.insert(1); */
/*     maxHeap.insert(6); */
/*     maxHeap.insert(5); */
/*     maxHeap.insert(2); */
/*     maxHeap.insert(4); */
/**/
/*     cout << "Heap elements: "; */
/*     maxHeap.printHeap(); */
/**/
/*     cout << "Extracted max: " << maxHeap.extractMax() << endl; */
/**/
/*     cout << "Heap elements after extraction: "; */
/*     maxHeap.printHeap(); */
/**/
/*     maxHeap.sort(); */
/*     cout << "Heap elements after sorting: "; */
/*     maxHeap.printHeap(); */
/**/
/*     return 0; */
/* } */

/* Task-2 end here */



/* Task-3 start here */

/* vector<int> distributeTasks(const vector<int>& tasks, int m) { */
/*     priority_queue<int, vector<int>, greater<int>> minHeap; */
/**/
/*     for (int i = 0; i < m; i++) { */
/*         minHeap.push(0); */
/*     } */
/**/
/*     for (int task : tasks) { */
/*         int minLoad = minHeap.top(); */
/*         minHeap.pop(); */
/*         minLoad += task; */
/*         minHeap.push(minLoad); */
/*     } */
/**/
/*     vector<int> result(m); */
/*     for (int i = 0; i < m; i++) { */
/*         result[i] = minHeap.top(); */
/*         minHeap.pop(); */
/*     } */
/**/
/*     return result; */
/* } */
/**/
/* int main() { */
/*     vector<int> tasks = {2, 4, 7, 1, 6}; */
/*     int m = 4; */
/**/
/*     vector<int> result = distributeTasks(tasks, m); */
/**/
/*     cout << "Final loads of machines: "; */
/*     for (int load : result) { */
/*         cout << load << " "; */
/*     } */
/*     cout << endl; */
/**/
/*     return 0; */
/* } */
/* Task-3 end here */



/* Task-4 start here */
/**/
/* vector<int> findTopKLargest(const vector<int>& nums, int k) { */
/*     priority_queue<int> maxHeap(nums.begin(), nums.end()); */
/*     vector<int> result; */
/*     for (int i = 0; i < k; i++) { */
/*         result.push_back(maxHeap.top()); */
/*         maxHeap.pop(); */
/*     } */
/**/
/*     return result; */
/* } */
/**/
/* int main() { */
/*     vector<int> nums = {4, 10, 2, 8, 6, 7}; */
/*     int k = 3; */
/**/
/*     vector<int> result = findTopKLargest(nums, k); */
/**/
/*     cout << "Top " << k << " largest elements: "; */
/*     for (int i : result) { */
/*         cout << i << " "; */
/*     } */
/*     cout << endl; */
/**/
/*     return 0; */
/* } */
/* Task-4 end here */

