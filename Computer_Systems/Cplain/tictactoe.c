/*Luo BOARD_SIZE^2 kokoisen pelialueen. Taulukossa kaikki rivit kirjoitettu yhteen pötköön*/
/*eli esimerkiksi taulukon indeksi 42 kuvaa ruudukon viidennen rivin kolmatta ruutua*/
/*Taulukossa olevat luvut kuvaavat kyseisten ruutujen merkkejä. 1 kuvaa ristiä, 2 nollaa ja 0 tyhjää ruutua.*/
#include <stdint.h>
#include <stdio.h>

#define BOARD_SIZE 10

// Funktioprototyyppi
int8_t tictactoe_check(int8_t * gameboard, int win_len);

int main() {
    int8_t gameboard[BOARD_SIZE * BOARD_SIZE] = {}; //tähän omia nappuloita, muuten kaikki nollia (tyhjiä)
    int win_len = 3;
    int8_t winner = tictactoe_check(gameboard, win_len);
    printf("Voittaja on: %d\n", winner);
    return 0;
}

int8_t tictactoe_check(int8_t * gameboard, int win_len) {
    int dx[] = {-1, 0, 1, 1};
    int dy[] = {1, 1, 1, 0};
    int8_t winner = 0;
    for (int i = 0; i < BOARD_SIZE * BOARD_SIZE; ++i) {
        if (gameboard[i] == 0) continue;
        for (int dir = 0; dir < 4; ++dir) {
            int len = 0;
            for (int j = 0; j < win_len; ++j) {
                int x = i / BOARD_SIZE + dx[dir] * j;
                int y = i % BOARD_SIZE + dy[dir] * j;
                if (x < 0 || x >= BOARD_SIZE || y < 0 || y >= BOARD_SIZE) break;
                if (gameboard[x * BOARD_SIZE + y] != gameboard[i]) break;
                len++;
            }
            if (len == win_len) {
                if (winner == 0) {
                    winner = gameboard[i];
                } else if (winner != gameboard[i]) {
                    return 0;
                }
            }
        }
    }
    return winner;
}

