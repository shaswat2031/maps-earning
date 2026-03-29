import requests
import json
import os
import time
import csv
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")
BASE_URL = "https://serpapi.com/search?engine=google_maps"

if not API_KEY:
    print("[ERROR] SERP_API_KEY not found in .env file. Please add it first.")
    exit(1)

def get_maps_results(query, current_leads, start_index=0, max_results_this_batch=10):
    """
    Fetches a batch of Google Maps results.
    """
    new_leads = []
    current_start = start_index
    
    print(f"\n[INFO] Searching for leads (Starting at offset {current_start})...")
    
    while len(new_leads) < max_results_this_batch:
        params = {
            "q": query,
            "api_key": API_KEY,
            "start": current_start,
            "type": "search"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"[ERROR] API Connection failed: {e}")
            break
            
        if "local_results" not in data:
            print("[INFO] No more results available from Google Maps.")
            return new_leads, None # No more pages
            
        local_results = data.get("local_results", [])
        for place in local_results:
            # Skip if it has a website
            if "website" in place:
                continue
            
            # Skip if we already found this lead in a previous batch (rare but possible)
            place_id = place.get("place_id")
            if any(lead.get("Place ID") == place_id for lead in current_leads + new_leads):
                continue

            # Extract data
            name = place.get("title", "N/A")
            address = place.get("address", "N/A")
            phone = place.get("phone", "N/A")
            rating = place.get("rating", "N/A")
            reviews = place.get("reviews", 0)
            category = place.get("type", "N/A")
            
            new_leads.append({
                "Business Name": name,
                "Location": address,
                "Phone": phone,
                "Rating": rating,
                "Review Count": reviews,
                "Category": category,
                "Place ID": place_id,
                "Status": "Needs Website"
            })
            
            if len(new_leads) >= max_results_this_batch:
                break
        
        # Check if there is next page
        if "serpapi_pagination" in data and "next" in data["serpapi_pagination"]:
            current_start += 20
        else:
            return new_leads, None # End of results

    # Return the new leads and the next start offset
    return new_leads, current_start

def save_to_csv(data, filename):
    if not data:
        print("[WARNING] No leads to save.")
        return
        
    # Remove 'Place ID' from export for cleaner file
    export_data = []
    for item in data:
        clean_item = item.copy()
        clean_item.pop("Place ID", None)
        export_data.append(clean_item)

    keys = export_data[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(export_data)
        print(f"\n[SUCCESS] File saved: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[ERROR] Save failed: {e}")

def main():
    print("="*60)
    print("🚀 Google Maps Lead Scraper - Pro version by [AIDevLab]")
    print("="*60)
    
    business_type = input("Business type (e.g. Roofers): ").strip()
    city = input("Location (e.g. New York): ").strip()
    
    if not business_type or not city:
        print("[ERROR] Input missing.")
        return
        
    query = f"{business_type} in {city}"
    all_leads = []
    next_start = 0
    batch_size = 10
    
    while True:
        new_batch, next_start = get_maps_results(query, all_leads, start_index=next_start, max_results_this_batch=batch_size)
        all_leads.extend(new_batch)
        
        print(f"\n[INFO] Found {len(new_batch)} new leads in this batch.")
        print(f"[INFO] Total leads collected so far: {len(all_leads)}")
        
        if next_start is None:
            print("[INFO] No more search results available.")
            break
            
        choice = input("\nWould you like to fetch 10 more leads? (y/n): ").lower().strip()
        if choice != 'y':
            break
            
    # Final CSV export
    if all_leads:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"leads_{business_type.replace(' ', '_')}_{city.replace(' ', '_')}_{timestamp}.csv"
        save_to_csv(all_leads, filename)
        print(f"[INFO] Total leads exported: {len(all_leads)}")
    else:
        print("[INFO] No leads found matching your criteria.")

if __name__ == "__main__":
    main()
