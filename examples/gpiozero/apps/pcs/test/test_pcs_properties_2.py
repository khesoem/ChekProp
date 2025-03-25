from hypothesis import given, strategies as st
from examples.gpiozero.apps.pcs.src.pcs import MockSystem


# Test that the cylinder locations remain within the bounds (0 and 2) at all times.
@given(
    total_time=st.floats(min_value=1.0, max_value=100.0),
    cylinder_interval=st.floats(min_value=0.1, max_value=10.0),
    controller_interval=st.floats(min_value=0.1, max_value=10.0),
    mock_interval=st.floats(min_value=0.1, max_value=10.0),
)
def test_cylinder_location_in_bounds(total_time, cylinder_interval, controller_interval, mock_interval):
    system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = system.execute_scenario()

    for state in collected_states:
        assert 0 <= state.cylinder_a_loc <= 2, f"Cylinder A out of bounds: {state.cylinder_a_loc}"
        assert 0 <= state.cylinder_b_location <= 2, f"Cylinder B out of bounds: {state.cylinder_b_location}"


# Test that a cylinder only starts moving if it's at the start or end.
@given(
    total_time=st.floats(min_value=1.0, max_value=100.0),
    cylinder_interval=st.floats(min_value=0.1, max_value=10.0),
    controller_interval=st.floats(min_value=0.1, max_value=10.0),
    mock_interval=st.floats(min_value=0.1, max_value=10.0),
)
def test_cylinder_trigger_motion(total_time, cylinder_interval, controller_interval, mock_interval):
    system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = system.execute_scenario()

    for state in collected_states:
        if state.cylinder_a_loc == 1:
            assert state.cylinder_a_motion == 0, "Cylinder A should not be moving when in the middle"
        if state.cylinder_b_location == 1:
            assert state.cylinder_b_motion == 0, "Cylinder B should not be moving when in the middle"


# Test interaction between the controllers and the cylinders.
@given(
    total_time=st.floats(min_value=1.0, max_value=100.0),
    cylinder_interval=st.floats(min_value=0.1, max_value=10.0),
    controller_interval=st.floats(min_value=0.1, max_value=10.0),
    mock_interval=st.floats(min_value=0.1, max_value=10.0),
)
def test_controller_cylinder_interaction(total_time, cylinder_interval, controller_interval, mock_interval):
    system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = system.execute_scenario()

    for i in range(1, len(collected_states)):
        previous_state = collected_states[i - 1]
        current_state = collected_states[i]

        # Controller A should only trigger Cylinder A if Cylinder B has just stopped at the start
        if previous_state.cylinder_b_location == 0 and previous_state.cylinder_b_motion == 0:
            assert current_state.cylinder_a_motion != 0, "Cylinder A should have started moving"

        # Controller B should only trigger Cylinder B if Cylinder A has just stopped or Cylinder B is at the end
        if previous_state.cylinder_a_loc == 2 or previous_state.cylinder_a_motion == 0:
            assert current_state.cylinder_b_motion != 0, "Cylinder B should have started moving"


# Test that both cylinders do not move in conflicting directions.
@given(
    total_time=st.floats(min_value=1.0, max_value=100.0),
    cylinder_interval=st.floats(min_value=0.1, max_value=10.0),
    controller_interval=st.floats(min_value=0.1, max_value=10.0),
    mock_interval=st.floats(min_value=0.1, max_value=10.0),
)
def test_no_conflicting_cylinder_motion(total_time, cylinder_interval, controller_interval, mock_interval):
    system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = system.execute_scenario()

    for state in collected_states:
        # Ensure both cylinders aren't moving in conflicting directions at the same time
        assert not (state.cylinder_a_motion == 1 and state.cylinder_b_motion == -1), "Cylinders cannot move in conflicting directions"
        assert not (state.cylinder_a_motion == -1 and state.cylinder_b_motion == 1), "Cylinders cannot move in conflicting directions"
