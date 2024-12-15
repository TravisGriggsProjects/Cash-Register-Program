from LinkedList_Module import LinkedList
from Queue_Module import Queue
from Stack_Module import Stack
from Product import Product
from Sorting_Metrics import bubbleSort, insertionSort
import collections
import time
products = []



def init():
    file = open('products.txt', 'rt')
    for each_line in file:
        bar_code, name, desc,price = (each_line.strip()).split(',')
        products.append(Product(bar_code,name,desc,float(price)))

    file.close()

def linked_list_demo():
    #linked_list = collections.deque()
    linked_list = LinkedList()
    startTime = time.time() # gets start time
    for each_product in products:
        linked_list.add_first(each_product)
    endTime = time.time()
    runTime = float((endTime - startTime) *1000)
    print(f"The time to add 1000000 Product objects to LinkedList is {runTime} milli seconds")

def queue_demo():
    queue = Queue()
    startTime = time.time()  # gets start time
    for each_product in products:
        queue.enqueue(each_product)
    endTime = time.time()
    runTime = float((endTime - startTime) * 1000)
    print(f"The time to add 1000000 Product objects to queue is {runTime} milli seconds")


def stack_demo():
    stack = Stack()
    startTime = time.time()  # gets start time
    for each_product in products:
        stack.push(each_product)
    endTime = time.time()
    runTime = float((endTime - startTime) * 1000)
    print(f"The time to add 1000000 Product objects to stack is {runTime} milli seconds")

def bubble_sort_demo():
    print('Starting bubble sort......')
    startTime = time.time()  # gets start time
    bubbleSort(products)
    endTime = time.time()
    runTime = float((endTime - startTime) )
    print(f"The time to sort 1000000 Product objects using a Bubble Sort is {runTime} seconds")

def insertion_sort_demo():
    print('Starting insertion sort......')
    #startTime = time.time()  # gets start time
    insertionSort(products)
    #endTime = time.time()
    #runTime = float((endTime - startTime) )
    #print(f"The time to sort 10000 Product objects using a Insertion Sort is {runTime} seconds")

def linear_search_demo(bar_code):
    print('Starting linear search......')
    found = False
    startTime = time.time()  # gets start time
    for product in products:
        if product.get_barcode()== bar_code:
            endTime = time.time()
            runTime = float((endTime - startTime))
            print(f"The time to linear search a list of 1000000 Product objects is {runTime} seconds")
            return True
    endTime = time.time()
    runTime = float((endTime - startTime))
    print(f"The time to Linear search a list of  1000000 Product objects is {runTime} seconds")
    return False

def binary_search_demo(bar_code):
    print('Starting binary search...')
    products.sort(key=lambda x: x.get_barcode())
    start_time = time.time()
    low = 0
    high = len(products) - 1

    while low <= high:
        mid = (low + high) // 2
        if products[mid].get_barcode() == bar_code:
            end_time = time.time()
            run_time = float((end_time - start_time) * 1000)
            print(f"The time to Binary search a list of  1000000 Product objects is {run_time:.10f} milliseconds")
            return True
        elif products[mid].get_barcode() < bar_code:
            low = mid + 1
        else:
            high = mid - 1

    end_time = time.time()
    run_time = float((end_time - start_time) * 1000)
    print(f"Binary search took {run_time:.10f} milliseconds and did not find the product")
    return False

init()



linked_list_demo()
queue_demo()
stack_demo()
linear_search_demo('800000')
binary_search_demo('800000')


    
          
