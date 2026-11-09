void scopes(int a) {
    {
        int t = a;
        a = t;
    }
    {
        int t = 5;
        int u = t;
    }
}
