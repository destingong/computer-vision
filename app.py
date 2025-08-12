# import statements
import streamlit as st


# configure page layout - title, page icon, description
def initialize_page():
    """Initialize the Streamlit page configuration and layout"""
    st.set_page_config(
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
    
    image = Image.open(uploaded_file)

    #TODO: (with a default image pre-displayed)

    return image


# 1. select task (allow multi-select) - parameter "task"
def get_selected_task():
    options = st.multiselect(
        "Which tasks would you like to perform?",
        [
            "visual-question-answering", 
            "document-question-answering", 
            "image-classification",
            "image-segmentation",

        ],
        max_selections=4,
        accept_new_options=False,
    )

    st.write("You selected:", options)

    # TODO: prompt for question input if the task is 'VQA' and 'DocVQA' - parameter "question"
    if 'visual-question-answering' in options or 'document-question-answering' in options:
        question = st.text_input(
            "Please enter your question:"
        )
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

# 3. collect all pipeline results



# 4. display multiple results in a table format
def display_results():

    image = get_uploaded_image()
    task_list, user_question = get_selected_task()
    model = get_selected_model()

    for task in task_list:
        params = {'question': user_question}
        ## TODO: add model type
        row = {
            'task': task,
            'params': params,
            # 'model type': model_type
            }

        try:
            model = i['model']
            row['model'] = model
            pipe = pipeline(task, model=model)
            st.write(f'Using user selected model {model}')
            
        except Exception as e:
            st.write('Using default model ...')
            pipe = pipeline(task)
            row['model'] = pipe.model.name_or_path

        start_time = time.time()
        output = pipe(
            image, 
            **params
        )
        execution_time = time.time() - start_time

        row['time'] = execution_time
        row['output'] = output

        # display image segentation visual output
        if task == 'image-segmentation':
            helpers.display_segmentation()
        
        results.append(row)
        results_df = pd.DataFrame(results)

    helpers.display_comparison_results(results_df)

    return results_df


def display().image_outputs():
    helpers.display_segmentation()

# define the main function that calls the functions above
def main():

    # generate reponse spinning wheel

    display_results()


# run the app

