import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api_flow():
    print("Testing API Flow...")
    
    # 1. Create Visitor Company
    print("\n1. Creating Visitor Company...")
    company_data = {
        "company_name": "Test Visitor",
        "industry": "Technology",
        "number_of_employees": "1-10",
        "website": "",
        "city": "",
        "email": ""
    }
    try:
        res = requests.post(f"{BASE_URL}/companies", json=company_data)
        if res.status_code != 200:
            print(f"FAILED: {res.text}")
            return
        company = res.json()
        print(f"SUCCESS: Company ID {company['company_id']}")
    except Exception as e:
        print(f"FAILED: Could not connect to backend. Is it running? {e}")
        return

    # 2. Create Response
    print("\n2. Creating Response...")
    try:
        res = requests.post(f"{BASE_URL}/responses", json={"company_id": company['company_id']})
        if res.status_code != 200:
            print(f"FAILED: {res.text}")
            return
        response = res.json()
        response_id = response['response_id']
        print(f"SUCCESS: Response ID {response_id}")
    except Exception as e:
        print(f"FAILED: {e}")
        return

    # 3. Save Answers (Simulate Wizard)
    print("\n3. Saving Answers...")
    # Get questions first to know IDs? Assuming 1 for now or fetching
    # Let's just try to save for question_id=1
    try:
        # Mock answer for question 1 (Slider?)
        # Need to know question type/ID.
        # Let's fetch questionnaire first
        q_res = requests.get(f"{BASE_URL}/questionnaire")
        questions = q_res.json()['questions']
        print(f"Fetched {len(questions)} questions.")
        if len(questions) < 10:
             print("FAILED: Too few questions loaded. Did seeding work?")
             return

        q1 = questions[0]
        
        # Answer q1
        answer_ids = [q1['answers'][0]['answer_id']]
        res = requests.patch(f"{BASE_URL}/responses/{response_id}/items", json={
            "question_id": q1['question_id'],
            "answer_ids": answer_ids
        })
        if res.status_code == 200:
             print(f"SUCCESS: Answered Q{q1['question_id']}")
        else:
             print(f"FAILED to answer: {res.text}")
             
    except Exception as e:
        print(f"FAILED to save answers: {e}")

    # 4. Complete Assessment (Snapshot)
    print("\n4. Completing Assessment...")
    final_company_data = {
        "company_name": "Real Company Inc",
        "industry": "Finance",
        "number_of_employees": "51-200",
        "website": "example.com",
        "city": "Berlin",
        "email": "test@example.com"
    }
    try:
        res = requests.post(f"{BASE_URL}/responses/{response_id}/complete", json={
            "company_details": final_company_data
        })
        if res.status_code == 200:
            print("SUCCESS: Assessment Completed")
        else:
            print(f"FAILED: {res.text}")
            return
    except Exception as e:
         print(f"FAILED: {e}")
         return

    # 5. Get Results
    print("\n5. Fetching Results...")
    try:
        res = requests.get(f"{BASE_URL}/responses/{response_id}/results")
        if res.status_code == 200:
            results = res.json()
            print(f"SUCCESS: Got Results!")
            print(f"Total Score: {results['overall_score']}")
            print(f"Cluster: {results['cluster']['cluster_name']}")
        else:
            print(f"FAILED: {res.text}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_api_flow()
