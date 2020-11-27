#include <stdio.h>
#include <stdlib.h>
#include "abTree.c"

int main()
{
    Tree *tree = initializeTree();
    printf("%p\n", tree);
    printf("tree->dummy->key: %f\n", tree->dummy->key);
    Leaf *child = (Leaf*)tree->r->c[B+1];
    printf("child->key: %f\n", child->key);
    return 0;
}
