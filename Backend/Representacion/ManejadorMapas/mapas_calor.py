import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
class MapaCalor:

    def __init__(self,dataset:pd.DataFrame):
        self.dataset = dataset


    def representar(self):
        columnaY = range(1,self.dataset.shape[0])
        sns.heatmap(pd.DataFrame(self.dataset, index = columnaY, columns = self.dataset.columns))
        plt.show()
