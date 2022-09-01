set terminal png size 1600,900 crop
set output 'Iteration_00/data/plot.png'
p 'Iteration_00/data/plot-data.csv' w l, 'Iteration_00/data/SiO2_alpha_vs_lambda.csv' u ($1/10000):2 w l