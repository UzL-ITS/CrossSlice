int f(int *fd_ptr, char *alias, int alias_len)
{
    int rc = phar_free_alias(*fd_ptr, alias, alias_len TSRMLS_CC);
    phar_set_inode(entry TSRMLS_CC);
    return rc;
}
