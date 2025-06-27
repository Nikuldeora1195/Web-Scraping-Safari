import requests
from bs4 import BeautifulSoup
import csv

def scrape_github_trending():
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find repository articles
        repos = soup.find_all('article', class_='Box-row')[:5]
        repo_data = []
        
        for repo in repos:
            # Get repository name
            name_tag = repo.find('h2', class_='h3 lh-condensed')
            if name_tag and name_tag.a:
                repo_name = name_tag.a.text.strip().replace('\n', '').replace(' ', '')
                repo_link = 'https://github.com' + name_tag.a['href']
                repo_data.append({'name': repo_name, 'link': repo_link})
        
        # Write to CSV
        with open('trending_repos.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['repository_name', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for repo in repo_data:
                writer.writerow({'repository_name': repo['name'], 'link': repo['link']})
                
        print("Successfully scraped and saved top 5 trending repositories to trending_repos.csv")
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    scrape_github_trending()