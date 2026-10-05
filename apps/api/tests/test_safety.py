from app.services.safety import evaluate_safety

def test_normal_message_is_not_urgent():
    assert evaluate_safety("Tell me about gotukola").urgent is False

def test_english_red_flag_is_urgent():
    assert evaluate_safety("I have severe chest pain").urgent is True

def test_sinhala_red_flag_is_urgent():
    assert evaluate_safety("මට හුස්ම ගන්න අමාරු").urgent is True
