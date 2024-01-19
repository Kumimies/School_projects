/*funktio joka laskee merkkijonon vokaalit ja konsonantit ja */
/*sijoittaa tulokset osoittimena annettuun taulukkoon.*/

#include <string.h>
#include <stdint.h>
#include <stdio.h>

void merkkilaskuri(char *str, uint8_t *tulos);

int main()
{
    // Testattava merkkijono str
    char str[] = "Hei, tämä on testimerkkijono!";
    uint8_t tulos[2];

    merkkilaskuri(str, tulos);

    printf("Vokaaleja: %d\n", tulos[0]);
    printf("Konsonantteja: %d\n", tulos[1]);

    return 0;
}

void merkkilaskuri(char *str, uint8_t *tulos)
{
    // Alkuun ei ole tuloksia, alustetaan.
    tulos[0] = 0; // vokaalit
    tulos[1] = 0; // konsonantit

    // Määritellään vokaalit ja konsonantit
    char vokaalit[] = "aeiouyåäöAEIOUYÅÄÖ";
    char konsonantit[] = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ";

    // Käydään läpi merkkijono
    for (int i = 0; str[i] != '\0'; i++)
    {
        // Strchr avulla katsotaan onko str[i] kohdalla vokaali
        if (strchr(vokaalit, str[i]) != NULL)
        {
            tulos[0]++; // Jos merkki on vokaali, kasvatetaan vokaalien määrää
        }
        // Strchr avulla katsotaan onko str[i] kohdalla konsonantti
        else if (strchr(konsonantit, str[i]) != NULL)
        {
            tulos[1]++; // Jos merkki on konsonantti, kasvatetaan konsonanttien määrää
        }
    }
}