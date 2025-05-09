import pandas as pd

def csv_parser(filepath):
    try:
        df = pd.read_csv(filepath)
        
        return {
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(3).to_dict(orient='records')
        }
    except Exception as e:
        return {"error": str(e)}
