/*Palauttaa luvun kertoman. Luvun maksimiarvo 20, muuten palauttaa -1*/
#include <stdio.h>
#include <inttypes.h>

int64_t laske_kertoma(int8_t n);

int main(void){
    int64_t lasku = laske_kertoma(3);
    printf("%" PRId64 "\n", lasku);    
    return 0;
}

int64_t laske_kertoma(int8_t n){
    int64_t tulos = 1;
    if (n <= 20){
        for (int8_t i = 1; i <= n; i++){
            tulos = tulos * i;
        }
    }
    else{
        tulos = -1;
    }
    return tulos;
}