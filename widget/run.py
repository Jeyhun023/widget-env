from openai import OpenAI
from tqdm import tqdm
import os
import time
import json

# Initialize the OpenAI client
# client = OpenAI(
#     api_key="",
#     organization='',
# )

info = """ZoomRentals offers a seamless online service designed to help customers effortlessly find, select, and rent cars from the comfort of their home. With access to a wide range of vehicles across multiple locations, we provide options for every need and budget. Whether you're planning a weekend getaway, a business trip, or need a temporary vehicle solution, ZoomRentals makes the process straightforward and stress-free. Our intuitive platform ensures you can easily compare prices, view detailed vehicle specifications, and book your perfect ride with just a few clicks, all backed by excellent customer support to assist you every step of the way."""
min_age = "18"
max_age = "50"
min_budget = "4000"
max_budget = "6000"
duration = "14"
goal = "Increase brand awareness"
comments = ""


# info = os.environ.get('info')
# min_age = os.environ.get('min_age')
# max_age = os.environ.get('max_age')
# min_budget = os.environ.get('min_budget')
# max_budget = os.environ.get('max_budget')
# duration = os.environ.get('duration')
# goal = os.environ.get('goal')
# comments = os.environ.get('comments')



def main(info, min_age, max_age, min_budget, max_budget, duration, goal, comments):
    if not comments:
        additional_comments = ""
    else:
        additional_comments = f"some additional comments provided by the client: {comments}"

    assistant = client.beta.assistants.create(
        name="Marketing Campaign Planner",
        description=r"""You are a Campaign Manager, or Campaign Director, you are responsible for planning and coordinating events to promote a particular project, including advertising initiatives.""",
        instructions=r"""Your primary duty is to ensure a comprehensive and effective marketing campaigns achieve their objectives. Duties include coordinating the efforts of various agencies and marketing roles, developing strategic plans for communicating a brand message. Plan the areas of focus to create, execute and monitor the performance of campaigns and provide all the resources required to meet targets. Ensure that the plan is catering directly to the clients specified insights, yet is creatively approached. Prepare a list of areas which the campaign documentation should include. Provide the list in a json format chronologically, like {"1": "intro", "2": "goals"}.
    """,
        #model="gpt-4-turbo-2024-04-09",
        response_format={"type": "json_object"},
        model="gpt-3.5-turbo-0125",
    )
    print("assistant created")

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f""" here are some requirements and insights from the client:
    - Product/service info: {info}
    - Target demographic analysis and audience profiling based on ages {min_age}-{max_age}.
    - Selection of marketing channels most likely to reach the target audience effectively.
    - A comprehensive budget allocation plan that aligns with {min_budget}-{max_budget} dollars while aiming to maximize ROI.
    - A timeline for campaign execution that fits within {duration} days.
    - Specific marketing actions and content suggestions to achieve {goal}.
    - Metrics for measuring campaign success aligned with the stated goal.

    {additional_comments}"""
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )

    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"{run.status} . ")
        time.sleep(1)
        print(f"{run.status} . . ")
        time.sleep(1)
        print(f"{run.status} . . .")
        time.sleep(1)

    print(f"{run.status} . ")
    print(f"{run.status} . . ")
    print(f"{run.status} . . .")

    thread_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )


    gpt_answer = []

    for message in thread_messages.data:
        for content in message.content:
            gpt_answer.append(content.text.value)

    del_assistant = client.beta.assistants.delete(assistant.id)

    doc_result_question = f"""{gpt_answer[0]}"""

    print("DONE")

    return doc_result_question

plan_json = main(info, min_age, max_age, min_budget, max_budget, duration, goal, comments)
print(plan_json)
test = json.loads(plan_json)


print(test)
print("SUCCESS!!!")


