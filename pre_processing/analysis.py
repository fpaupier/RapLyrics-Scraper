"""Consume functions from utilities to analyse the dataset"""

from utils import occurences_counter


def main():
    """Add other relevant function calls for dataset analysis"""
    occurences = occurences_counter('lyrics_US/dataset3-processed.txt')
    # TODO hardcode your last results if you want
    print("Number of different words in the original dataset3: 72601")
    print("Number of different words in last count (07-30-2018): 40961")
    print("Number of different words in last count LOWERED (07-30-2018): 33433")
    print("Number of different words in the dataset2: 219518")
    print("Number of different words in the dataset1: 168729")
    print("Number of different words in TinyShakespeare: 25670 ")
    print(f"Number of different words: {len(occurences)}")
    print("Repartition preview:")
    print(occurences)


if __name__ == "__main__":
    main()




