import requests
import pytest

BASE_URL = "https://reqres.in/api"

class TestReqResAPI:

    def test_get_users(self):
        print("\n--- Starting test: GET Users ---")
        print("Step 1: Performing GET request to list users from page 2")
        response = requests.get(f"{BASE_URL}/users?page=2")
        
        print(f"Step 2: Validating status code. Received: {response.status_code}")
        assert response.status_code == 200
        
        print("Step 3: Validating response body structure")
        data = response.json()
        assert "data" in data
        assert "page" in data
        assert len(data["data"]) > 0
        
        print(f"Result: GET request successful, found {len(data['data'])} users")

    def test_post_create_user(self):
        print("\n--- Starting test: POST Create User ---")
        print("Step 1: Preparing payload for new user")
        payload = {
            "name": "morpheus",
            "job": "leader"
        }
        
        print("Step 2: Performing POST request to create user")
        response = requests.post(f"{BASE_URL}/users", json=payload)
        
        print(f"Step 3: Validating status code. Received: {response.status_code}")
        assert response.status_code == 201
        
        print("Step 4: Validating created user details in response")
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["job"] == payload["job"]
        assert "id" in data
        assert "createdAt" in data
        
        print(f"Result: POST request successful, user created with id: {data['id']}")

    def test_put_update_user(self):
        print("\n--- Starting test: PUT Update User ---")
        print("Step 1: Preparing payload for full user update")
        payload = {
            "name": "morpheus",
            "job": "zion resident"
        }
        
        print("Step 2: Performing PUT request to update user with id 2")
        response = requests.put(f"{BASE_URL}/users/2", json=payload)
        
        print(f"Step 3: Validating status code. Received: {response.status_code}")
        assert response.status_code == 200
        
        print("Step 4: Validating updated user details")
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["job"] == payload["job"]
        assert "updatedAt" in data
        
        print("Result: PUT request successful, user details fully updated")

    def test_patch_update_user(self):
        print("\n--- Starting test: PATCH Partial Update User ---")
        print("Step 1: Preparing payload for partial job update")
        payload = {
            "job": "zion resident"
        }
        
        print("Step 2: Performing PATCH request to update job for user with id 2")
        response = requests.patch(f"{BASE_URL}/users/2", json=payload)
        
        print(f"Step 3: Validating status code. Received: {response.status_code}")
        assert response.status_code == 200
        
        print("Step 4: Validating updated field")
        data = response.json()
        assert data["job"] == payload["job"]
        assert "updatedAt" in data
        
        print("Result: PATCH request successful, job field partially updated")

    def test_delete_user(self):
        print("\n--- Starting test: DELETE User ---")
        print("Step 1: Performing DELETE request for user with id 2")
        response = requests.delete(f"{BASE_URL}/users/2")
        
        print(f"Step 2: Validating status code. Received: {response.status_code}")
        # ReqRes returns 204 No Content for successful deletions
        assert response.status_code == 204
        
        print("Result: DELETE request successful, user removed")
