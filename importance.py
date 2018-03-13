import math
import random

class node():
    def __init__(self, value):
        self.value = value
        self.children = {}

    def print_Tree(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for key, node in self.children.items():
            ret += self.children[key].print_Tree(level+1)
        return ret


def decision_tree_learning(examples, attributes, parent_examples, random):
    if not examples:
        return node(plurality_value(parent_examples))
    elif not diff_class:
        return node(diff_class)
    elif not attributes:
        return node(plurality_value(examples))
    else:
        if random:
            best = random_importance(attributes)
        else:
            best = gain_importance(attributes, examples)
        tree = node(best)
        print(best)
        new_attribute = list(attributes)
        new_attribute.remove(best)
        for v in [1, 2]:
            new_example = []
            for example in examples:
                if int(example[best]) == v:
                    new_example.append(example)
            sub_tree = decision_tree_learning(new_example, new_attribute, examples, random)
            tree.children[v] = sub_tree
    return tree


def diff_class(examples):
    value = examples[0][7]
    for e in examples:
        if value != e[0][7]:
            return True
    return False


def plurality_value(examples):
    p_examples = 0
    n_examples = 0
    for example in examples:
        if int(example[7]) == 2:
            p_examples = p_examples + 1
        else:
            n_examples = n_examples + 1

    if p_examples > n_examples:
        return 2
    elif p_examples < n_examples:
        return 1
    return random.randint(1, 2)


def random_importance(attributes):
    return attributes[random.randint(0, len(attributes)-1)]

def count_positive(examples):
    p = 0
    for e in examples:
        if int(e[7]) == 2:
            p += 1
    return boolean_random(p / len(examples))

def gain_importance(attributes, examples):
    total_b = count_positive(examples)
    min = 1.1
    index = None
    for attribute in attributes:
        attributes_calculated = total_b - remainder(examples, attribute)
        if attributes_calculated < min:
            index = attribute
            min = attributes_calculated
    return index


def remainder(examples, attribute):
    p_count = []
    n_count = []
    for e in examples:
        if (int(e[attribute]) == 2):
            p_count.append(e)
        else:
            n_count.append(e)
    rem = (len(p_count) / len(examples)) * count_positive(p_count) + (len(n_count) / len(examples)) * count_positive(n_count)
    return rem


def calc_p_n_attr(examples, attribute, i):
    p, n = [0, 0]
    for e in examples:
        if int(e[attribute]) == i:
            if int(e[-1]) == 2:
                p += 1
            else:
                n += 1
    return [p, n]


def boolean_random(q):
    if 0 < q < 1:
        return -(q * math.log(q, 2) + (1-q)*math.log((1-q), 2))
    return 0


def classify(root, example):
    current = root
    while current.children:
        current = current.children[int(example[current.value])]
    return current.value


def run_tests(tree, examples):
    success = 0
    for example in examples:
        if example[-1] == classify(tree, example):
            success += 1
    print("Successfull tests = ", success, "/", len(examples)," (",success/len(examples)*100,"%)")

def start():
    examples = []
    test = []
    file = open("training.txt", 'r')
    file2 = open("test.txt", 'r')
    for line in file.readlines():
        examples.append(line.rstrip("\n").split("\t"))
    for line in file2.readlines():
        test.append(line.rstrip("\n").split("\t"))

    node = decision_tree_learning(examples, list(range(0, len(examples[0]) - 1)), [], False)
    print(node.print_Tree())
    run_tests(node, test)
start()

