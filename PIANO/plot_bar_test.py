import matplotlib.pyplot as plt

all_note_score = [1,2,3]
all_bit_score = [4, 5, 6]
all_tempo_score = [7, 8, 9.1]


analysis_bar = [sum(all_note_score), sum(all_bit_score),  sum(all_tempo_score)]
bar_column = ['Note', 'Bit', 'Value']
plt.bar(bar_column, analysis_bar)
plt.ylabel('score')
plt.show()