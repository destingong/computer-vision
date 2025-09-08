# import statements
import streamlit as st
import PIL
from PIL import Image
# import helpers
import time
import pandas as pd
from transformers import pipeline
# from IPython.display import display, HTML

# configure page layout - title, page icon, description
def initialize_page():
    """Initialize the Streamlit page configuration and layout"""
    st.set_page_config(
        page_title="Computer Vision",
        page_icon="🤖",
        layout="centered"
    )
    st.title("Computer Vision Tasks")
    content_block = st.columns(1)[0]

    return content_block

# define app functions
# 0. prompt user to upload their own image (with a default image pre-displayed)
def get_uploaded_image():

    uploaded_file = st.file_uploader(
        "Upload your own image", 
        accept_multiple_files=False,
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Preview', use_container_width=False)

    else:
        image = None

    return image


# 1. select task (allow multi-select) - parameter "task"
def get_selected_task():
    options = st.multiselect(
        "Which tasks would you like to perform?",
        [
            "visual-question-answering",
            "image-to-text",
            "image-classification",
            "image-segmentation",
        ],
        max_selections=4,
        accept_new_options=True,
    )

    #prompt for question input if the task is 'VQA' and 'DocVQA' - parameter "question"
    if 'visual-question-answering' in options or 'document-question-answering' in options:
        question = st.text_input(
            "Please enter your question:"
        )
        
    elif "Other (specify task name)" in options:
        task = st.text_input(
            "Please enter the task name:"
        )
        options = task
        question = ""
        
    else:
        question = ""

    return options, question

# 2. allow user to choose their own model - parameter "model"
def get_selected_model():
    options = ["Use the default model", "Use your selected HuggingFace model"]
    selected_option = st.selectbox("Choose an option:", options)
    if selected_option == "Use your selected HuggingFace model":
        model = st.text_input(
            "Please enter your selected HuggingFace model id:"
        )
    else:
        model = None

    return model
    

# 4. display multiple results in a table format
def display_results(image, task_list, user_question, model):

    results = []
    # st.write(task_list)
    for task in task_list:
        if task in ['visual-question-answering', 'document-question-answering']:
            params = {'question': user_question}
        else:
            params = {}
            
        row = {
            'task': task,
        }
        
        if model != None:
            # model = i['model']
            # row['model'] = model
            pipe = pipeline(task, model=model)

        else:
            pipe = pipeline(task)
            
        row['model'] = pipe.model.name_or_path
        start_time = time.time()
        output = pipe(
            image,
            **params
        )
        execution_time = time.time() - start_time
        
        row['model_type'] = pipe.model.config.model_type
        row['time'] = execution_time
        

        # display image segentation visual output
        if task == 'image-segmentation':
            output_masks = [i['mask'] for i in output]

        row['output'] = str(output)
        
        results.append(row)
        results_df = pd.DataFrame(results)
        
    st.write('Model Responses')
    # st.dataframe(
    #     results_df
    # )
    st.table(results_df)

    if 'image-segmentation' in task_list:
        st.write('Segmentation Mask Output')
        
        for m in output_masks:
            st.image(m)
    
    return results_df


# define the main function that calls the functions above
def main():
    initialize_page()
    image = get_uploaded_image()
    task_list, user_question = get_selected_task()
    model = get_selected_model()
    
    # generate reponse spinning wheel
    if st.button("Generate Response", key="generate_button"):
        display_results(image, task_list, user_question, model)

# run the app
if __name__ == "__main__":
    main()
