import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

#========================================================================================================================================================================
# FUNCTION FOR VALIDATION OF TYPE OF DATA
#========================================================================================================================================================================

class distribution_analysis (BaseModel):
    
    model_config = ConfigDict(arbitrary_types_allowed=True) # allows to set external types of arg, like the dataframe from pandas.
    
    dataset: pd.DataFrame
    column: str
    
    @field_validator('dataset')
    @classmethod
    
    #===============================================DATASET IS EMPTY?===============================================

    def dataset_notEmpty (cls, df: pd.DataFrame) -> pd.DataFrame: # check if the df is empty 
        if df.empty:
            raise ValueError('The dataset cannot be empty')
        return df
    
    @field_validator('column')
    @classmethod
    
    #===============================================COLUMN IS BLANK?===============================================
    
    def column_notBlank (cls, column: str) -> str: # check if the column is blank and return him to his atribbute
        if not column.strip():
            raise ValueError('The column cannot be blank')
        return column
    
    @model_validator(mode='after') 
    
    #===============================================COLUMN IS IN THE DATASET?===============================================
    
    def column_in_dataset (self) -> 'distribution_analysis': # check if the columns is in the dataset and returns him to his class
        if self.column not in self.dataset.columns:
            raise ValueError(f'The column {self.column} is not in the {self.dataset}')
        
        number_columns = self.dataset.select_dtypes(include='number').columns
        
        if self.column not in number_columns:
            raise TypeError(f"The column {self.column} is not numeric. Only numeric columns are accepted")
        
        return self

#========================================================================================================================================================================
# FUNCTION FOR STATS AND DISTRIBUITION
#========================================================================================================================================================================
    
def distribution_and_stats (dataset: pd.DataFrame, column: str):
    
    params = distribution_analysis(dataset=dataset, column=column) # the atribbutes of the class is now used here. 
                                                                    # If any error appear before, this function is not compilling
    df = params.dataset
    col = params.column
    series = df[col]
    
    #===============================================CALCULARION OF THE AVERAGE, MEDIAN AND STANDARD DEVIATION===============================================

    avg = round(series.mean(), 2)
    median = round(series.median(), 2)
    std = round(np.std(series), 2)
    
    #===============================================BOWLEY'S COEFFICIENT OF SKEWNESS===============================================

    q1 = round(series.quantile(0.25), 2)
    q2 = round(series.quantile(0.75), 2)
    iqr = round(q2-q1, 2)

    skewness = round((((q2+q1) - (2*median))/iqr), 2)
    
    #===============================================INFO DISPLAY===============================================

    print(f"{"=" * 50}INFO DISPLAY:{dataset}{"=" * 50}")
    print(f"Average of {column}: {avg}")
    print(f"Median of {column}: {median}")
    print(f"Standard Deviation of {column}: {std}")
    print(f"Skewness of {column}: {skewness}")
    print("="*125)
    
    #===============================================DATASET DISTRIBUITION===============================================
    
    sns.set_theme(style='dark')
    
    plt.figure(figsize=(10, 6))
    sns.histplot(
        x=series,
        kde=True,
        color='black',
        bins=30
    )
    
    plt.title(f'Distribuition of {col}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    plt.axvline(
        avg, 
        color='r', 
        linestyle='dashed', 
        linewidth=1.5,
        label=f'Average: ({avg:.2f})'
    )
    
    plt.axvline(
        median, 
        color='b', 
        linestyle='dotted', 
        linewidth=1.5,
        label=f'Median: ({median:.2f})'
    )

    plt.legend()
    plt.grid(True)
    plt.show()

#========================================================================================================================================================================
# FUNCTION FOR FILTER DATA, BASED IN THE TYPE OF METRIC
#========================================================================================================================================================================


    