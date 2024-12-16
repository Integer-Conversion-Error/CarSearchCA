import requests
import json
import re

def fetch_autotrader_data(address, make, model, price_min, price_max, top=15, is_new=True, is_used=True, with_photos=True):
    """
    Continuously fetch data from AutoTrader.ca API with lazy loading (pagination).

    Args:
        address (str): Location for the search (e.g., "Kanata, ON").
        make (str): Car make (e.g., "Tesla").
        model (str): Car model (e.g., "Model 3").
        price_min (int): Minimum price.
        price_max (int): Maximum price.
        top (int): Number of results per page.
        is_new (bool): Include new cars in the search.
        is_used (bool): Include used cars in the search.
        with_photos (bool): Only return listings with photos.

    Returns:
        list: Combined list of all results from all pages.
    """
    # Define the URL
    url = "https://www.autotrader.ca/Refinement/Search"
    
    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # Combined results
    all_results = []
    current_page = 1
    max_page = None  # Will be determined dynamically
    skip = 0

    while True:
        # Define the payload with pagination
        payload = {
            "Address": address,
            "Make": make,
            "Model": model,
            "PriceMin": price_min,
            "PriceMax": price_max,
            "Skip": skip,
            "Top": top,
            "IsNew": is_new,
            "IsUsed": is_used,
            "WithPhotos": with_photos,
            "micrositeType": 1,
        }

        try:
            # Send the POST request
            response = requests.post(url, headers=headers, json=payload)
            
            # Raise an error if the response status code is not 200
            response.raise_for_status()
            
            # Parse the JSON response
            json_response = response.json()
            
            # Extract SearchResultsDataJson and decode
            search_results_json = json_response.get("SearchResultsDataJson", "")
            if not search_results_json:
                print("No more data available.")
                break  # Stop if no data is returned
            
            # Decode the JSON string
            search_results = json.loads(search_results_json)

            # Append results
            all_results.extend(search_results.get("compositeIdUrls", []))

            # Update pagination info
            current_page = search_results.get("currentPage", 0)
            max_page = search_results.get("maxPage", current_page)

            # Print progress
            print(f"Fetched page {current_page} of {max_page}...")

            # Check if we've reached the last page
            if current_page >= max_page:
                print("Reached the last page.")
                break
            
            # Increment skip for the next page
            skip += top
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Failed to decode SearchResultsDataJson: {e}")
            break

    return all_results

def remove_duplicates(arr):
    """
    Removes duplicates from an array while maintaining the order of elements.

    Args:
        arr (list): The input array.

    Returns:
        list: A new array with duplicates removed.
    """
    seen = set()
    result = []
    for item in arr:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result

# Example usage
if __name__ == "__main__":
    results = fetch_autotrader_data(
        address="Kanata, ON",
        make="Tesla",
        model="Model 3",
        price_min=3000,
        price_max=35000
    )
    
    results = remove_duplicates(results)

    for item in results:
        print(item)
    print(f"Total Results Fetched: {len(results)}")
    #print(results)

