from congestrl.core import calculate_delay

def unit_delay():
    active_periods = [
        (0.0, 1.3),
        (1.5, 2.0),
        (2.5, 6.0),
        (7.3, 8.9)
    ]
    created, received = 0.0, 1.5
    print(calculate_delay(created, received, active_periods))

if __name__ == '__main__':
    unit_delay()
