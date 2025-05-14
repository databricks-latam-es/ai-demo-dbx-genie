###
# Databricks Streamlit App
# 
# Author: @alberto.murguia
# Revision: 1.0
# 
# This script implements an experimental chatbot that interacts with Databricks' Genie API,
# which is currently in Public Preview. The bot facilitates conversations with Genie,
# Databricks' AI assistant, through a chat interface.
# 
# Note: This is experimental code and is not intended for production use.
###
from helper_functions import *

# Initialize session state variables
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# Set the title and description of the Streamlit app
st.title("🧞‍♂️ Apps on Databricks with AI")
st.markdown(
    "ℹ️ This is a simple app example. See "
    "[Databricks docs](https://docs.databricks.com/aws/en/genie/conversation-api) "
    "for a more comprehensive about how to use the Genie Conversation API to integrate Genie into your applications"
)
st.markdown(
    "ℹ️ For a working demo of Genie, see "
    "[Databricks AI/BI: Marketing Campaign Effectiveness with Dashboards and Genie](https://www.databricks.com/resources/demos/tutorials/aibi-genie-marketing-campaign-effectiveness?itm_data=demo_center)."
)
st.markdown(
    "🤖 author: @alberto.murguia"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize conversation_id
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set Databricks host, space ID, and token
databricks_host = os.getenv('DATABRICKS_HOST')
assert databricks_host, 'DATABRICKS_HOST must be set in app.yaml.'

databricks_token = os.getenv('DATABRICKS_TOKEN')
assert databricks_token, 'DATABRICKS_TOKEN must be set in app.yaml.'

space_id = os.getenv('GENIE_SPACE_ID')
assert space_id, 'GENIE_SPACE_ID must be set in app.yaml.'

# Accept user input
if prompt := st.chat_input("Ask your question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Check if conversation_id exists in session state
        if st.session_state.conversation_id is None:
            conversation_id = start_conversation(databricks_host, databricks_token, space_id)
            if isinstance(conversation_id, str):
                st.session_state.conversation_id = conversation_id
            else:
                st.error("Failed to start conversation.")
                conversation_id = None
        else:
            conversation_id = st.session_state.conversation_id

        if conversation_id:
            try:
                result = ask_question(databricks_host, databricks_token, space_id, conversation_id, prompt)
                if result["sql_query_result"] is None:
                    assistant_response = result["content"]
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    assistant_response = to_string_results(result)
                    st.dataframe(result["sql_query_result"])  # Display the DataFrame in a more readable format
                    table_markdown = result["sql_query_result"].to_markdown()
                    st.session_state.messages.append({"role": "assistant", "content": table_markdown})
                # st.markdown(assistant_response)
            except Exception as e:
                st.error(f"Error: {str(e)}")