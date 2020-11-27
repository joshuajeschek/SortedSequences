#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

typedef struct Leaf
{
    float key;
    float value;
    struct Leaf *next;
    struct Leaf *prev;
}Leaf;

/* initializing a list with only the dummy item, which also points at itself */
Leaf* initializeList()
{
    Leaf *dummy  = (Leaf*)malloc(sizeof(Leaf));
    dummy->key   = INFINITY;
    dummy->value = 0;
    dummy->next  = dummy;
    dummy->prev  = dummy;
    printf("Initialized list at %p\n", dummy);
    return dummy;
}

/* Locates a Leaf with a given key and returns its pointer */
Leaf* llocate(float key, Leaf *list)
{
    Leaf *current = list->next;
    while (current->key <= key)
    {
        // printf("current key: %f\n", current->key);
        current = current->next;
    }
    current = current->prev;
    // printf("Found leaf with key %f\n", current->key);
    return current;
}

/* Inserts Leaf with at given key */
void insert(float key, float value, Leaf *list)
{
    Leaf *target = llocate(key, list);
    if (target->key == key)
    {
        // printf("Overwriting value of at %p\n", target);
        target->value = value;
    }
    else
    {
        Leaf *new    = (Leaf*)malloc(sizeof(Leaf));
        new->key     = key;
        new->value   = value;
        new->prev    = target;
        new->next    = target->next;
        target->next = new;
        Leaf *next   = new->next;
        next->prev   = new;
    }
}

/* Deletes the whole list, including the dummy item (free()) */
void deleteList(Leaf *list)
{
    Leaf *current = list->next;
    while(current != list)
    {
        // printf("Freeing %p\n", current);
        free(current);
        current = current->next;
    }
    // printf("Freeing dummy %p\n", list);
    free(list);
}

/*deletes a single Leaf with the given key, if existent. */
void deleteLeaf(float key, Leaf *list)
{
    Leaf *target = llocate(key, list);
    if (target->key == key)
    {
        // printf("Deleting %p\n", target);
        target->prev->next = target->next;
        target->next->prev = target->prev;
        free(target);
    }
    else
    {
        // printf("Did not find a leave with key %f\n", key);
    }
}

/* lists all Leafs of the given list, with their keys, values and pointers through printf() */
void listAll(Leaf *list)
{
    Leaf *current = list->next;
    while (current != list)
    {
        printf("%f : %f\ta:%p p:%p n:%p\n", current->key, current->value, current, current->prev, current->next);
        current = current->next;
    }
}

/* returns the value corresponding to the given key. If the key is non-existent, returns INF */
float getValue(float key, Leaf *list)
{
    Leaf *target = llocate(key, list);
    if (target->key == key)
    {
        return target->value;
    }
    else
    {
        return INFINITY;
    }
}

/* returns first leaf of list */
Leaf* first(Leaf *list)
{
    return list->next;
}

/* returns last leaf of list */
Leaf* last(Leaf *list)
{
    return list->prev;
}

bool isEmpty(Leaf *list)
{
    if (list->next == list)
    {
        return true;
    }
    return false;
}
