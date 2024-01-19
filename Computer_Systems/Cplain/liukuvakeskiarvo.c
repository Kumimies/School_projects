/*Tämä ohjelma laskee liukuvan keskiarvon annetulle taulukolle*/
/*Esim nyt window_size on 3 eli ensiksi lasketaan keskiarvo arvoista 1.0, 2.0 ja 4.0*/
/*seuraavalla iteraatiolla arvoista 2.0, 4.0 ja 6.0 ja lopuksi arvoista 4.0, 6.0 ja 9.0*/
#include <stdio.h>
#include <stdint.h>

void movavg(float *array, uint8_t array_size, uint8_t window_size);

int main() {
    float data[5] = { 1.0, 2.0, 4.0, 6.0, 9.0 };
    movavg(data, 5, 3);
    return 0;
}

void movavg(float *array, uint8_t array_size, uint8_t window_size) {
    float sum;
    for (int i = 0; i <= array_size - window_size; i++) {
        sum = 0.0;
        for (int j = i; j < i + window_size; j++) {
            sum += array[j];
        }
        printf("%.2f", sum / window_size);
        if (i != array_size - window_size) {
            printf(",");
        }
    }
}