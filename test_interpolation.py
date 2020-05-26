import pytest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from interpolation import Matrix, NonDiagonalNeighboursNoAdjacentNanSupport

@pytest.mark.parametrize("input_array, output_array", 
[
    ([[59.865848, float('nan')], [60.111501,70.807258]], 
        [[59.865848, 65.336553], [60.111501,70.807258]]),

    ([[float('nan'), float('nan')], [60.111501,70.807258]], 
        [[float('nan'), float('nan')], [60.111501,70.807258]]),

    ([[float('nan'), float('nan')], [float('nan'),70.807258]], 
        [[float('nan'), float('nan')], [float('nan'),70.807258]]),

    ([[float('nan'), float('nan')], [float('nan'),float('nan')]], 
        [[float('nan'), float('nan')], [float('nan'),float('nan')]]),

    (   [[37.454012, 95.071431, 73.199394, 59.865848, float('nan')],
         [15.599452, 5.808361, 86.617615, 60.111501, 70.807258],
         [2.058449, 96.990985, float('nan'), 21.233911, 18.182497],
         [float('nan'), 30.424224, 52.475643, 43.194502, 29.122914],
         [61.185289, 13.949386, 29.214465, float('nan'), 45.606998]],
            [[37.454012, 95.071431, 73.199394, 59.865848, 65.336553],
             [15.599452, 5.808361, 86.617615, 60.111501, 70.807258],
             [2.058449, 96.990985, 64.329538, 21.233911, 18.182497],
             [31.222654, 30.424224, 52.475643, 43.194502, 29.122914],
             [61.185289, 13.949386, 29.214465, 39.338655, 45.606998]])
])
def test_matrix_as_expected(input_array, output_array):
    input = np.array(input_array)
    expected_output = np.array(output_array)

    matrix = Matrix(input)
    interpolation_strategy = NonDiagonalNeighboursNoAdjacentNanSupport()
    interpolated_matrix = matrix.get_interpolated_matrix(interpolation_strategy)
    
    np.testing.assert_allclose(interpolated_matrix, expected_output)