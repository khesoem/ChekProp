from examples.gpiozero.apps.pcs.src.pcs import MockSystem

def test_starting_motion():
    mock_system = MockSystem(total_time=1, cylinder_interval=1, controller_interval=1, mock_interval=1)
    collected_states = mock_system.execute_scenario()
    assert collected_states[0].cylinder_a_motion == 0
    assert collected_states[0].cylinder_b_motion == 1