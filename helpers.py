from IPython.display import display, HTML, Markdown
import pandas as pd

def display_comparison_results(df: pd.DataFrame):
    """
    Display the comparison results in a formatted table
    
    Args:
        df (pd.DataFrame): DataFrame containing the comparison results
    """
    # Style the DataFrame
    styled_df = df.style.set_properties(**{
        'text-align': 'left',
        'white-space': 'pre-wrap'
    }).set_table_styles([
        {'selector': 'th',
         'props': [
                  ('text-align', 'left'),
                  ('font-family', 'monospace'),
                  ('padding', '8px')]},
                  
        {'selector': 'td',
         'props': [('padding', '8px')]}
    ])
    
    display(HTML(styled_df.to_html()))

def display_segmentation(output):
    output_labels = [i['label'] for i in output]
    output_masks = [i['mask'] for i in output]
    
    st.write(output_labels)
    for m in output_masks:
        # display(m)
        st.write(output_masks)
        
    return output_labels