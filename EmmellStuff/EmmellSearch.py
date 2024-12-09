import os
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urljoin, urlparse

def fetch_and_save(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
        filename = os.path.join(folder, url.replace("http://", "").replace("https://", "").replace("/", "_") + ".html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

def get_all_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        # Only add links within the same domain
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return links

def crawl_website(base_url, folder, max_depth=2):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    visited = set()
    graph = nx.DiGraph()
    
    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return
        print(f"Crawling: {url}")
        visited.add(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            fetch_and_save(url, folder)
            graph.add_node(url)
            links = get_all_links(base_url, response.text)
            for link in links:
                graph.add_edge(url, link)
                crawl(link, depth + 1)
        except Exception as e:
            print(f"Failed to process {url}: {e}")
    
    crawl(base_url, 0)
    return graph

def visualize_graph(graph, output_file="sitemap.png"):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=50, font_size=8)
    plt.savefig(output_file)
    plt.show()
    print(f"Saved graph visualization as {output_file}")

if __name__ == "__main__":
    base_url = "http://dev.emmell.org/example"
    output_folder = "website_files"
    max_crawl_depth = 10

    print(f"Starting crawl of {base_url}...")
    site_graph = crawl_website(base_url, output_folder, max_depth=max_crawl_depth)
    print("Crawl completed. Visualizing sitemap...")
    visualize_graph(site_graph)
