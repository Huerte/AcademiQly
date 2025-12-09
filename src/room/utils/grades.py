def calculate_grade(score, total, base_passing=60):
    """
        example, if score i 75 over 100 then it is equal to 3.0 (60%)
    """
    if total <= 0:
        return 0, 0.0

    percent = (score / total) * 100

    if percent >= base_passing + 36:
        grade = 1.0
    elif percent >= base_passing + 30:
        grade = 1.25
    elif percent >= base_passing + 24:
        grade = 1.5
    elif percent >= base_passing + 18:
        grade = 1.75
    elif percent >= base_passing + 12:
        grade = 2.0
    elif percent >= base_passing + 6:
        grade = 2.25
    elif percent >= base_passing:
        grade = 3.0
    else:
        grade = 5.0  # failed

    return round(percent, 2), grade