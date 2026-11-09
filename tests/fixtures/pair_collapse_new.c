int f(state_t *state) {
    if (state->skip && gz_zero(state) == -1)
        return state->err;
    return 0;
}
