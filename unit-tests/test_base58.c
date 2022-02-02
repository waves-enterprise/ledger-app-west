#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include <cmocka.h>

#include "crypto/base58.h"

static void test_base58(void** state) {
    (void)state;

    const char* in = "The quick brown fox jumps over the lazy dog.";
    const char* expected_out = "USm3fpXnKG5EUBx2ndxBDMPVciP5hGey2Jh4NDv6gmeo1LkMeiKrLJUUBk6Z";
    char out[100] = {0};
    size_t out_len = sizeof(out);
    bool ret = false;

    ret = b58enc(out, &out_len, in, strlen(in));
    assert_true(ret);
    assert_int_equal(out_len, strlen(expected_out) + 1);
    assert_string_equal(expected_out, out);
}

int main() {
    const struct CMUnitTest tests[] = {cmocka_unit_test(test_base58)};

    return cmocka_run_group_tests(tests, NULL, NULL);
}
