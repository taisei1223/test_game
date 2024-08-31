import altair
import pandas

data = pandas.DataFrame({
    'x': ['A', 'B', 'C'],
    'y': [30, 50, 10]
})

altair.Chart(data, width=200, height=200).mark_line().encode(
    x='x',
    y='y',
)
