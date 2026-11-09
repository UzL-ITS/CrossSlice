int shadow(int a) {
    int x = 1;
    {
        int x = 2;
        x = a;
    }
    x = 3;
    return x;
}
