# Name: Steven Bradley
# NETID: svb140
# CSE 140 AA
# Homework 6 parts 1 and 2

import matplotlib.pyplot as plt
import csv
import os
import random
import math

########################################################################
##############           PART 1          ###############################
########################################################################

# The ideal frequency of digits
IDEAL = [.1,.1,.1,.1,.1,.1,.1,.1,.1,.1]
DIGITS = [0,1,2,3,4,5,6,7,8,9]

###### PROBLEM 1 #######################################################
def extract_election_vote_counts(input_file, names):
    """
    Given a file of election data and a list of names, returns a list of
    the vote counts for each of those candidates
    """
    return extract_data(input_file, names)

def extract_data(input_file, lst):
    """
    Given an input file in csv format and a list of column names, returns
    a list of all data in those columns as integers
    """
    result = []
    data = csv.DictReader(open(input_file))
    for row in data:
        for key in row:
            if key in lst:
                # reformats data(string) into integer value
                str_num = row[key].replace(',','')
                if str_num.isdigit():
                    result.append(int(str_num))
    return result

###### PROBLEM 2 #######################################################
def ones_and_tens_digit_histogram(lst):
    """
    Given a list of numbers, returns a list of the frequency of digits
    zero through 9 in the tens and ones spaces in the list. List must not
    have empty elements.
    """
    return frequency_of_digit_at_indexes(lst, -2, True)

def frequency_of_digit_at_indexes(lst, indx, zeros):
    """
    Given a list of data, an index and a True or False, returns the
    frequencies of digits at the index specified.
    If looking at ones and tens digits, use indx = -2 and True.
    If looking at the left most digit, use indx = 0 and False.
    """
    frequency = [0,0,0,0,0,0,0,0,0,0]
    lst_to_str = [str(num) for num in lst]
    for num in lst_to_str:
        assert(len(num) >= 1)
        if zeros:
            if len(num) > 1:
                frequency[int(num[indx])] += 1
                frequency[int(num[indx+1])] += 1
            else:
                frequency[0] += 1
                frequency[int(num[indx+1])] += 1
        else:
            if int(num[indx]) != 0:
                frequency[int(num[indx])] += 1
    result = [float(frequency[i])/sum(frequency) for i in range(10)]
    return result
    
###### PROBLEM 3 #######################################################
def plot_iranian_least_digits_histogram(data):
    """
    Graphs the given histogram of frequencies vs ideal frequencies.
    Returns None.
    """
    digit_frequency_plot(DIGITS, IDEAL, 'blue', 'Ideal', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, data, 'green', 'Iran', "Digit", "Frequency")
    plt.savefig("iran-digits.png")
    plt.show()
    return None

###### PROBLEM 4 #######################################################
def plot_distribution_by_sample_size():
    """
    Graphs the frequency of the digits in each random sample vs the ideal
    digit frequency. Returns None.
    """
    random_samples = create_random_samples([10,50,100,1000,10000], 99)
    random_freq = []
    for sample in random_samples:
        random_freq.append(ones_and_tens_digit_histogram(sample))                   
    # plot random samples vs ideal
    digit_frequency_plot(DIGITS, IDEAL, 'blue', 'Ideal', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, random_freq[0], 'green', '10 random numbers', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, random_freq[1], 'red', '20 random numbers', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, random_freq[2], 'purple', '100 random numbers', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, random_freq[3], 'black', '1000 random numbers', "Digit", "Frequency")
    digit_frequency_plot(DIGITS, random_freq[4], 'orange', '10000 random numbers', "Digit", "Frequency")
    plt.title("Distribution of last two digits")
    plt.legend(prop = {'size':8})
    plt.savefig("random-digits.png")
    plt.show()
    return None

def create_random_samples(sample_sizes, num):
    """
    Creates and returns a list of random number samples(lists) with a number
    of samples given by a list input.
    """
    random_samples = []
    for size in sample_sizes:
        indx = sample_sizes.index(size)
        random_numbers = []
        for i in range(size):
            random_numbers.append(random.randint(0,num))
        random_samples.append(random_numbers)
    return random_samples

def digit_frequency_plot(digits, data, color, label, xlabel, ylabel):
    """
    Creates a graph of frequencies of digits of data given with color
    and label specified
    """
    plt.plot(digits, data, color=color, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

###### PROBLEM 5 #######################################################
def mean_squared_error(lst1, lst2):
    """
    Give two lists of numbers, returns the mean squared error between values
    in each list
    """
    result = 0
    assert(len(lst1) == len(lst2))
    for i in range(len(lst1)):
        result += (lst1[i]-lst2[i])**2
    return result

###### PROBLEM 6 #######################################################
def calculate_mse_with_uniform(data):
    """
    Returns the mean squared error (MSE) between the given data and the IDEAL
    frequency of digits
    """
    return mean_squared_error(data, IDEAL)

def compare_iranian_mse_to_samples(iran_mse):
    """
    Compares the 2009 Iranian election MSE to the mse of 10000 random samples
    and prints the number of mse that are larger or equal, and smaller than
    the 2009 Iranian election MSE.
    """
    compare_mse_to_samples("2009 Iranian election", iran_mse, 120)

def compare_mse_to_samples(election, mse, n):
    """
    Compares the given MSE to the MSE of 10000 random samples and prints returns
    a list with two elements. The first is the number of larger or equal MSEs in
    the samples and the second is the number of smaller MSEs.
    Must give size of election data n.
    """
    smaller = 0
    larger = 0
    for i in range(10000):
        random_samples = create_random_samples([n], 99)
        sample_frequencies = ones_and_tens_digit_histogram(random_samples[0])
        sample_mse = calculate_mse_with_uniform(sample_frequencies)
        if sample_mse >= mse:
            larger += 1
        else:
            smaller += 1
    print_mse_results(election, mse, larger, smaller)
    
def print_mse_results(election, mse, larger, smaller):
    """
    Given an election, ideal MSE, larger MSE quantity, and smaller MSE quantity,
    prints the results of the MSE test.
    """
    print election,"MSE:", mse
    print "Quantity of MSEs larger than or equal to the",election,"MSE:", larger
    print "Quantity of MSEs smaller than the",election,"MSE:", smaller
    print election,"null hypothesis rejection level p:", float(larger)/10000
    return None

def test_2009_iranian_election():
    """
    Tests the 2009 Iranian election with MSE analysis
    """
    counts = extract_election_vote_counts("election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"])
    histogram = ones_and_tens_digit_histogram(counts)
    plot_iranian_least_digits_histogram(histogram)
    plot_distribution_by_sample_size()
    iran_mse = calculate_mse_with_uniform(histogram)
    compare_iranian_mse_to_samples(iran_mse)

def test_2008_US_election():
    """
    Tests the 2008 US election with MSE analysis
    """
    counts = extract_election_vote_counts("election-us-2008.csv", ["Obama", "McCain", "Nader", "Barr", "Baldwin", "McKinney", "Others votes"])
    histogram = ones_and_tens_digit_histogram(counts)
    us_mse = calculate_mse_with_uniform(histogram)
    compare_mse_to_samples("2008 Us election",us_mse, 342)
    
########################################################################
##############           PART 2          ###############################
########################################################################

###### PROBLEM 9 #######################################################
def benfords_law(d):
    """
    Given an integer, returns the Benford's Law value according to
    P(d) = log10(1 + 1/d)
    """
    return math.log10(1 + 1.0/d)

def plot_benfords_distribution():
    """
    Plots the Benford's distribution of numbers
    """
    digits = DIGITS[1:10]
    benfords_frequencies = get_benfords_frequencies()
    digit_frequency_plot(digits, benfords_frequencies, "blue","Benford", "First digit","Frequency")

def get_benfords_frequencies():
    """
    Returns a list of Benfords Frequencies
    """
    digits = DIGITS[1:10]
    benfords_frequencies = []
    for digit in digits:
        frequency = benfords_law(digit)
        benfords_frequencies.append(frequency)
    return benfords_frequencies

###### PROBLEM 10 ######################################################
def plot_random_benfords_scales():
    """
    Plots two random samples of simulated Benford frequencies. One using
    e^r and one using pi*e^r
    """
    plot_random_benford_sample(1000, 1, "1000 samples", "red")
    plot_random_benford_sample(1000, math.pi, "1000 samples, scaled by $\pi$", "black")
    
def plot_random_benford_sample(size, scaler, label, color):
    """
    Given a sample size, scaler to use, label and color for the line, plots
    one simulated Benford frequency with the given sample size.
    """
    samples = create_random_samples([size], 30.0)[0]
    sample_values = [scaler*math.e**num for num in samples]
    frequencies = frequency_of_digit_at_indexes(sample_values, 0, False)
    digit_frequency_plot(DIGITS[1:10], frequencies[1:10], color,label, "First digit","Frequency")

###### PROBLEM 11 ######################################################
def plot_benfords_vs_random_scaled_samples():
    """
    Plots a graph of the true Benford distribution frequencies vs two
    random scaled sample frequencies.
    """
    plot_benfords_distribution()
    plot_random_benfords_scales()
    plt.legend()
    plt.savefig("scale-invariance.png")
    plt.clf()
    #plt.show()

###### PROBLEM 12 ######################################################

def plot_benfords_vs_populations():
    """
    Plots a graph of the true Benford distribution frequencies vs two
    population frequencies.
    """
    plot_benfords_distribution()
    plot_population("SUB-EST2009_ALL.csv", ["POPCENSUS_2000"], "red", "US (all)", True)
    plot_population("literature-population.txt", [], "black", "Literature Places", False)
    plt.legend()
    plt.savefig("population-data.png")
    plt.clf()
    #plt.show()
   

def plot_population(input_file, lst, color, label, csv):
    """
    Plots one population digit frequency data with the given input file, column names,
    line color and label.
    csv is BOOLEAN.
    True if input file is csv format.
    False if the following format:
        Athkatla (Forgotten Realms)	130,000
        Baldur's Gate (Forgotten Realms)	42,000
        Barareh (Pavarchin)	92
        Bedrock (The Flintstones)	2,500
        ....
    """
    if csv:
        pops = extract_data(input_file, lst)
    else:
        pops = get_population_data(input_file)
    frequencies = get_population_digit_frequency(pops)
    digit_frequency_plot(DIGITS[1:10], frequencies[1:10], color,label, "First digit","Frequency")

def get_population_digit_frequency(population):
    """
    Returns the digit frequency of the given population data list
    """
    pops = population
    for pop in population:
        if pop < 2000:
            pops.remove(pop)
    return frequency_of_digit_at_indexes(pops, 0, False)

###### PROBLEM 13 ######################################################
def get_population_data(input_file):
    """
    Given an input file of specified format, returns the population data list.
    format:
        Athkatla (Forgotten Realms)	130,000
        Baldur's Gate (Forgotten Realms)	42,000
        Barareh (Pavarchin)	92
        Bedrock (The Flintstones)	2,500
        ....
    """
    result = []
    populations = open(input_file)
    for line in populations:
        data = line.split()
        if data[-1] > 2000:
            result.append(data[-1])
    return result

###### PROBLEM 14 ######################################################
def plot_random_benfords_samples():
    """
    Plots true Benford distribution vs 4 random simuilated frequencies of
    sample sizes 10, 50, 100, and 10000.
    """
    plot_benfords_distribution()
    plot_random_benford_sample(10, 1, "10 samples", "red")
    plot_random_benford_sample(50, 1, "50 samples", "black")
    plot_random_benford_sample(100, 1, "100 samples", "purple")
    plot_random_benford_sample(10000, 1, "10000 samples", "green")
    plt.legend()
    plt.savefig("benford-samples.png")
    plt.clf()
    #plt.show()

###### PROBLEM 15 ######################################################
def compare_benfords_vs_us_town_mse():
    """
    Computes and compares the mean square error between random samples of US town
    population data and the literature population data MSE. Does this comparison
    10000 times and prints out the number or random US town MSE that are larger or
    equal, or smaller than the literature population data MSE.
    """
    #Get population data
    pops = extract_data("SUB-EST2009_ALL.csv", ["POPCENSUS_2000"])
    lit_data = get_population_data("literature-population.txt")
    #Get frequencies
    lit_freq = get_population_digit_frequency(lit_data)
    benfords = get_benfords_frequencies()
    #Base MSE
    lit_mse = mean_squared_error(lit_freq[1:10], benfords)
    larger = 0
    smaller = 0
    same = 0
    for i in range(10000):
        sample_pops = []
        #Ensures same sample size as literature data
        for i in range(len(lit_data)):
            num = random.randint(0, len(pops)-1)
            sample_pops.append(pops[num])
        sample_pops_freq = get_population_digit_frequency(sample_pops)
        sample_mse = mean_squared_error(sample_pops_freq[1:10], benfords)
        if sample_mse > lit_mse:
            larger += 1
        elif sample_mse < lit_mse:
            smaller +=1
        else:
            same += 1
    print "larger/equal:", larger+same
    print "smaller:", smaller
         
# The code in this function is executed when this file is run as a Python program
def main():
    #test_2009_iranian_election()
    #test_2008_US_election()
    plot_benfords_vs_random_scaled_samples()
    plot_benfords_vs_populations()
    plot_random_benfords_samples()
    compare_benfords_vs_us_town_mse()

    
if __name__ == "__main__":
    main()
