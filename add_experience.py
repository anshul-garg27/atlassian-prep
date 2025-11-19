import json
import datetime
import random
import string

def generate_uuid(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def add_experience():
    new_content = """Given a company's hierarchy graph with Employees and departments, I had to find the closest department between a list of employees. Working solution was required and I had construct the dependency graph as well. The starting point was company which had multiple departments and in the deparments, there were multiple employees.
I gave the Lowest Common Ancestor approach and ran the solution for multiple test cases. The verdict was NO Hire. The reasons provided from the HR -
a. No clarifying questions were asked.
b. The edge cases like - if the employee didn't exist wasn't covered. (I had a discussion with the interviewer on this specifically and implemented the fail safe)
c. Time complexity wasn't computed correctly.
PS - To make the approach more efficient, I proposed to store the paths from the root to the deparments and just check which deparment the employee belongs to while getting the closest department. But the interviewer didn't let me discuss on this approach and kept insisting on making the LCA approach better without sheding any light on what exactly he felt the issue was.(space or time?)
Please write in the comments if you have a better solution.


HLD Round - Atlassian Tags management.
The interviewer was a Principal engineer and maturely handled the interview. Asked the API design, DB schema, microservices and then moved on to discussion on scaled up system. He asked questions on which components can act as a bottleneck and how can they be scaled.
The verdict was positive.


LLD Round - Mobile Snake system design
I was a bit overwhelmed because i hadn't attempted this question before and there were multiple requirements that were needed to be implemented. Finally, the interviewer wanted to see the position of head and tail in the console. I gave a working solution and was able to run all the use cases which were asked.


The verdict was NO Hire. The reasons provided from the HR -
a. Unit Test cases were not written
b. Exception handling wasn't done.ß
c. corner cases weren't covered


PS - I was proud of myself after implementing a running solution. But the HR feedback was absurd.

What do you guys think?
Hope I will be able to help others planning to give Atlassian interviews."""

    new_article = {
        "uuid": generate_uuid(),
        "title": "Atlassian Interview Experience - Company Hierarchy, Tags Management, Snake Game",
        "slug": "atlassian-interview-experience-company-hierarchy-tags-snake",
        "summary": "Interview experience covering Company Hierarchy (DS), Tags Management (HLD), and Mobile Snake (LLD).",
        "content": new_content,
        "isSlate": False,
        "topicId": random.randint(1000000, 9999999),
        "tags": [
            {
                "name": "Atlassian",
                "slug": "atlassian",
                "tagType": "COMPANY"
            }
        ],
        "topic": {
            "id": random.randint(1000000, 9999999),
            "topLevelCommentCount": 0
        },
        "fetched_at": datetime.datetime.now().isoformat()
    }

    try:
        with open("all_experience_details.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Add to the beginning of the list
        data["articles"].insert(0, new_article)
        data["metadata"]["total_articles"] += 1
        
        with open("all_experience_details.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        print("Successfully added new experience.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_experience()
