def test_load_trial_data():
    # Test with valid trial_id
    data, log = load_trial_data("1_1")
    assert len(data) > 0 and "successfully loaded" in log
    
    # Test with invalid type for trial_id
    try:
        load_trial_data(123)
    except ValueError as e:
        assert str(e) == "Input trial_id should be a string."
    
    # Test with invalid format for trial_id
    try:
        load_trial_data("abc_5")
    except ValueError as e:
        assert str(e) == "Input trial_id should be in the format x_n where x is an integer and n is a number from 1 to 4."
    
    # Test with non-existing trial_id
    try:
        load_trial_data("5_2")
    except ValueError as e:
        assert str(e) == "trial_id 5_2 not found in the database."
