import pandas as pd
class ConvertDataType:
    def __init__(self, column_name: str, target_type: type):
        self.column_name = column_name
        self.target_type = target_type

    # @staticmethod
    # def convert(self,df: pd.DataFrame) -> pd.DataFrame:
    #     try:
    #         df[self.column_name] = df[self.column_name].astype(self.target_type)
    #     except Exception as e:
    #         print(f"Error converting {self.column_name} to {self.target_type}: {e}")
    #     return df

    def convert(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        try:
            if self.target_type == 'datetime':
                df[self.column_name] = pd.to_datetime(df[self.column_name])
            else:
                df[self.column_name] = df[self.column_name].astype(self.target_type)
        except Exception as e:
            print(f"Error converting {self.column_name} to {self.target_type}: {e}")
        return df
    