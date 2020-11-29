from multiprocessing import Process, cpu_count


def bulkInsert(self, elements=[()], k=cpu_count):
    if k == 1:
        for element in elements:
            if len(element) > 1:
                self.insert(element[0], element[1])
            else:
                self.insert(element[0])
    else:
