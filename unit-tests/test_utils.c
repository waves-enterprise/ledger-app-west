#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include <cmocka.h>

#include "utils.h"

static void test_copy_in_reverse_order(void** state) {
    (void)state;

    const char* in = "The quick brown fox jumps over the lazy dog.";
    const char* expected_out = ".god yzal eht revo spmuj xof nworb kciuq ehT";
    char out[100] = {0};

    copy_in_reverse_order((unsigned char*)out, (const unsigned char*)in, strlen(in));
    assert_string_equal(out, expected_out);
}

int main() {
    const struct CMUnitTest tests[] = {cmocka_unit_test(test_copy_in_reverse_order)};

    return cmocka_run_group_tests(tests, NULL, NULL);
}
