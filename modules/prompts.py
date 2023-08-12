CODE_PROMPT = """
# Goal
    Write Python code, in a triple backtick Markdown code block, that does the following:
    {}

# Notes
    First, think step by step what you want to do and write it down in English.
    Then generate valid Python code in a code block 
    Make sure all code is valid - it be run in a Jupyter Python 3 kernel environment. 
    
    Define every variable before you use it.
    When creating a DataFrame or reading data from file, verify what columns are present before proceeding to the next process.

    Be sure to generate charts with matplotlib.
    When you use "import matplotlib", you must also use "import japanize_matplotlib".

    You can use "financial_data.xlsx" in workspace folder.
    When you read data, you must use ```df = pd.read_excel('financial_data.xlsx', sheet_name=None)```.

# Teacher mode
    if the code modifies or produces a file, at the end of the code block insert a print statement that prints a link to it as HTML string: <a href='/download?file=INSERT_FILENAME_HERE'>Download file</a>. Replace INSERT_FILENAME_HERE with the actual filename.
"""