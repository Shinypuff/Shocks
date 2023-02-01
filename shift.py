class Jeeja():

    def __init__(self, data):
        self.data = data
    
    ### data имеет вид: data[0] = сдвигаемые данные (факторы); data[1] = несдвигаемые данные (результирующая переменная)


    def get_shift(self, data, year=2009, days=0, show_fig=True):

        df = self.data[self.data.index.year==year]
        df.columns=['X', 'Y']

        df['X']=df['X'].shift(periods=days)
        shifted = df.iloc[days:,:]

        if show_fig != False:

            fig, ax = plt.subplots()

            ax.plot(df['X'], color='red', label = "bond_rets")
            ax.legend(loc='upper right', bbox_to_anchor=(0.5, -0.07))

            ax2=ax.twinx()
            ax2.plot(df['Y'], label = "RGBi")
            ax2.legend(loc='upper left', bbox_to_anchor=(0.5, -0.07))

            kr = key_rate[key_rate.index.year==year].index

            for date in kr:
                plt.axvline(date, color='black',alpha=0.1)
                ax2.text(date, max(df['Y']), str(key_rate.loc[date, 'change']), horizontalalignment='center')

            plt.rcParams["figure.figsize"] = (11,4)
            plt.show()

        return shifted

    def get_cor(self, data, days_limit=100):

        cor_table = pd.DataFrame()
        cor_table.index = list(range(0, days_limit))
        cor_table.index.name = 'Shift (days)'

        for year in self.data.index.year.unique():

            for day in range(0, days_limit+1):

                x = get_shift(self.data, year, day, show_fig=False)
                cor = x.corr()
                cor_table.loc[day,year] = cor.iloc[0,1]

        return cor_table

    def get_best_cor(self, data, *args):
        best_cor={}
        
        cor_tab = get_cor(self.data, days_limit=args)

        for year in cor_tab.columns:
            b_yearcor = max(cor_tab[year], key=abs)
            b_shift = list(cor_tab[cor_tab[year]==b_yearcor].index)

            best_cor[year] = (b_shift[0], b_yearcor)

        return best_cor