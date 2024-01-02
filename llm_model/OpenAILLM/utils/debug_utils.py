from litellm import completion_cost
from pathlib import Path

import logging


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


Path("../logs").mkdir(parents=True, exist_ok=True)
setup_logger('../logs/debug.log')


def print_basic_response_info(response):
    logging.info("Model Used: %s", response.get('model', 'N/A'))
    logging.info("Response Created At: %s", response.get('created', 'N/A'))
    logging.info("Token Usage: %s", response.get('usage', {}))


def print_detailed_choices_info(response):
    choices = response.get('choices', [])
    for i, choice in enumerate(choices):
        logging.info(f"Choice {i}:")
        logging.info("  Finish Reason: %s", choice.get('finish_reason', 'N/A'))
        message = choice.get('message', {})
        logging.info("  Role: %s", message.get('role', 'N/A'))
        logging.info("  Content: %s", message.get('content', 'N/A'))


def update_and_save_overall_cost(new_cost, filename="total_cost.txt"):
    try:
        with open(filename, 'r') as file:
            total_cost = float(file.read())
    except (FileNotFoundError, ValueError):
        total_cost = 0.0

    total_cost += new_cost

    with open(filename, 'w') as file:
        file.write(f"{total_cost}")

    logging.info(f"Updated Total Cost: ${total_cost:.10f}")


def calculate_and_update_cost(response, filename="total_cost.txt"):
    cost = completion_cost(completion_response=response)
    logging.info("Cost for this completion call: $%f", float(cost))
    update_and_save_overall_cost(cost, filename)
