from src.keyword_generator import KeywordGenerator
import sys

def main(topic):
    kw_generator = KeywordGenerator()
    keys = kw_generator.get_keywords(topic,10)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <argument>")
        sys.exit(1)
    
    # Extract the argument
    argument = sys.argv[1]

    main(argument)