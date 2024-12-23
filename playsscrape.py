import requests
import re
import time


def parse_files():
    parse_list_of_urls("3 Parsed Urls")
    parse_list_of_urls("3b Parsed Urls")

def parse_list_of_urls(filename):
    with open(filename + ".txt", "r") as infile, open(filename + ".output" + ".txt", "w") as outfile:
        for line in infile:
            print(line)
            video_url = get_page_source(source=line)
            time.sleep(1)
            outfile.write(video_url + "\n")
    print(f"Processing complete. Check {filename}.output.txt")

def get_page_source(quality=720,
                    source="https://web.archive.org/web/20191210100723/https://plays.tv/video/5b768fcfa003e8f045/ya-just-got-milled-son-"):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(source, headers=headers)
    # Check if the request was successful (status code 200)
    if r.status_code == 200:
        # Print the HTML source code
        page_source = r.text

        lines = page_source.splitlines()

        line_number = 130
        pattern = fr'src="\/\/[/a-zA-z.0-9:-]*720.mp4'
        
        if len(lines) >= line_number:
            specific_line = lines[line_number - 1]
            #print(f"Line {line_number}: {specific_line}")

            match = re.search(pattern, specific_line)
            url = match.group().lstrip('src="//')

            if match:
                print(f"Url found: {url}")
                return url
            else:
                print("No match found.")
                        
        else:
            print(f"The page source has only {len(lines)} lines.")
        
        #720.mp4" type="video/mp4">
        
    else:
        print('Failed to retrieve the webpage. Status code:', response.status_code)
