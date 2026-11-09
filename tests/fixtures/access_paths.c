struct gb { int x; int size; };
struct ctx { struct gb gb; char *buf; int n; int y; struct ctx *next; };
struct val { int q; int r; };

int writes(struct ctx *s, int *len, int a[], struct val v, int i, int x) {
    *len = x;
    s->gb.x = 1;
    s->gb.x += 1;
    s->n++;
    (*s).y = 2;
    s[0].y = 3;
    a[i] = x;
    v.q = 2;
    s->next->n = 4;
    s->buf[i] = 'c';
    return 0;
}

int reads(struct ctx *s, int *len, int a[], struct val v, int i) {
    int x = a[i];
    int y = *len;
    int z = s->gb.x + (*s).gb.size;
    struct gb *g = &s->gb;
    int *q = &a[i];
    int w = *&x;
    int k = sizeof(s->gb);
    return v.q + s->next->n;
}

void calls(struct ctx *s, char *buf, int x, struct val v) {
    scanf("%d", &x);
    gets(buf);
    memcpy(s->buf + s->n, buf, 4);
    memset(s, 0, sizeof(*s));
    sscanf(buf, "%d", &s->n);
    init_get_bits(&s->gb, s->buf, 8);
    consume(s);
    consume(v);
    if (s == 0) return;
    if (s->gb.x > 0) return;
}

int out_param(int *len, int n) {
    *len = n;
    n = n + 1;
    return *len;
}

int field_flow(struct ctx *s, int n) {
    s->gb.x = n;
    s->y = 7;
    int a = s->gb.x;
    int b = s->y;
    int c = s->n;
    return a;
}

int whole_object(struct ctx *s, struct val v, struct val u) {
    v.q = 1;
    memset(s, 0, sizeof(*s));
    u = v;
    consume(s);
    int b = s->y;
    return u.q;
}

int buffer_flow(struct ctx *s, const char *src, int n) {
    memcpy(s->buf + s->n, src, n);
    s->n = n;
    init(s->buf);
    if (s->buf) return 1;
    return s->y;
}

int bare_pointer(struct ctx *s, int n) {
    s->n = n;
    if (s) n = 1;
    consume(s);
    return n;
}

int scanf_flow(int x) {
    int y = 0;
    scanf("%d", &x);
    y = x;
    return y;
}

int array_flow(int a[], int i, int j) {
    int before = a[j];
    a[i] = 1;
    int after = a[j];
    sum(a);
    return after;
}

int macro_tail(int i, int *listp, int p5s, int t) {
    LOCK(t, 0)i++;
    LOCK(1)listp = &p5s;
    return i;
}
