# This script runs analysis and visualizations on the behavioral data.
library('tidyverse')

data_filepath <- '../data/behavior/all_data_beatpadding=0'
data <- read.csv(data_filepath)
as_tibble(data)
data <- data[-1] # remove the first column - uninformative index

#data %>%
#  select(-c(X,cond,rep,sub,group))

#mutate(data, avg_acc = mean())
