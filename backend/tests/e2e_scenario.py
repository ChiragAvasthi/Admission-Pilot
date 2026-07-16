import asyncio
import httpx
import json

API_URL = "http://localhost:8000/api/v1"

async def run_e2e_scenario():
    print("Starting End-to-End Scenario...")
    async with httpx.AsyncClient(base_url=API_URL, timeout=30.0) as client:
        # 1. Create Organization
        print("1. Creating Organization...")
        org_data = {"name": "MITRC Engineering College", "description": "Tech college"}
        res = await client.post("/organizations/", json=org_data)
        if res.status_code == 400:
            print("Org already exists, fetching existing...")
            res = await client.get("/organizations/")
            org_id = res.json()[0]["id"]
        else:
            org_id = res.json()["id"]
        print(f"   Org ID: {org_id}")

        # 2. Create Project
        print("2. Creating Project...")
        proj_data = {
            "organization_id": org_id,
            "name": "2026 Admissions Drive",
            "description": "Increase CS enrollments",
            "website_url": "https://mitrc.ac.in"
        }
        res = await client.post("/projects/", json=proj_data)
        proj_id = res.json()["id"]
        print(f"   Project ID: {proj_id}")

        # 3. Simulate Upload (skip actual multipart for script brevity, just start execution)
        print("3. Starting Execution...")
        exec_data = {"project_id": proj_id}
        res = await client.post("/execution/", json=exec_data)
        exec_id = res.json()["id"]
        print(f"   Execution ID: {exec_id}")

        # 4. Monitor Progress
        print("4. Monitoring Progress (WebSocket Simulation)...")
        # In a real script we would connect a WS client. Here we poll the API for completion.
        status = "running"
        for _ in range(10):
            await asyncio.sleep(2)
            res = await client.get(f"/execution/{exec_id}")
            if res.status_code == 200:
                status = res.json()["status"]
                print(f"   Status: {status}")
                if status in ["completed", "failed"]:
                    break
        
        if status != "completed":
            print("   Execution failed or timed out.")
            return

        # 5. Fetch Report
        print("5. Fetching Reports...")
        res = await client.get(f"/reports/?project_id={proj_id}")
        reports = res.json()
        if reports:
            print(f"   Found {len(reports)} reports. Title: {reports[0]['title']}")
        else:
            print("   No reports generated yet (Simulated execution).")
            
        print("End-to-End Scenario Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(run_e2e_scenario())
