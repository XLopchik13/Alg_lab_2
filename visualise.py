from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

columns_prep = ["Prep_1", "Prep_2", "Prep_3"]
columns_res = ["Res_1", "Res_2", "Res_3"]
columns_total = ["Total_1", "Total_2", "Total_3"]
title_prep = "Dependence of preparation time on the number of rectangles"
title_res = "Dependence of execution time on the number of rectangles"
title_total = "Dependence of total time on the number of rectangles"
maxPower = 11
cnt_rectangles = list(map(lambda x: 2 ** x, range(maxPower)))

df = pd.read_table("tests.txt", sep="\t", header=None)
df.columns = columns_prep + columns_res + columns_total
df_prep, df_res, df_total = df[columns_prep], df[columns_res], df[columns_total]


def show_graph(df, columns, title):
    sns.lineplot(df, x=cnt_rectangles, y=columns[0], label="Brute_force")
    sns.lineplot(df, x=cnt_rectangles, y=columns[1], label="Map_algorithm")
    sns.lineplot(df, x=cnt_rectangles, y=columns[2], label="Persistent_segment_tree_algorithm")
    plt.xlabel("Rectangles")
    plt.ylabel("Time (nanoseconds)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.title(title)
    plt.show()


show_graph(df_prep, columns_prep, title_prep)
show_graph(df_res, columns_res, title_res)
show_graph(df_total, columns_total, title_total)
