import pandas as pd

def generate_report(results, filename="report.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    return filename
