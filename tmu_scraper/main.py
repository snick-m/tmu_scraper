from bs4 import BeautifulSoup, NavigableString, PageElement, ResultSet, Tag
from requests import get
import json, re


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


# Function to extract course data
def extract_courses(soup: BeautifulSoup, semester_id):
    semester_data = []
    # Find the container for the semester
    semester = soup.find(id=semester_id)
    if semester:
        courses: ResultSet[Tag] = semester.find_all("li")
        for course in courses:
            course_info = course.find("a")
            if course_info:
                course_data = {
                    "course_code": course_info.text.strip(),
                    "course_link": course_info.get("href", ""),
                    "course_name": (
                        course_info.next_sibling.text.strip()
                        if course_info.next_sibling
                        else ""
                    ),
                }
                semester_data.append(course_data)
    return semester_data

def checkClassNotContains(class_name: str, *extra_checks):
    def inner(tag: Tag) -> bool:
        return class_name not in tag.get("class", []) and all(check (tag) for check in extra_checks)
    return inner

def checkChildAbsent(tag_name: str, *extra_checks):
    def inner(tag: Tag) -> bool:
        return tag.find(tag_name) is None and all(check(tag) for check in extra_checks)
    return inner

if __name__ == "__main__":
    # URL: https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci
    html = get(
        "https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci"
    ).text

    soup = get_soup(html)

    # Get the course plan container
    # Find the H2 tag that contains the text "Semester", then get the parent of the parent of the H2 tag
    try:
        program_container: Tag = list(
            soup.find_all("h2", string=re.compile("Semester"))[0].parents
        )[2]
    except IndexError:
        print("Could not find the program container")
        exit()

    section_titles: ResultSet[Tag] = program_container.find_all("div", class_="resTitle section") # find all div tags with class "resTitle section"
    sections: list[ResultSet[Tag]] = []
    for title in section_titles:
        section_elems = title.find_next_siblings(checkClassNotContains("resTitle", checkChildAbsent("img"))) # All siblings until next title and excluding images (horizontal lines)
        section_elems.insert(0, title)
        sections.append(section_elems)
    
    # Extract text info
    for section in sections:
        print("\n")
        title = section[0].text.strip()
        print(title)
        if "resText" in section[1].get("class"):
            print('\t', section[1].text.strip())
        cols = [elem for elem in section[1:] if "resTwoColEven" in elem.get("class")][0]
        if cols.find(string=re.compile("REQUIRED", re.IGNORECASE)):
            for col in cols.find_all("li"):
                print('\t', col.text.strip())
        else:
            for col in cols.find_all("p"):
                print('\t', col.text.strip())


        

    # # Initialize a BeautifulSoup object with the HTML content
    # soup = soup.find(class_="resTwoColEven")

    # # Define semesters based on div IDs or some structure in the HTML (you need to adjust these)
    # semesters = {
    #     "1st Semester": extract_courses(soup, "17b4b785-7f06-4a40-9fd6-9292dbeb6a26"),
    #     "2nd Semester": extract_courses(soup, "f342e497-e591-4682-bf06-ca080f5b52ac"),
    # }

    # # Convert the dictionary to JSON
    # json_data = json.dumps(semesters, indent=4)

    # # Save the JSON data to a file
    # with open("course_plan.json", "w") as json_file:
    #     json_file.write(json_data)

    # print("JSON data saved to 'course_plan.json'")
