void fields(struct S *s, int x) {
    s->field = x;
    *s->arr = x;
}
