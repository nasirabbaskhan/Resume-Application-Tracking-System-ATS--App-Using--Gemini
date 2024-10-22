from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import PyPDF2 as pdf
import os

load_dotenv()



GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# gemini pro response
def get_gemini_response(resume_text,job_description):
    
    # llm
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",temperature=0,)
    
    
    # prompt
    prompt_template = """
    Hey asct like a skilled or very experience ATS(Application Tracking System)
    with a deep understanding of tech fields, Software Engineering, Data Science,
    Fullstack web dwvelopment, Big Data Engineering, DEVOPS, Data Analyest,ML and DL Engineering,
    Generative AI engineering and having deep ATS functionality,
    Your Task is to avaluate the resume  based on the given job description. 
    You must consider the job market is very competitive and you should provide best assistance
    for improving the resumes. Assign the percentage Matching based on the jd and
    the missing keywordswith high accuracy 
    resume:{text}
    description:{job_description} 

    I want the reason that having structure
    {{"JD Match":"%",
    "MissingKeywieds:[]", 
    "Profile Summary":""}}

    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text", "job_description"] )
    
    
    # chaining 
    chain = prompt | llm
    
    # invoke the response
    response = chain.invoke({"text":resume_text, "job_description":job_description })
    return response.content



# extract the text from uploaded_file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text=""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text+=page.extract_text()
    return text

    
    
# streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
st.text("Improve Your Resume Through ATS")

job_description = st.text_area("Past the Job Description :")

uploaded_file = st.file_uploader("Upload Your Resume" ,type="pdf", help="please upload the pdf")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(resume_text,job_description)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("please upload a resume")  
    
    

