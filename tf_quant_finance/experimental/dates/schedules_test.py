# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for schedules.py."""

import datetime

from absl.testing import parameterized
import numpy as np
import tensorflow.compat.v2 as tf

from tf_quant_finance.experimental import dates
from tf_quant_finance.experimental.dates import test_data
from tensorflow.python.framework import test_util  # pylint: disable=g-direct-tensorflow-import


@test_util.run_all_in_graph_and_eager_modes
class SchedulesTest(tf.test.TestCase, parameterized.TestCase):

  @parameterized.named_parameters(
      *test_data.schedule_with_fixed_range_test_cases)
  def test_schedule_on_fixed_interval(self, start_dates, end_dates,
                                      period_quantities, period_type, backward,
                                      expected_schedule):
    start_dates = dates.from_np_datetimes(_to_np_datetimes(start_dates))
    end_dates = dates.from_np_datetimes(_to_np_datetimes(end_dates))
    tenors = dates.periods.PeriodTensor(period_quantities, period_type)
    backward = backward
    expected_schedule = dates.from_np_datetimes(
        _to_np_datetimes(expected_schedule))
    actual_schedule = dates.PeriodicSchedule(
        start_dates,
        end_dates,
        tenors,
        dates.HolidayCalendar(
            weekend_mask=dates.WeekendMask.SATURDAY_SUNDAY,
            start_year=2020,
            end_year=2028),
        roll_convention=dates.BusinessDayConvention.MODIFIED_FOLLOWING,
        backward=backward).dates()
    self.assertAllEqual(expected_schedule.ordinal(), actual_schedule.ordinal())


def _to_np_datetimes(nested_date_tuples):

  def recursive_convert_to_datetimes(sequence):
    result = []
    for item in sequence:
      if isinstance(item, list):
        result.append(recursive_convert_to_datetimes(item))
      else:
        result.append(datetime.date(*item))
    return result

  return np.array(
      recursive_convert_to_datetimes(nested_date_tuples), dtype=np.datetime64)


if __name__ == "__main__":
  tf.test.main()
