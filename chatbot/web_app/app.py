import streamlit as st
import requests

# Define the function to perform prediction
def predict_answer(query):
    # Make a request to the API endpoint
    url = "http://localhost:8901/api/search"  # Assuming the API endpoint is running locally
    params = {"query": query}
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data["answer"], data["context"]
    else:
        return None, None

# Streamlit UI
def main():
    st.title("Edstem Chatbot")

    # Input query
    query = st.text_area("Enter your query here:")

    if st.button("Submit"):
        # Perform prediction
        if query:
            answer, context = predict_answer(query)
            if answer is not None:
                # Display predicted answer and context
                st.write("Predicted Answer:", answer)
                st.write("Context:", context)
            else:
                st.error("Failed to retrieve prediction.")
        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()

