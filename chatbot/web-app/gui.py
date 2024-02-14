import streamlit as st
import requests

# Password for app access
correct_password = "secure_password"

# Streamlit app title and header
st.title("EdStem Chatbot")

# Placeholder for password input
password_placeholder = st.empty()

# Get the password input from the user
password = password_placeholder.text_input("Enter password:", "", type="password")

# Check if the entered password is correct
if password == correct_password:
    password_placeholder.empty()  # Remove the password input field

    st.success("Login successful!")

    # Streamlit app content
    st.header("Enter your question below:")

    # Input box for user query
    query = st.text_input("Query:")

    # Button to send the query
    if st.button("Send"):
        if query:
            api_url = f"http://localhost:8000/similarity_search?query={query}"
            try:
                # Make the API request
                response = requests.get(api_url)

                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()  # Assuming the API response is in JSON format
                    st.success("User Query:")
                    st.write(query)  # Display the user's query
                    st.success("API Response:")
                    st.json(result)  # Display the API response as JSON
                else:
                    st.error(f"API Request Failed (Status Code: {response.status_code})")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a query.")
else:
    st.error("Incorrect password. Access denied.")

