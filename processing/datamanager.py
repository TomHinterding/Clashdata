import pandas as pd
import os
import api.data_service as ds

class Datamanager:

    def __init__ (self, storage_dir = "data"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def upsert(df1, df2, indexvariable):
        df1[indexvariable] = df1[indexvariable].astype(str)
        df2[indexvariable] = df2[indexvariable].astype(str)
        df1 = df1.set_index(indexvariable)
        df2 = df2.set_index(indexvariable)
        df_merged = df2.combine_first(df1).reset_index()
        return df_merged

    def saveDFasPkl(self, df, filename):
        full_path = os.path.join(self.storage_dir, f"{filename}.pkl")
        df.to_pickle(full_path)
    
    def readPklFile(self, filename):
        full_path = os.path.join(self.storage_dir, f"{filename}.pkl")
        file = pd.read_pickle(full_path)
        return file
    
class Dataupdater:
    def __init__ (self):
        self.ds = ds()