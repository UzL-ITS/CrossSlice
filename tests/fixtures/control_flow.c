int control(int a, int b) {
    int r = 0;
    if (a > b) {
        r = a;
    } else {
        r = b;
    }
    while (r > 0) {
        r = r - 1;
    }
    return r;
}
