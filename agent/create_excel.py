import pandas as pd

def matrix_to_excel(matrix, filename):
    """Convert a matrix (list of lists) to an Excel sheet with columns name, age, city."""
    df = pd.DataFrame(matrix, columns=['name', 'age', 'city'])
    df.to_excel(filename, index=False)
    print(f'Data saved to {filename}')

if __name__ == '__main__':
    # 5 rows of data: name, age, city
    data = [
        ['Alice', 30, 'New York'],
        ['Bob', 25, 'Los Angeles'],
        ['Charlie', 35, 'Chicago'],
        ['Diana', 28, 'Houston'],
        ['Ethan', 22, 'Phoenix']
    ]
    matrix_to_excel(data, 'people.xlsx')
