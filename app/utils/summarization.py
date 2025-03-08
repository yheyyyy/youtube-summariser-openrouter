from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from .openrouter_client import ChatOpenRouter


def initialize_embeddings():
    """Initialize HuggingFace embeddings."""
    model_name = "dunzhang/stella_en_400M_v5"
    model_kwargs = {
        'trust_remote_code': True,
        'device': 'cpu',
        'config_kwargs': {
            'use_memory_efficient_attention': False,
            'unpad_inputs': False
        }
    }
    encode_kwargs = {
        'normalize_embeddings': False
    }
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


def split_text_into_chunks(text, embeddings):
    """Split the text into semantic chunks."""
    chunker = SemanticChunker(embeddings=embeddings)
    chunks = chunker.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]


def initialize_llm():
    """Initialize the language model (LLM)."""
    return ChatOpenRouter(model_name="google/gemini-2.0-flash-exp:free")


def create_prompts():
    """Create the question and refine prompts for summarization."""
    question_template = PromptTemplate.from_template("""
    Write a concise summary of the following youtube transcript with key takeaways for the audience:
    "{text}"
    CONCISE SUMMARY:""")

    refine_template = PromptTemplate.from_template("""Your job is to produce a final key takeaways summary.
    We have provided an existing summary up to a certain point: {existing_answer}

    We have the opportunity to refine the existing summary (only if needed) with some more context below.
    ------------
    {text}
    ------------
    Given the new context, refine the original summary with new key takeaways.
    If the context isn't useful, return the original summary.\
    """)

    return question_template, refine_template


def setup_summarization_chain(llm, question_prompt, refine_prompt):
    """Set up the summarization chain."""
    return load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        verbose=True,
        document_variable_name="text", 
        initial_response_name="existing_answer"
    )


def generate_summary(chain, documents):
    """Generate the summary using the summarization chain."""
    output_comb = chain.invoke(documents)
    return output_comb['output_text']


def summarize_transcript(text):
    """Main function to summarize the transcript."""
    print(f"Transcript: {text}")

    embeddings = initialize_embeddings()
    documents = split_text_into_chunks(text, embeddings)
    llm = initialize_llm()
    question_prompt, refine_prompt = create_prompts()
    chain = setup_summarization_chain(llm, question_prompt, refine_prompt)
    summary = generate_summary(chain, documents)

    return summary