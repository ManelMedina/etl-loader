#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int i=0;
    int rate=1000;
    char line[10000];

    // screw segfaults, I don't care
    if (argv[1][1] == 'h') {
        fprintf(stderr, "syntax: %s [-h] [-n sample_rate] < input.txt > output.txt \n", argv[0]);
        return 0;
    }
    else if (argv[1][1] == 'n') {
        rate = atoi(argv[2]);
    }
    while (NULL != fgets(line, sizeof(line)-1, stdin)) {
        if (!(i%rate)) {
            fprintf(stdout, line);
        }
        i++;
    }
    return 0;
}
