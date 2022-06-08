from algorithms.master import Master
import pandas as pd

master = Master()
# pd.DataFrame(master.get_all_results_perc(1, 0.5), index=None).to_csv('results.csv', index=False)
pd.DataFrame(master.get_all_result_gen(50, 100, 50, 25, 10,0.1, 0.4, 3, 0.2), index=None).to_csv('results_gen.csv', index=False)