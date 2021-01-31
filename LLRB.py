class Node:
    def __init__(self, data):
        self.data = data
        self.left, self.right = None, None
        self.N, self.height = 1, 1
        # new node which is created is always red in color
        self.color = True # red = True, black = False

class LLRB_TREE:
    def __init__(self):
        self.root, self.temp = None, None
        self.print_line = True
        self.lst = []

    # function to rotate node anticlockwise
    def rotate_left(self, my_node):
        print("LEFT ROTATION")
        child = my_node.right
        child_left = child.left
        child.left = my_node
        my_node.right = child_left
        return child

    # function to rotate node clockwise
    def rotate_right(self, my_node):
        print("RIGHT ROTATION")
        child = my_node.left
        child_right = child.right
        child.right = my_node
        my_node.left = child_right
        return child

    def fix_up(self, h):
        if (self.is_red(h.right)):  h = self.rotate_left(h)
        if ((self.is_red(h.left) and (self.is_red(h.left.left)))):  h = self.rotate_right(h)
        if ((self.is_red(h.left) and (self.is_red(h.right)))):  self.colorFlip(h)
        return self.setN(h)

    def size(self, x):
        if (x == None): return 0
        else:   return x.N

    def height(self, x):
        if (x == None): return 0
        else:   return x.height

    def setN(self, h):
        h.N  = self.size(h.left) + self.size(h.right) + 1
        if (self.height(h.left) > self.height(h.right)):    h.height = self.height(h.left) + 1
        else:   h.height = self.height(h.right) + 1
        return h

    def del_min(self, h):
        if (h.left == None):    return None
        if ((not self.is_red(h.left) and (not self.is_red(h.left.left)))):    h = self.move_red_left(h)
        h.left = self.del_min(h.left)
        return self.fix_up(h)

    def min(self, x):
        if (x.left == None):    return x.data
        else:   return self.min(x.left)

    def colorFlip(self, my_node):
        my_node.color, my_node.right.color = not my_node.color, not my_node.right.color

    def move_red_left(self, my_node):
        self.colorFlip(my_node)
        if (self.is_red(my_node.right.left)):
            my_node.right = self.rotate_right(my_node.right)
            my_node = self.rotate_left(my_node)
            self.colorFlip(my_node)
        return my_node

    def move_red_right(self, my_node):
        self.colorFlip(my_node)
        if (self.is_red(my_node.left)):
            my_node = self.rotate_right(my_node)
            self.colorFlip(my_node)
        return my_node

    def get(self, x, key):
        if (x == None): return None
        if (key == x.data): return x.data
        if (key < x.data):  return self.get(x.left, key)
        else:   return self.get(x.right, key)

    # function to check whether node is red in color or not
    def is_red(self, my_node):
        if (my_node == None):   return False
        return (my_node.color == True)

    # function to swap color of two nodes
    def swap_colors(self, node_1, node_2):
        node_1.color, node_2.color = node_2.color, node_1.color

    def search(self, value):
        print(f'Yes, {value} exist in a tree.') if value in self.lst else print(f'No, {value} does not exist in a tree.')

    # insertion into LLRB Tree
    def insert(self, my_node, data):
        if (my_node == None):
            x = Node(data)
            print(f"{data} is inserted in the tree.")
            return x
        if (data < my_node.data):   my_node.left = self.insert(my_node.left, data)
        elif (data > my_node.data): my_node.right = self.insert(my_node.right, data)
        else:   return my_node

        # case 1: when right child is Red but left child is Black or doesn't exist
        if ((self.is_red(my_node.right) == True) and (self.is_red(my_node.left) == False)):
            my_node = self.rotate_left(my_node)
            self.swap_colors(my_node, my_node.left)

        # case 2: when left child as well as left grand child in Red
        if ((self.is_red(my_node.left) == True) and (self.is_red(my_node.left.left) == True)):
            my_node = self.rotate_right(my_node)
            self.swap_colors(my_node, my_node.right)

        # case 3:  when both left and right child are Red in color
        if ((self.is_red(my_node.left) == True) and (self.is_red(my_node.right) == True)):
            my_node.color = False if (my_node.color == True) else True
            my_node.left.color, my_node.right.color = False, False
        return my_node

    # inorder traversal
    def inorder(self, node):
        if (node != None):
            self.lst.append(node.data)
            color = 'Red' if node.color == True else 'Black'
            self.inorder(node.left)
            print(str(node.data) + ':' + color, end=' ')
            self.inorder(node.right)

    # preorder traversal
    def preorder(self, node):
        if (node != None):
            color = 'Red' if node.color == True else 'Black'
            print(str(node.data) + ':' + color, end=' ')
            self.preorder(node.left)
            self.preorder(node.right)

    def Delete(self, h, key):
        if key not in self.lst: print(f"{key} does not exist in a tree.")
        else:
            if (key < h.data):
                if (not self.is_red(h.left) and (not self.is_red(h.left.left))):    h = self.rotate_left(h)
                h.left = self.Delete(h.left, key)
            else:
                if (self.is_red(h.left)):   h = self.rotate_right(h)
                if ((key == h.data) and (h.right == None)): return None
                if (not self.is_red(h.right) and (not self.is_red(h.right.left))):  h = self.move_red_right(h)
                if (key == h.data):
                    h.value, h.data, h.right = self.get(h.right, self.min(h.right)), self.min(h.right), self.del_min(h.right)
                else:
                    h.right = self.Delete(h.right, key)
            if (self.print_line):
                print(f"{key} deleted from the tree.")
                self.print_line, self.temp = False, key
            if (self.temp != key):  self.print_line = True
            return self.fix_up(h)

node = LLRB_TREE()
root = node.root
root = node.insert(root, 10)
root.color = False # to make sure that root remains black in color
root = node.insert(root, 20)
root.color = False
root = node.insert(root, 30)
root.color = False
root = node.insert(root, 40)
root.color = False
root = node.insert(root, 50)
root.color = False
root = node.insert(root, 25)
root.color = False
print("INORDER:",end=' ')
node.inorder(root)
print("\nPREORDER:",end=' ')
node.preorder(root)
print('\n')
node.Delete(root, 25)
root.color = False
print("INORDER:",end=' ')
node.inorder(root)
print("\nPREORDER:",end=' ')
node.preorder(root)
print('\n')
node.search(1)
node.search(30)