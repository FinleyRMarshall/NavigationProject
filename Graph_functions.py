import matplotlib.pyplot as plt
import numpy as np
from helper_functions import *
from main import *

def average_1(x, n, a):
    # computes an average from last average a and n indexed at 0 for next item x
    return (n * a + x) / (n + 1)


def graph_x1(satellite, prediction_data, estimate_data):
    estimate_x1 = []
    predictions_x1 = []

    for num in range(len(prediction_data)):
        x1_prediction, x2_prediction, p_prediction = prediction_data[num]

        predictions_x1.append(x1_prediction)

    for num in range(len(estimate_data)):
        x1_estimate, x2_estimate, p_estimate = estimate_data[num]

        estimate_x1.append(x1_estimate)

    plt.title('Dimension X1: Measurements, Prediction and Estimate of X1 over time')
    plt.plot(satellite.times, satellite.x1, label='X1')
    plt.plot(satellite.measurements_times, estimate_x1, label='Estimate_x1')
    plt.plot(satellite.measurements_times, satellite.measurements, 'o', label='Measurements')
    plt.plot(satellite.times, predictions_x1, '+', label='Predictions_x1')
    plt.legend(loc='upper left')
    plt.show()


def graph_x1_and_p(satellite, prediction_data, estimate_data):
    estimate_x1 = []
    predictions_x1 = []
    p_above = []
    p_below = []
    offset = 0

    for num, time in enumerate(satellite.times):
        x1_prediction, x2_prediction, p_prediction = prediction_data[num]
        predictions_x1.append(x1_prediction)

        if time in satellite.measurements_times:
            x1_estimate, x2_estimate, p_estimate = estimate_data[num - offset]
        else:
            offset += 1
            x1_estimate, x2_estimate, p_estimate = x1_prediction, x2_prediction, p_prediction

        p = p_estimate[0][0]
        estimate_x1.append(x1_estimate)
        p_above.append(x1_estimate + two_standard_deviations(p))
        p_below.append(x1_estimate - two_standard_deviations(p))

    plt.title('Dimension X1: Measurements, Prediction and P of X1 over time')
    plt.plot(satellite.times, satellite.x1, '.', label='X1')
    plt.plot(satellite.times, estimate_x1, label='Estimate_x1')
    plt.plot(satellite.times, p_above, label='Two Standard deviations above')
    plt.plot(satellite.times, p_below, label='Two Standard deviations below')

    plt.legend(loc='upper left')
    plt.show()


def graph_x2(satellite, prediction_data, estimate_data):
    estimate_x2 = []
    predictions_x2 = []

    for num in range(len(prediction_data)):
        x1_prediction, x2_prediction, p_prediction = prediction_data[num]
        predictions_x2.append(x2_prediction)

    for num in range(len(estimate_data)):
        x1_estimate, x2_estimate, p_estimate = estimate_data[num]
        estimate_x2.append(x2_estimate)

    plt.title('Dimension X2: Measurements, Estimate and P of X2 over time')
    plt.plot(satellite.times, satellite.x2, label='X2')
    plt.plot(satellite.measurements_times, estimate_x2, label='Estimate_x2')
    plt.plot(satellite.times, predictions_x2, '+', label='Predictions_x2')
    plt.legend(loc='upper left')
    plt.show()


def graph_x2_and_p(satellite, prediction_data, estimate_data):
    estimate_x2 = []
    predictions_x2 = []
    p_above = []
    p_below = []

    offset = 0

    for num, time in enumerate(satellite.times):
        x1_prediction, x2_prediction, p_prediction = prediction_data[num]
        predictions_x2.append(x2_prediction)

        if time in satellite.measurements_times:
            x1_estimate, x2_estimate, p_estimate = estimate_data[num - offset]
        else:
            offset += 1
            x1_estimate, x2_estimate, p_estimate = x1_prediction, x2_prediction, p_prediction

        p = p_estimate[1][1]
        estimate_x2.append(x2_estimate)
        p_above.append(x2_estimate + two_standard_deviations(p))
        p_below.append(x2_estimate - two_standard_deviations(p))

    plt.title('Dimension X2: Measurements, Prediction and P of X2 over time')
    plt.plot(satellite.times, satellite.x2, '.', label='X1')
    plt.plot(satellite.times, predictions_x2, label='Prediction_x2')
    plt.plot(satellite.times, p_above, label='Two Standard deviations above')
    plt.plot(satellite.times, p_below, label='Two Standard deviations below')

    plt.legend(loc='upper left')
    plt.show()


def graph_error(satellite, prediction_data, estimate_data):
    measurements_error = []
    x1_estimate_error = []
    x2_estimate_error = []
    h = satellite.h

    for num, time in enumerate(satellite.measurements_times):
        time = int(time // h)
        x1_prediction, x2_prediction, p_prediction = prediction_data[time]
        x1_estimate, x2_estimate, p_estimate = estimate_data[num]
        true_x1 = satellite.x1[time]
        true_x2 = satellite.x2[time]
        x1_measurement = satellite.measurements[num]

        measurements_error.append(x1_measurement - true_x1)
        x1_estimate_error.append(x1_estimate - true_x1)
        x2_estimate_error.append(x2_estimate - true_x2)

    plt.title('Error of Measurements and X1, X2 Estimates')
    plt.plot(satellite.measurements_times, measurements_error, label='Measurements_error')
    plt.plot(satellite.measurements_times, x1_estimate_error, label='X1_estimate_error')
    plt.plot(satellite.measurements_times, x2_estimate_error, label='X2_estimate_error')
    plt.legend(loc='upper left')
    plt.show()


def graph_average_error(satellite, prediction_data, estimate_data):
    average_measurements_error = [0]
    average_x1_estimate_error = [0]
    average_x2_estimate_error = [0]
    h = satellite.times[1] - satellite.times[0]

    for num, time in enumerate(satellite.measurements_times):
        time = int(time // h)
        x1_prediction, x2_prediction, p_prediction = prediction_data[time]
        x1_estimate, x2_estimate, p_estimate = estimate_data[num]
        true_x1 = satellite.x1[time]
        true_x2 = satellite.x2[time]
        x1_measurement = satellite.measurements[num]

        a = average_measurements_error[-1]
        average_measurements_error.append(average_1(abs(x1_measurement - true_x1), num, a))

        a = average_x1_estimate_error[-1]
        average_x1_estimate_error.append(average_1(abs(x1_estimate - true_x1), num, a))

        a = average_x2_estimate_error[-1]
        average_x2_estimate_error.append(average_1(abs(x2_estimate - true_x2), num, a))

    plt.title('Average Error of Measurements and X1, X2 Estimates')
    plt.plot(satellite.measurements_times, average_measurements_error[1:], label='Average_measurements_error')
    plt.plot(satellite.measurements_times, average_x1_estimate_error[1:], label='Average_x1_estimate_error')
    plt.plot(satellite.measurements_times, average_x2_estimate_error[1:], label='Average_x2_estimate_error')
    plt.legend(loc='upper left')
    plt.show()


def graph_analysis(data, parameter):

    plt.title("Analysis of {} different values for {}".format(len(data), parameter))
    x1_colours = ['#0ef1f0', '#1f56e0', '#2015ea']
    x2_colours = ['#f10e92', '#f21e0d', '#eb8214']


    for num, i in enumerate(data):
        measurements, x1s, x2s, times, value = i
        plt.plot(times[10:], measurements[10:], '#09f61d')
        x1_colour = x1_colours[num % 3]
        x2_colour = x2_colours[num % 3]
        plt.plot( times[10:], x1s[10:], x1_colour, label = 'X1 for {} = {}'.format(parameter, value))
        plt.plot( times[10:], x2s[10:], x2_colour, label = 'X2 for {} = {}'.format(parameter, value))

    plt.legend(loc='upper left')
    plt.show()

def graph_x1_x2_error(satellite, prediction_data, estimate_data):

    x1_error = []
    x2_error = []
    offset = 0

    for num, time in enumerate(satellite.times):
        x1_prediction, x2_prediction, p_prediction = prediction_data[num]

        if time in satellite.measurements_times:
            x1_estimate, x2_estimate, p_estimate = estimate_data[num - offset]
        else:
            offset += 1
            x1_estimate, x2_estimate, p_estimate = x1_prediction, x2_prediction, p_prediction

        true_x1 = satellite.x1[num]
        true_x2 = satellite.x2[num]
        x1_error.append(true_x1 - x1_estimate)
        x2_error.append(true_x2 - x2_estimate)

    plt.title('Dimension X2: Measurements, Prediction and P of X2 over time')
    plt.plot(satellite.times, x1_error, label='X1 Error')
    plt.plot(satellite.times, x2_error, label='X2 Error')

    plt.legend(loc='upper left')
    plt.show()
