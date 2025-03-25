from hypothesis import given, strategies as st, settings
from examples.gpiozero.apps.pcs.src.pcs import MockSystem

# Properties we want to test:
# 1. The location of the cylinders should always stay between 0 and 2 (inclusive).
# 2. Cylinder A should not move if Cylinder B is at the bottom.
# 3. Cylinder B should always follow the correct pattern of up and down movement.

# Test 1: Cylinder A and B's location should always be within the range [0, 2]
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.floats(min_value=0.1, max_value=50),
    cylinder_interval=st.floats(min_value=0.1, max_value=1),
    controller_interval=st.floats(min_value=0.1, max_value=1),
    mock_interval=st.floats(min_value=0.1, max_value=1)
)
def test_cylinder_location_within_bounds(total_time, cylinder_interval, controller_interval, mock_interval):
    mock_system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = mock_system.execute_scenario()

    for state in collected_states:
        # Ensure cylinder locations are within the allowed range
        assert 0 <= state.cylinder_a_loc <= 2, "Cylinder A out of bounds"
        assert 0 <= state.cylinder_b_location <= 2, "Cylinder B out of bounds"


# Test 2: Cylinder A should not move when Cylinder B is at the bottom (location 0)
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.floats(min_value=0.1, max_value=50),
    cylinder_interval=st.floats(min_value=0.1, max_value=1),
    controller_interval=st.floats(min_value=0.1, max_value=1),
    mock_interval=st.floats(min_value=0.1, max_value=1)
)
def test_cylinder_a_stays_still_when_b_at_bottom(total_time, cylinder_interval, controller_interval, mock_interval):
    mock_system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = mock_system.execute_scenario()

    for state in collected_states:
        print(state)
        # When Cylinder B is at the bottom (location 2), Cylinder A's motion should be 0
        if state.cylinder_b_location == 2:
            assert state.cylinder_a_motion == 0, "Cylinder A is moving while Cylinder B is at the bottom"


# Test 3: Cylinder B follows the up and down movement pattern
# @settings(deadline=10000, max_examples=20)
# @given(
#     total_time=st.floats(min_value=0.1, max_value=50),
#     cylinder_interval=st.floats(min_value=0.1, max_value=1),
#     controller_interval=st.floats(min_value=0.1, max_value=1),
#     mock_interval=st.floats(min_value=0.1, max_value=1)
# )
# def test_cylinder_b_moves_up_and_down(total_time, cylinder_interval, controller_interval, mock_interval):
#     mock_system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
#     collected_states = mock_system.execute_scenario()
#
#     for i in range(1, len(collected_states)):
#         prev_state = collected_states[i - 1]
#         current_state = collected_states[i]
#
#         # If Cylinder B's motion is upwards (1), location should be higher
#         if prev_state.cylinder_b_motion == 1:
#             assert current_state.cylinder_b_location >= prev_state.cylinder_b_location, "Cylinder B should be moving up"
#         # If Cylinder B's motion is downwards (-1), location should be lower
#         if prev_state.cylinder_b_motion == -1:
#             assert current_state.cylinder_b_location <= prev_state.cylinder_b_location, "Cylinder B should be moving down"


# Test 4: Cylinder motion values should always be -1, 0, or 1
@settings(deadline=10000, max_examples=20)
@given(
    total_time=st.floats(min_value=0.1, max_value=50),
    cylinder_interval=st.floats(min_value=0.1, max_value=1),
    controller_interval=st.floats(min_value=0.1, max_value=1),
    mock_interval=st.floats(min_value=0.1, max_value=1)
)
def test_cylinder_motion_is_valid(total_time, cylinder_interval, controller_interval, mock_interval):
    mock_system = MockSystem(total_time, cylinder_interval, controller_interval, mock_interval)
    collected_states = mock_system.execute_scenario()

    for state in collected_states:
        assert state.cylinder_a_motion in [-1, 0, 1], "Invalid motion for Cylinder A"
        assert state.cylinder_b_motion in [-1, 0, 1], "Invalid motion for Cylinder B"
