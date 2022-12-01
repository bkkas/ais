import pandas as pd

def main():
    d = pd.read_excel("mmsikos1.xlsx")
    print(d)
    print(type(d))
    with open("n_file.txt", 'w') as f:
        for row in d.iterrows():
            f.write(f"    {row[1]['Digit']}: \"{row[1]['Allocated to']}\",\n")
        pass
if __name__ == '__main__':
    main()