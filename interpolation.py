
import math
import numpy
import sys
import argparse
from abc import ABC, abstractmethod

class InterpolationStrategy(ABC):

    @abstractmethod
    def interpolate_value(self, row, column, matrix):
        pass


class NonDiagonalNeighboursNoAdjacentNanSupport(InterpolationStrategy):

    def __init__(self):
        super().__init__()

    def interpolate_value(self, row, column, matrix):

        try:
            validNeighboursCumulativeValue = 0.0
            numberOfValidNeighbours = 0

            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):

                    neighbourValue = matrix.get_value(i, j)

                    if (neighbourValue != 'non-existent') and self.__is_valid(row, column, i, j):
                        validNeighboursCumulativeValue += neighbourValue
                        numberOfValidNeighbours += 1

            return validNeighboursCumulativeValue/numberOfValidNeighbours
        except Exception as e:
            msg = "Error interpolating value at row: {} and column: {}". format(row, column)
            raise Exception(msg) from e
        
    def __is_valid(self, row, column, i, j):
        return not((row != i and column != j) or (row == i and column == j))


class Matrix:

    def __init__(self, matrix):
            self.__matrix = matrix

    def get_value(self, row, column):
        if self.__is_within_shape(row, column):
            return self.__matrix[row, column]
        return 'non-existent'

    def get_interpolated_matrix(self, interpolationStrategy):

        interpolated_matrix = self.__matrix

        for position, value in numpy.ndenumerate(self.__matrix):
            if math.isnan(value):
                interpolated_matrix[position[0]][position[1]] = interpolationStrategy.interpolate_value(position[0], position[1], self)
        
        return interpolated_matrix

    def __is_within_shape(self, row, column):
        return ((row >= 0 and row < self.__matrix.shape[0]) and (column >= 0 and column < self.__matrix.shape[1]))


class FileOperations:

    @staticmethod
    def read(filename):
        try:
            return numpy.loadtxt(filename, delimiter=',')
        except Exception as e:
            msg = "Error while reading input from file: {}.".format(filename)
            raise Exception(msg) from e

    @staticmethod
    def write(filename, data_to_be_saved):
        try:
            numpy.savetxt(filename, data_to_be_saved, '%6f', ',')
        except Exception as e:
            msg = "Error while writing output to file: {}.\nOutput to be written:\n{}".format(filename, data_to_be_saved)
            raise Exception(msg) from e


def main():

    try:
        ap = argparse.ArgumentParser()

        ap.add_argument('-i', required=True, help='input file with full path')
        ap.add_argument('-o', required=True, help='output file with full path; if path not specified, then created in current working directory')

        args = vars(ap.parse_args())

        input_filename = args['i']
        output_filename = args['o']

        ndarray = FileOperations.read(input_filename)
        matrix = Matrix(ndarray)

        interpolated_strategy = NonDiagonalNeighboursNoAdjacentNanSupport()
        interpolated_matrix = matrix.get_interpolated_matrix(interpolated_strategy)        
        
        FileOperations.write(output_filename, interpolated_matrix)    

    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    main()