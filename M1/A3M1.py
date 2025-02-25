import parse as p
import tokenizer as t
import index
import nltk
import time

# "C:\\Users\\fight\\OneDrive\\Desktop\\CS121\\Assignment3\\CS121_SearchEngine\\DEV"
def main() -> None:
    """
    Run the program
    """
    start_time = time.time()
    files = p.traverse_directory("C:\\Users\\Justi\\Downloads\\CS121\\Assignment3M1\\cs_121_A3\\DEV")
    index_maker = index.Indexer()
    index_maker.run(files)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Compute duration
    print(f"Execution time: {elapsed_time:.6f} seconds")



if __name__ == "__main__":
    main()
