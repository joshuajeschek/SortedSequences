from multiprocessing import cpu_count, Pool, Process, Manager


def bulkInsert(self, elements=[()], k=cpu_count, return_list):
    if k == 1:
        for element in elements:
            if len(element) > 1:
                self.insert(element[0], element[1])
            else:
                self.insert(element[0])
        return_list.append(self)

    else:
        m = len(elements) // 2
        Tree1, Tree2 = self.split(elements[m][0])
        return_1 = Manager().list()
        return_2 = Manager().list()
        p1 = Process(target=Tree1.bulkInsert, args=(
            elements[:m], k // 2, return_1))
        p2 = Process(target=Tree2.bulkInsert, args=(
            elements[m:], k // 2, return_2))
        print(return_1)
        print(return_2)
        return mergeTrees(Tree1, Tree2)
