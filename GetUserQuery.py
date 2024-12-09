import CarDataCollector

def read_query_file(file_path="querydetails.txt"):
    """
    Reads the query file and extracts the details.

    Args:
        file_path (str): Path to the query file.

    Returns:
        tuple: Contains make (str), model (str), price_min (int), price_max (int),
               max_pages (int), max_distance (float), and keywords (list).
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Initialize variables to extract details
    make = ""
    model = ""
    price_min = 0
    price_max = 0
    max_pages = 0
    max_distance = 0.0
    keywords = []

    # Parse each line
    for line in lines:
        if line.startswith("Make:"):
            make = line.split(":", 1)[1].strip()
        elif line.startswith("Model:"):
            model = line.split(":", 1)[1].strip()
        elif line.startswith("Price Min:"):
            price_min = int(float(line.split("$")[1].strip()))
        elif line.startswith("Price Max:"):
            price_max = int(float(line.split("$")[1].strip()))
        elif line.startswith("Max Pages:"):
            max_pages = int(line.split(":")[1].strip())
        elif line.startswith("Distance:"):
            max_distance = int(line.split(":")[1].strip().replace("km", "").strip())
        elif line.startswith("Keywords:"):
            keywords = [kw.strip() for kw in line.split(":", 1)[1].strip().split(",")]

    return make, model, price_min, price_max, max_pages, max_distance, keywords


# Example usage
if __name__ == "__main__":
    result = read_query_file()
    print(result)


def create_query_file():
    # Open a new file named querydetails.txt for writing
    with open("querydetails.txt", "w") as file:
        # Get car make
        all_makes = CarDataCollector.get_makes_from_autotrader()
        print(all_makes)
        make = ""
        model = -2
        while make == "" or make not in all_makes: 
            make = input("Enter make of car: ")
            if make not in all_makes and make != "":
                make = input("Please enter a valid car maker: ")
                

        file.write(f"Make: {make}\n")
        
        # Get car model
        modelsformake = CarDataCollector.get_models_from_autotrader(make)
        for index, modelformake in enumerate(modelsformake):
            print(f"{index}: {modelformake}")

        while True:
            try:
                model = int(input("Select model ID of car: ").strip())
                if 0 <= model < len(modelsformake):
                    model = modelsformake[model]
                    break
                else:
                    print(f"Invalid index. Please choose a number between 0 and {len(modelsformake) - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid input.")



        file.write(f"Model: {model}\n")
        
        # Get and validate minimum price
        while True:
            try:
                price_min = float(input("Enter min price ($): ").strip())
                if price_min < 0:
                    print("Minimum price cannot be negative. Try again.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid numeric value for min price.")
        file.write(f"Price Min: ${price_min:.2f}\n")
        
        # Get and validate maximum price
        while True:
            try:
                price_max = float(input("Enter max price ($): ").strip())
                if price_max < price_min:
                    print("Maximum price cannot be less than minimum price. Try again.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid numeric value for max price.")
        file.write(f"Price Max: ${price_max:.2f}\n")
        
        # Get and validate max_pages
        while True:
            try:
                max_pages = int(input("Enter amount of pages to search (each page is 15 listings, enter -1 for unlimited): ").strip())
                if max_pages < -1:
                    print("Invalid input. Pages cannot be less than -1. Try again.")
                else:
                    if max_pages == -1:
                        max_pages = 999
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer for pages.")
        file.write(f"Max Pages: {max_pages}\n")

        while True:
            try:
                max_distance = int(input("Enter maximum distance from Kanata (Enter -1 for nationwide search): "))
                if max_distance < -1 or max_distance == 0:
                    print("Invalid input. Distance cannot be less than -1 or equal 0. Try again.")
                else:
                    break
                
            except ValueError:
                print("Invalid input. Distance cannot be less than -1 or equal 0 ")

        file.write(f"Distance: {max_distance}\n")

        # Get keywords from user
        keywords = get_keywords_from_user()
        file.write(f"Keywords: {', '.join(keywords)}\n")

        print("Query details successfully saved to 'querydetails.txt'.")

        make = make.replace(" ","%20")
        make = make.lower()
        model = model.replace(" ", "%20")
        model = model.lower()

        return make,model,int(price_min),int(price_max),max_pages,max_distance,keywords


def get_keywords_from_user():
    """
    Allows the user to input keywords and manage them through a menu system.
    Returns a list of keywords.
    """
    keywords = []

    print("Enter keywords one by one. Press -1 to stop entering keywords.")
    while True:
        keyword = input("Enter a keyword: ").strip()
        if keyword == '-1':
            break
        if keyword:
            keywords.append(keyword)

    while True:
        print("\nCurrent keywords:", ", ".join(keywords) if keywords else "None")
        print("Menu:")
        print("1. Add a keyword")
        print("2. Remove a keyword")
        print("3. Finish")

        choice = input("Choose an option (1, 2, or 3): ").strip()
        if choice == '1':
            new_keyword = input("Enter a new keyword to add: ").strip()
            if new_keyword:
                keywords.append(new_keyword)
        elif choice == '2':
            keyword_to_remove = input("Enter a keyword to remove: ").strip()
            if keyword_to_remove in keywords:
                keywords.remove(keyword_to_remove)
            else:
                print("Keyword not found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    return keywords

def use_previous_or_new_query():
    """
    Prompts the user to use the previous query or create a new query.

    Returns:
        tuple: Contains make (str), model (str), price_min (int), price_max (int),
               max_pages (int), max_distance (float), and keywords (list).
    """
    try:
        # Try to read the previous query file
        previous_query = read_query_file()
        print("\nPrevious Query Details:")
        print(f"Make: {previous_query[0]}")
        print(f"Model: {previous_query[1]}")
        print(f"Price Min: ${previous_query[2]}")
        print(f"Price Max: ${previous_query[3]}")
        print(f"Max Pages: {previous_query[4]}")
        print(f"Distance: {previous_query[5]} km")
        print(f"Keywords: {', '.join(previous_query[6])}")
    except FileNotFoundError:
        # If no previous query file exists
        print("\nNo previous query found. You will need to create a new query.")
        create_query_file()
        return read_query_file()

    # Prompt the user to use the previous query or create a new one
    while True:
        choice = input("\nDo you want to use the previous query? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Using the previous query.")
            return previous_query
        elif choice == "no":
            print("Creating a new query.")
            create_query_file()
            return read_query_file()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    make,model,price_min,price_max,max_pages,max_distance,exclusions = use_previous_or_new_query()

    make = make.replace(" ","%20")
    make = make.lower()
    model = model.replace(" ", "%20")
    model = model.lower()

    modified_url = f"https://www.autotrader.ca/cars/{make}/{model}/?rcp=15&rcs=0&srt=35&pRng={price_min}%2C{price_max}&prx={max_distance}&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

    search_url = modified_url##"https://www.autotrader.ca/cars/tesla/model%203/?rcp=15&rcs=0&srt=35&pRng=3000%2C35000&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

    print("Search URL: ",search_url)
    print("Exclusion Keywords: ",exclusions)

    return search_url, max_pages, exclusions

# while True:
#     main()
#     break