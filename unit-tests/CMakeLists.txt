cmake_minimum_required(VERSION 3.10)

if(${CMAKE_VERSION} VERSION_LESS 3.10)
    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION})
endif()

# project information
project(unit_tests
        VERSION 0.1
	      DESCRIPTION "Unit tests for Ledger Nano application"
        LANGUAGES C)


# guard against bad build-type strings
if (NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug")
endif()

include(CTest)
ENABLE_TESTING()

# specify C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wall -pedantic -g -O0 --coverage")

set(GCC_COVERAGE_LINK_FLAGS "--coverage -lgcov")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")

# guard against in-source builds
if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
  message(FATAL_ERROR "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there. You may need to remove CMakeCache.txt. ")
endif()

add_compile_definitions(TEST)

include_directories(../src)

add_executable(test_base58 test_base58.c)
add_executable(test_ed25519 test_ed25519.c)
add_executable(test_utils test_utils.c)

add_library(base58 STATIC ../src/crypto/base58.c)
add_library(ed25519 STATIC  ../src/sodium/keypair.c ../src/sodium/private/ed25519_ref10_fe_25_5.c ../src/sodium/private/ed25519_ref10.c ../src/sodium/private/fe_25_5/fe.c)
add_library(utils STATIC  ../src/utils.c)

target_link_libraries(test_base58 PUBLIC cmocka gcov base58)
target_link_libraries(test_ed25519 PUBLIC cmocka gcov ed25519)
target_link_libraries(test_utils PUBLIC cmocka gcov utils)

add_test(test_base58 test_base58)
add_test(test_ed25519 test_ed25519)
add_test(test_utils test_utils)
