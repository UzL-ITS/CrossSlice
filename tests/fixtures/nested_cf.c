int nested(int a, int n) {
    int s = 0;
    while (n > 0) {
        if (a > 0) {
            s = s + a;
        }
        n = n - 1;
    }
    return s;
}
