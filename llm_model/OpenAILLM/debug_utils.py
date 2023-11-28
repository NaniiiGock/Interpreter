from litellm import completion_cost


def print_basic_response_info(response):
    print("Model Used:", response.get('model', 'N/A'))
    print("Response Created At:", response.get('created', 'N/A'))
    print("Token Usage:", response.get('usage', {}))


def print_detailed_choices_info(response):
    choices = response.get('choices', [])
    for i, choice in enumerate(choices):
        print(f"Choice {i}:")
        print("  Finish Reason:", choice.get('finish_reason', 'N/A'))
        message = choice.get('message', {})
        print("  Role:", message.get('role', 'N/A'))
        print("  Content:", message.get('content', 'N/A'))
        print()


def update_and_save_overall_cost(new_cost, filename="total_cost.txt"):
    try:
        with open(filename, 'r') as file:
            total_cost = float(file.read())
    except FileNotFoundError:
        total_cost = 0.0
    except ValueError:
        total_cost = 0.0

    total_cost += new_cost

    with open(filename, 'w') as file:
        file.write(f"{total_cost}")

    print(f"Updated Total Cost: ${total_cost:.10f}")


def calculate_and_update_cost(response, filename="total_cost.txt"):
    cost = completion_cost(completion_response=response)
    print("Cost for this completion call:", f"${float(cost):.10f}")
    update_and_save_overall_cost(cost, filename)


