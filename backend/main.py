# from fastapi import FastAPI, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from bs4 import BeautifulSoup
# import requests
# import time
# from typing import List, Dict
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5174"],  # React app's address
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global variable to store scraped data
# scraped_data: List[Dict[str, str]] = []

# def scrape_wellfound(keyword: str):
#     global scraped_data
#     url = f"https://wellfound.com/jobs?q={keyword}"

#     # Set up Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')  # Run in headless mode
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     try:
#         print(f"Initializing Chrome WebDriver for URL: {url}")
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get(url)

#         # Wait for the content to load
#         wait = WebDriverWait(driver, 10)
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'styles_component__UCLp3')))

#         # Get the page source after JavaScript has loaded
#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'html.parser')
#         print("Parsing HTML content...")

#         # Find all job listings
#         all_links = soup.find_all('a', class_='styles_component__UCLp3')
#         print(f"Found {len(all_links)} company links")

#         # Clear existing data
#         scraped_data.clear()

#         for link in all_links:
#             try:
#                 company_element = link.find('div', class_='styles_company__NfHNO')
#                 title_element = link.find('div', class_='styles_title__jWi_d')
#                 location_element = link.find('div', class_='styles_location__btYYi')

#                 company = company_element.text.strip() if company_element else "Unknown Company"
#                 title = title_element.text.strip() if title_element else "Unknown Title"
#                 location = location_element.text.strip() if location_element else "Unknown Location"
#                 job_url = "https://wellfound.com" + link.get('href', '')

#                 job_data = {
#                     "company": company,
#                     "title": title,
#                     "location": location,
#                     "url": job_url
#                 }
#                 scraped_data.append(job_data)

#             except Exception as e:
#                 print(f"Error processing job listing: {str(e)}")
#                 continue

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         scraped_data.clear()
#         scraped_data.append({"company": f"Error fetching data: {str(e)}"})
        
#     finally:
#         try:
#             driver.quit()
#         except:
#             pass
            
#     print(f"Scraped {len(scraped_data)} jobs")
#     return

# @app.post("/scrape")
# async def scrape(background_tasks: BackgroundTasks):
#     background_tasks.add_task(scrape_wellfound, "python")
#     return {"message": "Scraping started"}

# @app.get("/results")
# async def get_results():
#     return {"data": scraped_data}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import time
from typing import List, Dict

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store scraped data
scraped_data: List[Dict[str, str]] = []

def scrape_wellfound(keyword: str):
    global scraped_data
    url = f"https://wellfound.com/jobs?q={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs = soup.find_all(id='main') 
    
    # Clear the global scraped_data list
    scraped_data.clear()
    
    for job in jobs:
        try:
            # Extract all 'a' tags with the target class
            companies = job.find_all('a', class_='styles_component__UCLp3')
            company_names = [company.text.strip() for company in companies if company.text.strip()]  # Extract text and ignore empty strings
            
            plain_text_span = container.find("span", class_=False)
            plain_text = plain_text_span.text.strip() if plain_text_span else ""

            # Get the span with class 'text-gray-700'
            gray_text_span = container.find("span", class_="text-gray-700")
            gray_text = gray_text_span.text.strip() if gray_text_span else ""

            # Check for distinguishing factors (e.g., "dot" in text)
            if "•" in plain_text and "•" in gray_text:
                # Only save data if both fields contain a distinguishing sign
                scraped_data.append({
                    "job_title": job_title,
                    "company_Name": plain_text,
                    "additional_info": gray_text
                })
            
            # Combine companies and titles if both exist
            for company in company_names:
                scraped_data.append({
                    "company": company,
                    "title": title,
                    "info": info,
                })
        except Exception as e:
            print(f"Error parsing job: {e}")

    print(f"Scraped {len(scraped_data)} jobs")
    time.sleep(2)  # Simulate longer process

@app.post("/scrape")
async def scrape(background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_wellfound, "python")
    return {"message": "Scraping started"}

@app.get("/results")
async def get_results():
    return {"data": scraped_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)