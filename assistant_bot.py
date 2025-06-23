import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.3)

PROMPT_TEMPLATES = {
    "Differentiate Activities": "You are an expert instructional coach. Suggest differentiated activities to help students achieve grade level proficiency based on this data: {student_data}",
    "Pre-Assessment from Data": "You are an expert instructional coach. Using this student data summary: {student_data}, create a pre-assessment with questions to gauge student readiness.",
    "Open-Ended Question Correction": "You are an expert instructional coach. Suggest improvements for this student response to an open-ended question: {student_response}"
}

st.title("Teacher Assistant Chatbot")

task = st.selectbox("Choose a task", list(PROMPT_TEMPLATES.keys()))

if task == "Differentiate Activities":
    student_data = st.text_area("Paste or type student data summary here:")
    if st.button("Get Suggestions"):
        if student_data.strip():
            prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES[task])
            messages = prompt.format_messages(student_data=student_data)
            result = llm.invoke(messages)
            st.success("Suggestions:")
            st.write(result.content)
        else:
            st.error("Please enter student data summary.")

elif task == "Pre-Assessment from Data":
    csv_text = st.text_area("📋 Paste your CSV student data here:")
    if st.button("Create Pre-Assessment"):
        if csv_text.strip():
            try:
                df = pd.read_csv(io.StringIO(csv_text))
                st.write("Preview of your data:")
                st.dataframe(df.head())

                summary = df.describe(include='all').to_string()

                prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES[task])
                messages = prompt.format_messages(student_data=summary)
                result = llm.invoke(messages)
                st.success("Pre-Assessment:")
                st.write(result.content)
            except Exception as e:
                st.error(f"Error processing CSV data: {e}")
        else:
            st.error("Please paste CSV data.")

elif task == "Open-Ended Question Correction":
    student_response = st.text_area("Paste student's open-ended question response here:")
    if st.button("Suggest Corrections"):
        if student_response.strip():
            prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES[task])
            messages = prompt.format_messages(student_response=student_response)
            result = llm.invoke(messages)
            st.success("Correction Suggestions:")
            st.write(result.content)
        else:
            st.error("Please enter the student response.")
