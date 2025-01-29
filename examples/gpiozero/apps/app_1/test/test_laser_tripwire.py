import unittest
from io import StringIO
from unittest.mock import patch, Mock
from hypothesis import given
from hypothesis.strategies import *
from examples.gpiozero.apps.app_1.src import laser_tripwire

class TestLaserTripwire(unittest.TestCase):

    @given(is_dark=booleans())
    def test_intruder_detection_when_dark(self, is_dark):
        with patch('examples.gpiozero.apps.app_1.src.laser_tripwire.LightSensor') as MockLightSensor:
            """
            Test to verify that the INTRUDER is detected when darkness is detected.
            """
            # Mock the LightSensor instance
            sensor_mock = MockLightSensor.return_value

            # Create the intruder detector
            detector = laser_tripwire.create_intruder_detector_laser_tripwire()

            with patch("sys.stdout", new_callable=StringIO) as f:
                if is_dark:
                    # Simulate intruder detection by calling the `when_dark` method
                    sensor_mock.when_dark()
                    self.assertEqual(f.getvalue(), "INTRUDER\n")
                else:
                    self.assertNotEqual(f.getvalue(), "INTRUDER\n")

if __name__ == '__main__':
    unittest.main()
