#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#include "LinkedList.c"

#define A 2
#define B 4


typedef struct Node
{
    int d;          // degree
    float s[B-1];   // splitters
    void *c[B];      // children - void pointer to be compatible with Nodes and Leafs
}Node;

typedef struct Tree
{
    unsigned int height;
    Leaf *dummy;    // dummy item of the list, access to list
    Node *r;        // root
}Tree;


/* Initializing an (a,b)-tree at the returned pointer. */
Tree* initializeTree()
{
    Leaf *list         = initializeList();

    Tree *tree   = (Tree*)malloc(sizeof(Tree));
    tree->dummy  = list;
    tree->height = 1;

    Node *root   = (Node*)malloc(sizeof(Node));
    tree->r      = root;

    root->d      = 1;
    root->c[B+1] = (void*)list;

    printf("Tree initialized at %p\n", tree);

    return tree;
}

int locateLocally(float k, float s[B-1]) // k=key, s=splitters
{
    for(int i=0;(i < B);++i)
    {
        if ((s[i]>k) && (i>0))
        {
            return i-1;
        }
        else if (s[i]>k)
        {
            printf("Couldn't locate locally\n");
        }
    }
    return B+1;
}

locateRec(float k, int h) // k=key, h=height
{
    int i = locateLocally(k, )
}
