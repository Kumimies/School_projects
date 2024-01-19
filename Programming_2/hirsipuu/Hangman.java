import java.util.ArrayList;
import java.util.List;

public class Hangman {
    private String word;
    private int remainingGuesses;
    private List<Character> guessedLetters;

    public Hangman(WordList wordList, int numGuesses) {
        this.word = wordList.getRandomWord();
        this.remainingGuesses = numGuesses;
        this.guessedLetters = new ArrayList<>();
    }

    public boolean guess(Character c) {
        Character lowerC = Character.toLowerCase(c);
        boolean found = false;
        if (!guessedLetters.contains(lowerC)) {
            guessedLetters.add(lowerC);
            for (int i = 0; i < word.length(); i++) {
                if (Character.toLowerCase(word.charAt(i)) == lowerC) {
                    found = true;
                }
            }
            if (!found) {
                remainingGuesses--;
            }
        } else {
            for (int i = 0; i < word.length(); i++) {
                if (Character.toLowerCase(word.charAt(i)) == lowerC) {
                    found = true;
                }
            }
            if (!found) {
                remainingGuesses--;
            }
        }
        return found;
    }

    public List<Character> guesses() {
        return guessedLetters;
    }

    public int guessesLeft() {
        return remainingGuesses;
    }

    public String word() {
        return word;
    }

    public boolean theEnd() {
        return isGameLost() || isGameWon();
    }

    public boolean isGameWon() {
        for (int i = 0; i < word.length(); i++) {
            if (!guessedLetters.contains(word.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public boolean isGameLost() {
        return remainingGuesses <= 0;
    }

    public String getMaskedWord() {
        StringBuilder maskedWord = new StringBuilder();
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            if (guessedLetters.contains(c)) {
                maskedWord.append(c);
            } else {
                maskedWord.append("*");
            }
            maskedWord.append(" ");
        }
        return maskedWord.toString().trim();
    }
}
