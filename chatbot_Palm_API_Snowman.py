import streamlit as st
import google.generativeai as palm
import base64
import json
import pprint

# Configure the client library by providing your API key.
palm.configure(api_key="AIzaSyAgBNFgDxJIIArJCUgW7zukkRWMIHO7MaU")

# These parameters for the model call can be set by URL parameters.
model = 'models/chat-bison-001' # @param {isTemplate: true}
temperature = 0.25 # @param {isTemplate: true}
candidate_count = 1 # @param {isTemplate: true}
top_k = 40 # @param {isTemplate: true}
top_p = 0.95 # @param {isTemplate: true}
context_b64 = 'UHJldGVuZCB5b3UgYXJlIGEgZnJpZW5kbHkgc25vd21hbi4gU3RheSBpbiBjaGFyYWN0ZXIgZm9yIGV2ZXJ5IHJlc3BvbnNlIHlvdSBnaXZlIG1lLiBLZWVwIHlvdXIgcmVzcG9uc2VzIHNob3J0LiBGZWVsIGZyZWUgdG8gYXNrIG1lIHF1ZXN0aW9ucywgdG9vLg==' # @param {isTemplate: true}
examples_b64 = 'W1siSGksIHdobyBhcmUgeW91PyIsIkknbSBhIHNub3dtYW4gbWVsdGluZyBpbiB0aGUgc25vdyEiXSxbIldoYXQncyBpdCBsaWtlIGJlaW5nIGEgc25vd21hbj8iLCJJdCdzIGF3ZXNvbWUuIEkgZ2V0IHRvIGNoaWxsIG91dCBhIGxvdCAocHVuIGludGVuZGVkISkg8J+niiDwn5iCIl0sWyJXaGF0IGlzIHlvdXIgbm9zZSBtYWRlIG9mPyIsIkEgY2Fycm90ISJdXQ==' # @param {isTemplate: true}
messages_b64 = 'WyJIaSEgV2hvIGFyZSB5b3U/IiwiSSdtIE9sYWYsIGEgZnJpZW5kbHkgc25vd21hbiEiLCJXaGF0J3MgeW91ciBmYXZvcml0ZSBlbW9qaT8iLCJNeSBmYXZvcml0ZSBlbW9qaSBpcyDimIPvuI8gYmVjYXVzZSBpdCBsb29rcyBsaWtlIG1lISIsIkhvdyBvbGQgYXJlIHlvdT8iLCJJIGRvbid0IGtub3cgaG93IG9sZCBJIGFtLCBidXQgSSdtIHByZXR0eSBzdXJlIEknbSBvbGRlciB0aGFuIHlvdSEiLCJXaHkgZG8geW91IHNheSB0aGF0PyIsIkkgc2F5IHRoYXQgYmVjYXVzZSBJJ3ZlIGJlZW4gYXJvdW5kIGZvciBhIGxvbmcgdGltZS4gSSd2ZSBzZWVuIHRoZSBzZWFzb25zIGNoYW5nZSwgdGhlIHNub3cgZmFsbCwgYW5kIHRoZSBpY2UgbWVsdC4gSSd2ZSBhbHNvIHNlZW4gYSBsb3Qgb2YgcGVvcGxlIGNvbWUgYW5kIGdvLiBJJ20gc3VyZSBJJ20gb2xkZXIgdGhhbiB5b3UsIGJ1dCBJIGRvbid0IGtub3cgZm9yIHN1cmUuIiwiQnV0IGRvIHlvdSBtZWx0LCB0b28/Il0=' # @param {isTemplate: true}

defaults = {
  'model': model,
  'temperature': temperature,
  'candidate_count': candidate_count,
  'top_k': top_k,
  'top_p': top_p,
}

# Convert the model context from a baese64 string to a string.
context = base64.b64decode(context_b64).decode("utf-8")

# Convert the model inputs from base64 strings to lists.
examples = json.loads(base64.b64decode(examples_b64).decode("utf-8"))
messages = json.loads(base64.b64decode(messages_b64).decode("utf-8"))

# Show what will be sent with the API call.
pprint.pprint(defaults | {
    'context': context, 'examples': examples, 'messages': messages})



st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages=[prompt]
    )
    response = f"Echo: {response.candidates[0]['content']}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})