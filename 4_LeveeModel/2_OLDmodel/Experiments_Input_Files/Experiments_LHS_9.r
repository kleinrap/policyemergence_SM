#Lets load the lhs library
library(lhs)
library(ggplot2)
library(reshape)

#We will use the optimum lhs algorithm
#see http://rss.acs.unt.edu/Rdoc/library/lhs/html/optimumLHS.html

#Model design parameters
numberOfExperiments = 10	# How many experiments can we afford ?
numberOfParameters = 17

#Algorithm settings
maxSweeps=20	 		# The maximum number of times the algorithm may iterate ?
eps=.1				# The optimal stopping criterion

#we need to put the matrix in a data frame, so it gets headers etc, so we can work with it.
lhs=data.frame(optimumLHS(numberOfExperiments, numberOfParameters, maxSweeps, eps))

#make a histogram of each variable.
#We will do this to visualy inspect the uniformity of the data.

#We need to put the data in a two columns [ variable, value], or [X1, 0.223], so that we can plot it.
lhsMelt = melt(lhs)

#We will use 30 bins for each histogram
simpleHistogram = ggplot(data=lhsMelt, aes(x=value)) + geom_histogram(binwidth = 0.03) + facet_wrap(~ variable, scales="free") 
print(simpleHistogram)
ggsave(simpleHistogram, file="ExperimentDistributionHistogram.png") 



#Now we must scale the sample values so that we get paramter values out.
#LSH gives you numbers from [0 1]
#There are a few ways to do this.
#
# The seven parameters that need to be taken into account for experiment 1:
# 1. The belief tree aims (3 profiles) - 1 of 3
# 2. The affiliation weight 1 - from 0.7 to 0.8
# 3. The affiliation weight 2 - from 0.8 to 0.9
# 4. The affiliation weight 3 - from 0.9 to 1.0
# 5. The affiliation distribution 1 - from 25 to 50
# 6. The affiliation distribution 2 - from 25 to 50
# 7. The electorate influence on policymakers - from 0.001 to 0.010
# 8. The resource potency parameter - from 1 to 10
# 9. The resource weight action - from 0.05 to 0.20
# 10. The trust decay coefficient - from 0.01-0.10
# 11. The conflict level coefficient 1 - from 0.7 to 0.8
# 12. The conflict level coefficient 2 - from 0.8 to 0.9
# 13. The conflict level coefficient 3 - from 0.9 to 1.0
# 14. The team gap in belief - from 0.6 to 1.0
# 15. The team gap in closeness of problem - fom 0.2 to 0.7
# 16. The team gap in closeness of policy - from 0.2 to 0.7
# 17. The ACF threshold - from 0.15 to 0.55

# 1. The belief tree aims
#partitions1=3
# we count backwards to avoid overwriting the values we already set to 1.
#for (i in partitions1:0) {
#  lhs$X1[which(lhs$X1 > (i-1)/partitions1 & lhs$X1 <= i/partitions1)] = i
#}
lhs$X1 = 1

# 2. The affiliation weight 1
lhs$X2 = 0.7

# 3. The affiliation weight 2
lhs$X3 = 0.8

# 4. The affiliation weight 3
lhs$X4 = 0.9

# 5. The affiliation distribution 1
lhs$X5 = 33
#lhs$X5 = 1+lhs$X5*49

# 6. The affiliation distribution 2
lhs$X6 = 0

# 7. The elecorate influence on policymakers
#lhs$X7 = 0.001+lhs$X7*0.009
lhs$X7 = 0.001

# 8. The resource potency parameter
#lhs$X8 = 1+lhs$X8*9
lhs$X8 = 1

# 9. The resource weight action
#lhs$X9 = 0.05+lhs$X9*0.15
lhs$X9 = 0.1

# 10. The trust decay coefficient - from 0.01-0.10
#lhs$X10 = 0.01+lhs$X10*0.09
lhs$X10 = 0.05

# 11. The conflict level coefficient 1 - from 0.7 to 0.8
#lhs$X11 = 0.7+lhs$X11*0.1
lhs$X11 = 0.7

# 12. The conflict level coefficient 2 - from 0.8 to 0.9
lhs$X12 = 0.8
#
# 13. The conflict level coefficient 3 - from 0.9 to 1.0
#lhs$X13 = 0.9+lhs$X13*0.1
lhs$X13 = 0.9

# 14. The team gap in belief - from 0.6 to 1.0
lhs$X14 = 0.6+lhs$X14*0.4
#lhs$X14 = 0.8

# 15. The team gap in closeness of problem - fom 0.2 to 0.7
#lhs$X15 = 0.2+lhs$X15*0.5
lhs$X15 = 0.5

# 16. The team gap in closeness of policy - from 0.2 to 0.7
#lhs$X16 = 0.2+lhs$X16*0.5
lhs$X16 = 0.5

# 17. The ACF threshold - from 0.15 to 0.55
#lhs$X17 = 0.15+lhs$X17*0.4
lhs$X17 = 0.35

#1. our parameter value goes from [0  X]
#2. we have a base value and add a arange to it [x+0 x+y]
#3. a parameter is a boolean
#4. a parameter is a switch 1,2,3

#X1 whould be sweeped from [0 250]
#lhs$X1=lhs$X1*250

#X2 is swept from [300 350]
#lhs$X2=300+lhs$X2*50

#X3 is a boolean. If the sample value is below 0.5 is is TRUE, otherwise it is FALSE
#We ave to set the >= 0.5 first, otehrwise everything gets set to false.
#lhs$X3[which(lhs$X3 >= 0.5)] = "false"
#lhs$X3[which(lhs$X3 < 0.5)] = "true"

#x4 is a switch variable, having n possible values, 1,2,3...n We partition the [0 1] space into n parts, and test whether the value fall in, and assign a value to it.
#partitions=5

# we count backwards to avoid overwriting the values we already set to 1.
#for (i in partitions:1) {
#lhs$X4[which(lhs$X4 > (i-1)/partitions & lhs$X4 <= i/partitions)] = i
#}



#Now, lets save the data to a space separated file, no row or column names. 
#Note that we ARE NOT using CSV, as NetLogos file-read function expects space separated values
#You have to be careful when you read the experiment into NetLogo, to get the same order of parameters right.
write.table(lhs,file="Experiments_LHS_9.data",sep=",",row.names = FALSE,col.names = FALSE,quote = FALSE)

#This data file can be read into NetLogo and parameter values set up. See LhsExperiment.nlogo for a exampel how to do this.

