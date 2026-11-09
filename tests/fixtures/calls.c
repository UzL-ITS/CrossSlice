void calls(int a, char *buf, int n) {
    int y;
    y = compute(a, 5);
    fgets(buf, n, stdin);
    scanf("%d", &a);
    printf("%d", y);
}
