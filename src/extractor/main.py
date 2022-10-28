#!/usr/bin/python3

from extractor import Extractor

def main():
    exit(0 if Extractor().run() else 1)

if __name__ == "__main__":
    main()
