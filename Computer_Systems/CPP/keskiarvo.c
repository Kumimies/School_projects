/*Funktio etsii pilkulla erotettujen kokonaislukujen keskiarvon*/

#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

float keskiarvo(char *lista);

int main(){
    char lista[] = "201,53,12,31,5"; 
    printf("%f\n", keskiarvo(lista));
    return 0;
}

float keskiarvo(char *lista){
    const char sep[] = ",";
    char *token;
    token = strtok(lista, sep);

    float summa = 0;
    int lkm = 0;

    while( token != NULL ) {
        float luku = atof(token);
        summa += luku;
        lkm++;
        token = strtok(NULL, sep);
    }
    return summa / lkm;
}