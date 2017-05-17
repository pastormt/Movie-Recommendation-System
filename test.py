from scipy import stats

x = [1,2]
y = [3,4]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
