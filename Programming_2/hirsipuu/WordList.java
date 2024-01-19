import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class WordList {
    private List<String> words;

    public WordList(String fileName) {
        words = new ArrayList<>();
        try (Scanner scanner = new Scanner(new File(fileName))) {
            while (scanner.hasNextLine()) {
                String word = scanner.nextLine().trim().toLowerCase();
                words.add(word);
            }
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + fileName);
        }
    }

    public String getRandomWord() {
        int index = (int) (Math.random() * words.size());
        return words.get(index);
    }

    public List<String> giveWords() {
        return words;
    }

    public WordList theWordsOfLength(int length) {
        WordList filteredList = new WordList("");
        for (String word : words) {
            if (word.length() == length) {
                filteredList.words.add(word);
            }
        }
        return filteredList;
    }

    public WordList theWordsWithCharacters(String someString) {
        WordList filteredList = new WordList("");
        for (String word : words) {
            if (word.length() == someString.length()) {
                boolean matches = true;
                for (int i = 0; i < someString.length(); i++) {
                    char c = someString.charAt(i);
                    if (c != '_' && c != Character.toLowerCase(word.charAt(i))) {
                        matches = false;
                        break;
                    }
                }
                if (matches) {
                    filteredList.words.add(word);
                }
            }
        }
        return filteredList;
    }
}
