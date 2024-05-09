from bs4 import BeautifulSoup
from requests import get
import json

def get_soup(html):
    return BeautifulSoup(html, "html.parser")


# Function to extract course data
def extract_courses(soup, semester_id):
    semester_data = []
    # Find the container for the semester
    semester = soup.find(id=semester_id)
    if semester:
        courses = semester.find_all("li")
        for course in courses:
            course_info = course.find("a")
            if course_info:
                course_data = {
                    "course_code": course_info.text.strip(),
                    "course_link": course_info.get("href", ""),
                    "course_name": (
                        course_info.next_sibling if course_info.next_sibling else ""
                    ),
                }
                semester_data.append(course_data)
    return semester_data


if __name__ == "__main__":
    # URL: https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci/#!accordion-1595938857886-full-time--four-year-program
    html = get(
        "https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci/#!accordion-1595938857886-full-time--four-year-program"
    ).text

    soup = get_soup(html)
    # Get Element with class name resTwoColEven
    print(soup.find(class_="resTwoColEven").prettify())

    # Initialize a BeautifulSoup object with the HTML content
    soup = soup.find(class_="resTwoColEven")

    # Define semesters based on div IDs or some structure in the HTML (you need to adjust these)
    semesters = {
        "1st Semester": extract_courses(soup, "17b4b785-7f06-4a40-9fd6-9292dbeb6a26"),
        "2nd Semester": extract_courses(soup, "f342e497-e591-4682-bf06-ca080f5b52ac"),
    }

    # Convert the dictionary to JSON
    json_data = json.dumps(semesters, indent=4)

    # Save the JSON data to a file
    with open("course_plan.json", "w") as json_file:
        json_file.write(json_data)

    print("JSON data saved to 'course_plan.json'")
