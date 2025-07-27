import pandas as pd
import gradio as gr
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def llm(descriptions, dep1, dep2):
    try:
        url = os.getenv("URL")
        myobj = {
            "model": "gemma3:12b",
            "prompt": f"""Given the following descriptions, generate 15 not too broad, but also not too specific, themes that the professors embodied. The hope is that these themes can be extrapolated to classify other {dep1}/{dep2} professors, so make them very encompassing themes. Only output the 15 themes and nothing else and add a new line character after each theme.
            {descriptions}
            """,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(url, data=json.dumps(myobj), headers=headers, auth=(os.getenv("AUTH_USER"), os.getenv("AUTH_PASSWORD")), timeout=1000)
        output = response.json()['response']
        log_entry = {
            "department_1": dep1,
            "department_2": dep2,
            "themes_output": output
        }

        log_file = "theme_log.csv"
        file_exists = os.path.isfile(log_file)
        df = pd.DataFrame([log_entry])
        df.to_csv(log_file, mode='a', index=False, header=not file_exists)
        return output
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    



def get_unique_dept_combinations():
    log_file = "theme_log.csv"
    if not os.path.isfile(log_file):
        return []
    
    df_theme = pd.read_csv(log_file)
    df_theme["combo"] = df_theme["department_1"].astype(str) + " / " + df_theme["department_2"].astype(str)
    return sorted(df_theme["combo"].unique())





def classify_description(description, department_combo, professor_name, professor_dept):
    log_file = "theme_log.csv"
    if not os.path.isfile(log_file):
        return "No theme data available."

    df = pd.read_csv(log_file)
    df["combo"] = df["department_1"].astype(str) + " / " + df["department_2"].astype(str)
    row = df[df["combo"] == department_combo].head(1)

    if row.empty:
        return "No themes found for this department combination."

    themes_raw = row["themes_output"].values[0]

    prompt = f"""Below are 15 research themes that UIUC professors typically research as well as a UIUC professor's description. I want you to classify the UIUC professor into 4 of the themes based on their description. Don’t say anything else and add a new line character after each theme.

### Research Description:
{description}

### Department Themes:
{themes_raw}

Only output a numbered list of 4 selected themes.
"""

    try:
        url = os.getenv("URL")
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "model": "gemma3:12b",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            auth=(os.getenv("AUTH_USER"), os.getenv("AUTH_PASSWORD")),
            timeout=1000
        )

        llm_response = response.json().get("response", "No response received from LLM.")

        log_entry = {
            "professor_name": professor_name,
            "professor_department": professor_dept,
            "classified_themes": llm_response
        }

        class_log_file = "classification_log.csv"
        file_exists = os.path.isfile(class_log_file)
        pd.DataFrame([log_entry]).to_csv(class_log_file, mode='a', index=False, header=not file_exists)

        return llm_response

    except Exception as e:
        return f"Error calling LLM: {e}"







with gr.Blocks() as demo:
    gr.Markdown("# Professor Research Topics at UIUC")
    with gr.Tab("Themes Generation"):
        with gr.Row():
            with gr.Column():
                dep1 = gr.Textbox(label="Department 1")
            with gr.Column():
                dep2 = gr.Textbox(label="Department 2")
        descriptions = gr.Textbox(label="Input all Professor Research Descriptions", lines=4, placeholder="Paste the research summaries here...")
        find_button = gr.Button("Submit", variant="primary")
        outputted_themes = gr.Textbox(label="Themes:", lines = 15)
        find_button.click(
            fn=llm,
            inputs=[descriptions, dep1, dep2],
            outputs=[outputted_themes],
        )
    with gr.Tab("Themes Classification"):
        with gr.Row():
            dept_dropdown = gr.Dropdown(
                label="Select Department Combination",
                choices=get_unique_dept_combinations()
            )
            refresh_btn = gr.Button("Refresh Department Combinations", scale=0)
            refresh_btn.click(
                fn=lambda: gr.update(choices=get_unique_dept_combinations()),
                outputs=dept_dropdown
            )
        
        with gr.Row():
            with gr.Column():
                dep1 = gr.Textbox(label="Professor Name")
            with gr.Column():
                dep2 = gr.Textbox(label="Department")
        new_description = gr.Textbox(
            label="New Research Description",
            lines=4,
            placeholder="Paste the research summary here..."
        )

        classify_btn = gr.Button("Classify into 4 Themes", variant="primary")
        classification_result = gr.Textbox(label="Top 4 Themes", lines = 4)

        classify_btn.click(
            fn=classify_description,
            inputs=[new_description, dept_dropdown, dep1, dep2],
            outputs=classification_result
        )
        



demo.launch()