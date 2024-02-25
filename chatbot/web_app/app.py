import streamlit as st
from rag import RAG  # Import your RAG implementation

# Define the function to perform prediction
def predict_answer(query):
    rag = RAG()
    pred = rag(query)
    return pred.answer, pred.context

# Streamlit UI
def main():
    st.title("Edstem Chatbot")

    # Input query
    query = st.text_area("Enter your query here:")

    if st.button("Submit"):
        # Perform prediction
        if query:
            answer, context = predict_answer(query)
            # Display predicted answer and context
            st.write("Predicted Answer:", answer)
            st.write("Context:", context)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
