#include <filesystem>
#include <iostream>
#include <vector>

#include "combinatorics.h"
#include "file.h"
#include "matroid.h"

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char** argv) {
    (void)argc;
    string repo_root =
        fs::canonical(argv[0]).parent_path().parent_path().string();

    // Initialize mappings between indices and sets,
    // and fill permutation array of size n! * C(n, r)
    initialize_combinatorics_mappings();
    initialize_combinatorics_tables();

    std::string combinatorics_file = repo_root + "/table/comb.bin";
    save_combinatorics(combinatorics_file);
    printf("Wrote %s\n", combinatorics_file.c_str());

    return 0;
}
