from examples.gpiozero.apps.tcs.src.tcs import MockRoom


def test_controller_lowers_temp():
    mock_room = MockRoom(total_time=1, sensor_interval=1, control_interval=1, initial_temp=24)
    execution_states = mock_room.execute_scenario()
    for state in execution_states:
        print(state)
    assert execution_states[0].cooler_state == 1