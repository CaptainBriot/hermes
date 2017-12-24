def fan_speed(temperature):
    min_temp = 30.0
    max_temp = 70.0
    min_speed = 10.0
    max_speed = 100.0

    if temperature < min_temp:
        return int(min_speed)
    elif temperature > max_temp:
        return int(max_speed)

    # linear function: y = ax + b
    return int(((float(max_speed - min_speed) / float(max_temp - min_temp)) * (temperature - max_temp)) + max_speed)
