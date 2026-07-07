"""Phase 06 Integration: Mission Impossible — try/except, raise, custom exceptions, context managers, logging, exceptiongroup."""

import logging
import random
import time
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", handlers=[logging.FileHandler("/tmp/mission_impossible.log", mode="w"), logging.StreamHandler()])
logger = logging.getLogger("IMF")


class MissionError(Exception):
    """Base for all mission errors."""


class ExtractionFailed(MissionError):
    def __init__(self, agent, target):
        self.agent = agent
        self.target = target
        super().__init__(f"Extraction failed for {agent} at {target}")


class HackFailed(MissionError):
    def __init__(self, system, code):
        self.system = system
        self.code = code
        super().__init__(f"Hack failed on {system} (error {code})")


class CommsLost(MissionError):
    def __init__(self, zone):
        self.zone = zone
        super().__init__(f"Communications lost in {zone}")


@contextmanager
def secure_channel(zone):
    logger.info(f"Opening channel in {zone}")
    try:
        yield
    finally:
        logger.info(f"Closing channel in {zone}")


class Agent:
    def __init__(self, name, skill=70):
        self.name = name
        self.skill = skill
        self.failures = 0
        logger.info(f"Agent {self.name} activated (skill={skill})")

    def attempt_extraction(self, target):
        logger.info(f"Extraction at {target}")
        if random.randint(1, 100) > self.skill:
            self.failures += 1
            raise ExtractionFailed(self.name, target)
        logger.info(f"Extraction successful!")
        return True

    def attempt_hack(self, system, difficulty=50):
        logger.info(f"Hacking {system} (diff={difficulty})")
        if random.randint(1, 100) > difficulty:
            self.failures += 1
            raise HackFailed(system, random.choice([401, 403, 500, 503]))
        logger.info(f"{system} hacked")
        return True

    def total_failures(self):
        return self.failures


def run_mission(agent, target, systems):
    logger.info(f"\n{'='*40}\nMISSION: Infiltrate {target}\n{'='*40}")
    errors = []
    try:
        with secure_channel(target):
            for system in systems:
                try:
                    agent.attempt_hack(system, difficulty=random.randint(30, 80))
                except HackFailed as e:
                    errors.append(e)
            if errors:
                raise ExceptionGroup("Multiple hack failures", errors)
            agent.attempt_extraction(target)
    except ExceptionGroup as eg:
        logger.error(f"Mission FAILED: hack(s) failed")
        return False
    except ExtractionFailed as e:
        logger.error(f"Mission FAILED: {e}")
        return False
    except Exception as e:
        logger.critical(f"Unexpected: {e}")
        return False
    else:
        logger.info(f"MISSION ACCOMPLISHED: {target}")
        return True
    finally:
        logger.info(f"Report: {agent.name} had {agent.total_failures()} failure(s)")


if __name__ == "__main__":
    random.seed(42)
    agent = Agent("Ethan Hunt", skill=80)
    targets = [("Kremlin Vault", ["firewall", "database", "cctv"]), ("Syndicate HQ", ["mainframe", "comm-relay"]), ("Safe House", ["door-lock"])]
    successes = 0
    for target, systems in targets:
        if run_mission(agent, target, systems):
            successes += 1
    logger.info(f"\n{'='*40}\nSUMMARY: {successes}/{len(targets)} missions successful")
    logger.info(f"Mission log written to /tmp/mission_impossible.log")
