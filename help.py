import streamlit as st
import json
import os

DATA_FILE = "grocery_list.json"


# Load data from local file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# Save data to local file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


st.title("Collaborative Grocery List")

# Initialize session state for input
if 'list_data' not in st.session_state:
    st.session_state.list_data = load_data()

# Input Form
with st.form("add_item", clear_on_submit=True):
    col1, col2 = st.columns(2)
    name = col1.text_input("Your Name")
    item = col2.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=1, value=1)
    # Simple placeholder for image (filepath)
    img_url = st.text_input("Image URL (optional)")

    submit = st.form_submit_button("Add to List")

    if submit and name and item:
        new_entry = {"name": name, "item": item, "qty": qty, "img": img_url}
        st.session_state.list_data.append(new_entry)
        save_data(st.session_state.list_data)
        st.rerun()

# Display List
st.subheader("Current Items")
for i, entry in enumerate(st.session_state.list_data):
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        st.write(f"**{entry['item']}** (Qty: {entry['qty']}) - Added by: {entry['name']}")
        if entry['img']:
            st.image(entry['img'], width=100)

    with col2:
        # Checkmark to remove
        if st.checkbox("Got it", key=f"check_{i}"):
            del st.session_state.list_data[i]
            save_data(st.session_state.list_data)
            st.rerun()