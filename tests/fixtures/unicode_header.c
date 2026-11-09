/* Copyright (c) 2017 Václav Slavík — contributors with non-ASCII names
   shift tree-sitter's byte offsets away from str indices. */
#include <stdio.h>
#define SQUARE(x) ((x) * (x))
static enum color_t { RED, GREEN } pick(int a, int b) { return a > b ? RED : GREEN; }
int add_numbers(int a, int b) { return SQUARE(a) + b; }
