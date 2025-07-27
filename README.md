# Research at UIUC Themes Generator and Classifier
## Authored by William Kulwin and Suvan Chatakondu

The UIUC Research Themes Generator is a website where two UIUC Departments can input Professors' research biographies and generate themes among the inputted professors and use those themes to classify new biographies into corresponding themes.

## ATLAS Project Documentation

===

Client Name: ATLAS ML/AI Team

Name of Direct Supervisor: Mike Sommers

Names of Team Members: Suvan Chatakondu, William Kulwin

Names of Contacts: Megan Fry

Tooks Utilized: VSCode, Python, Local UIUC LLM, UIUC VPN, Other AI Tools(ChatGPT, Gemini), Microsoft Tools(PowerPoint, Teams, Sharepoint, Outlook)

Communication: Microsoft Teams

Login/Password: Please obtain from your supervisor for the Local UIUC LLM

## Getting Started

===

#### Dependencies
- Python
- pandas (Python Library)
- gradio (Python Library)
- requests (Python Library)
- json (Python Library)
- dotenv (Python Library)
- os (Python Library)

Please pip install all of the python libraries to ensure the app works properly.

## Reflection

===

### Summary of this semester placement expectations: 
We were tasked with creating research themes for a combination of two departments based on professors' research biographies. We had to find a way to come up with encompassing themes for both departments. We would then have to use the resulting themes to classify new professors based on their biographies. We needed to figure out a way to automate this process using AI/ML and reduce the human classification aspect.

### Project Status Report:
1. Research Phase: We needed to figure out ways we wanted to implement this with Artificial Intelligence. What would be the most practical way, and how should we go about doing it?
2. AI Testing: We tested various prompts to see which ones worked the best in outputting the best themes based on the given descriptions.
3. Validation: We needed to make sure that what the LLMs were outputting was accurate. William manually checked and saw good results with the Local LLM.
4. MVP Creation: We finally made a UI for this and split the project into two: Training and Testing. The Generation would handle taking in all of the research bios and output 15 themes. The Classification would take in new descriptions and then classify them based on the 15 themes, outputting four themes that it thinks the description fits best.

### Future
These are the things we think would be next steps:
1. Block duplicate generations: If a combincation of departments already has a list of 15 themes, we don't want to create 15 new themes.
2. UI updates: It is avery basic application right now, we would hope for a more aesthetically pleasing app.
3. Logging Updates: As of right now, Logging is very basic and we don't know what to log, we hope that we can log the ifnoramtion in the proper way that the research team wants it
4. Add New Features: If there is anything else that needs to be added that we missed, that is something for the future as well.