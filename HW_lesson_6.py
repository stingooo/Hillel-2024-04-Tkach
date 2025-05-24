import time
import logging


# ------------------------------------------------------------------
# Task 1


class TimerContext:
    def __enter__(self):
        self.start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.monotonic() - self.start
        logging.info(f"Elapsed: {elapsed:.2f} seconds")


logging.basicConfig(level=logging.INFO)

with TimerContext():
    time.sleep(5)

#  ------------------------------------------------------------------
# Task 2


GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}


class Configuration:
    def __init__(self, updates: dict, validator=None):
        self.updates = updates
        self.validator = validator
        self.origin_global_CFG = None

    def __enter__(self):
        self.origin_global_CFG = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        if self.validator:
            try:
                validation = self.validator(GLOBAL_CONFIG)
                if not validation:
                    raise ValueError("Invalid value")
            except Exception as err:
                print(err, ", max_retries should be integer and more than Zero\n Restored to Default")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global GLOBAL_CONFIG
        GLOBAL_CONFIG = self.origin_global_CFG


def validate_config(config: dict):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0


# Test with valid updates
with Configuration(updates={"max_retries": 6, "feature_a": False}, validator=validate_config):
    print("Inside: ", GLOBAL_CONFIG)
print("Outside: ", GLOBAL_CONFIG)
print()

# Test with invalid updates
with Configuration(updates={"max_retries": -5}, validator=validate_config):
    print("Inside: ", GLOBAL_CONFIG)
print("Outside: ", GLOBAL_CONFIG)
print()

# Test with ERROR
with Configuration(updates={"max_retries": "a"}, validator=validate_config):
    print("Inside: ", GLOBAL_CONFIG)
print("Outside: ", GLOBAL_CONFIG)
