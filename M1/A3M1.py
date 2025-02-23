import parse as p
import tokenizer as t
import index
import nltk

# "C:\\Users\\fight\\OneDrive\\Desktop\\CS121\\Assignment3\\CS121_SearchEngine\\DEV"
def main() -> None:
    """
    Run the program
    """
    files = p.traverse_directory("C:\\Users\\Justi\\Downloads\\CS121\\Assignment3M1\\cs_121_A3\\DEV")
    yeah = index.Indexer()
    yeah.run(files)

if __name__ == "__main__":
    main()
