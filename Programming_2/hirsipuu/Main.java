/*Hirsipuu javassa.*/
/*Sanat luetoon words.txt tiedostosta.*/

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            WordList wordList = new WordList("words.txt");
            Hangman hangman = new Hangman(wordList, 5);

            while (!hangman.theEnd() && hangman.guessesLeft() > 0) {
                System.out.println("\nThe hidden word...\n");
                System.out.println(hangman.getMaskedWord());
                System.out.println("\nGuesses left: " + hangman.guessesLeft());
                System.out.println("Guessed letters: " + hangman.guesses());
                System.out.print("\nGuess a letter: ");

                String input = scanner.nextLine().toLowerCase(); // convert input to lowercase
                if (input.length() != 1) {
                    System.out.println("\nPlease enter a single letter.\n");
                    continue;
                }

                char guess = input.charAt(0);
                hangman.guess(guess);
            }

            if (hangman.theEnd() && hangman.guessesLeft() > 0) {
                System.out.println("Congratulations! You won!!!\nThe hidden word was: " + '"' + hangman.word() + '"');
            }

            else {
                System.out.println("Sorry, you lost! \nThe hidden word was: " + '"' + hangman.word() + '"');
            }

        }

    }
}
