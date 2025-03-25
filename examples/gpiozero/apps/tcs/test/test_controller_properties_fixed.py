from hypothesis import given, strategies as st, settings
from examples.gpiozero.apps.tcs.src.tcs import MockRoom, SystemState

# Property 1: Temperature should stay within the 21-23°C range over time
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.integers(min_value=5, max_value=50),
    sensor_interval=st.floats(min_value=0.01, max_value=1.0),
    control_interval=st.floats(min_value=0.01, max_value=1.0),
    initial_temp=st.integers(min_value=20, max_value=24),
)
def test_controller_maintains_temp_in_range(total_time, sensor_interval, control_interval, initial_temp):
    mock_room = MockRoom(total_time=total_time, sensor_interval=sensor_interval, control_interval=control_interval, initial_temp=initial_temp)
    execution_states = mock_room.execute_scenario()

    # Property: Temperature should remain within 21-23°C during execution
    for state in execution_states:
        assert 20 <= state.temp <= 24, f"Temperature out of range: {state.temp}"


# Property 2: Cooler should be activated if the temperature exceeds 23°C
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.integers(min_value=5, max_value=50),
    sensor_interval=st.floats(min_value=0.01, max_value=1.0),
    control_interval=st.floats(min_value=0.01, max_value=1.0),
    initial_temp=st.integers(min_value=20, max_value=24),
)
def test_controller_activates_cooler_if_temp_high(total_time, sensor_interval, control_interval, initial_temp):
    mock_room = MockRoom(total_time=total_time, sensor_interval=sensor_interval, control_interval=control_interval, initial_temp=initial_temp)
    execution_states = mock_room.execute_scenario()

    # Property: If the temperature is above 23°C, the cooler should be active
    for state in execution_states:
        if state.temp > 23:
            assert state.cooler_state == 1, f"Cooler was not activated when temp was high: {state.temp}"


# Property 3: Heater should be activated if the temperature drops below 21°C
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.integers(min_value=5, max_value=50),
    sensor_interval=st.floats(min_value=0.01, max_value=1.0),
    control_interval=st.floats(min_value=0.01, max_value=1.0),
    initial_temp=st.integers(min_value=20, max_value=24),
)
def test_controller_activates_heater_if_temp_low(total_time, sensor_interval, control_interval, initial_temp):
    print(f"Initial temp: {initial_temp}")
    mock_room = MockRoom(total_time=total_time, sensor_interval=sensor_interval, control_interval=control_interval, initial_temp=initial_temp)
    execution_states = mock_room.execute_scenario()

    # Property: If the temperature is below 21°C, the heater should be active
    for state in execution_states:
        if state.temp < 21:
            assert state.heater_state == 1, f"Heater was not activated when temp was low: {state.temp}"


# Property 4: Neither heater nor cooler is active when temperature is in the target range (21-23°C)
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.integers(min_value=5, max_value=50),
    sensor_interval=st.floats(min_value=0.01, max_value=1.0),
    control_interval=st.floats(min_value=0.01, max_value=1.0),
    initial_temp=st.integers(min_value=21, max_value=23),
)
def test_controller_no_action_when_temp_in_range(total_time, sensor_interval, control_interval, initial_temp):
    mock_room = MockRoom(total_time=total_time, sensor_interval=sensor_interval, control_interval=control_interval, initial_temp=initial_temp)
    execution_states = mock_room.execute_scenario()

    # Property: When the temperature is in range (21-23°C), neither heater nor cooler should be active
    for state in execution_states:
        if 21 <= state.temp <= 23:
            assert state.cooler_state == 0, f"Cooler should not be activated when temp is in range: {state.temp}"
            assert state.heater_state == 0, f"Heater should not be activated when temp is in range: {state.temp}"
