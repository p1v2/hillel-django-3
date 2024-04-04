import time


def get_weather(city):
    # Simulate slow API
    time.sleep(2)
    if city == "Kyiv":
        return {"temperature": 25, "humidity": 50}
    elif city == "London":
        return {"temperature": 15, "humidity": 70}
    else:
        return {"temperature": 0, "humidity": 0}
