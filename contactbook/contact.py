import streamlit as st
import pandas as pd

# Initialize contacts in session state
if 'contacts' not in st.session_state:
    st.session_state['contacts'] = []


# Function to add a contact
def add_contact(name, phone, email, address):
    contact = {'Name': name, 'Phone': phone, 'Email': email, 'Address': address}
    st.session_state['contacts'].append(contact)


# Function to update a contact
def update_contact(index, name, phone, email, address):
    st.session_state['contacts'][index] = {'Name': name, 'Phone': phone, 'Email': email, 'Address': address}


# Function to delete a contact
def delete_contact(index):
    st.session_state['contacts'].pop(index)


# Function to search for a contact
def search_contacts(query):
    results = [contact for contact in st.session_state['contacts'] if
               query.lower() in contact['Name'].lower() or query in contact['Phone']]
    return results


# Streamlit app layout
st.title("Contact Book Application")

# Add a new contact
st.header("Add a New Contact")
name = st.text_input("Name")
phone = st.text_input("Phone")
email = st.text_input("Email")
address = st.text_area("Address")

if st.button("Add Contact"):
    if name and phone:
        add_contact(name, phone, email, address)
        st.success(f"Contact for {name} added.")
    else:
        st.error("Name and Phone are required fields!")

# View all contacts
st.header("Contact List")
if st.session_state['contacts']:
    df = pd.DataFrame(st.session_state['contacts'])
    st.dataframe(df)

# Search for a contact
st.header("Search for a Contact")
search_query = st.text_input("Enter name or phone number to search")
if st.button("Search"):
    results = search_contacts(search_query)
    if results:
        st.write("Search Results:")
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)
    else:
        st.write("No contacts found.")

# Update or delete a contact
if st.session_state['contacts']:
    st.header("Update or Delete a Contact")
    contact_index = st.number_input("Enter the index of the contact to update or delete", min_value=0,
                                    max_value=len(st.session_state['contacts']) - 1, step=1)

    if contact_index < len(st.session_state['contacts']):
        selected_contact = st.session_state['contacts'][contact_index]
        st.write(f"Selected Contact: {selected_contact['Name']}")

        new_name = st.text_input("New Name", value=selected_contact['Name'])
        new_phone = st.text_input("New Phone", value=selected_contact['Phone'])
        new_email = st.text_input("New Email", value=selected_contact['Email'])
        new_address = st.text_area("New Address", value=selected_contact['Address'])

        if st.button("Update Contact"):
            update_contact(contact_index, new_name, new_phone, new_email, new_address)
            st.success(f"Contact at index {contact_index} updated.")

        if st.button("Delete Contact"):
            delete_contact(contact_index)
            st.success(f"Contact at index {contact_index} deleted.")

    if st.button("Download Contacts as CSV"):
        df.to_csv("contacts.csv", index=False)
        st.success("Contacts saved to contacts.csv")

else:
    st.write("No contacts to update or delete.")
