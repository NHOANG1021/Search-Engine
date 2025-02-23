import parse as p
import tokenizer as t
import index
import nltk

def main() -> None:
    """
    Run the program
    """
    count = 0
    files = p.traverse_directory("C:\\Users\\fight\\OneDrive\\Desktop\\CS121\\Assignment3\\CS121_SearchEngine\\DEV\\aiclub_ics_uci_edu")
    for file in files:
        frequency_dict = p.parse(file)
        print(frequency_dict)
        count += 1

if __name__ == "__main__":
    main()
