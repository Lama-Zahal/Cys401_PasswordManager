# ui.py - Streamlit interface for the password manager
# Run with: streamlit run ui.py

import streamlit as st
from vault import Vault
from generator import generate_password, check_strength, find_reused

st.set_page_config(page_title="Password Manager")

# Streamlit reruns the whole file

if "vault" not in st.session_state:
    st.session_state.vault = Vault()
    st.session_state.unlocked = False
    st.session_state.revealed = []
    st.session_state.editing = None
    st.session_state.deleting = None
    st.session_state.generated = ""

vault = st.session_state.vault


def show_strength(password): #when password is input call check strength to provide a score from 0-5
    if password:
        label, tips = check_strength(password)
        st.write("Strength:", label)
        for tip in tips:
            st.caption(tip)# provides tips


# create vault (for the first time only)
def create_page():
    st.title("Create your vault")
    st.write("Choose a master password. If you forget it, the vault cannot be recovered.")
    pw = st.text_input("Master password", type="password")
    show_strength(pw)
    pw2 = st.text_input("Confirm master password", type="password")

    if st.button("Create vault"):#ensure its not less that 8 characters
    
        if len(pw) < 8:
            st.error("Master password must be at least 8 characters.")
        elif pw != pw2:#ensure both entries are the same
            st.error("Passwords do not match.")
        else:
            vault.create(pw)#if requirments are met creates encrypted vault and opens it
            st.session_state.unlocked = True
            st.rerun()


# the loging page with one password box and a button for unlock
def login_page():
    st.title("Unlock your vault")
    pw = st.text_input("Master password", type="password")

    if st.button("Unlock"):
        if vault.unlock(pw):#if its true unlocks the vault
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Wrong master password.")


# the list of saved passwords
def vault_page():
    if len(vault.entries) == 0: #alerts if empty
        st.info("Your vault is empty. Add an entry in the Add entry tab.")
        return

    reused = find_reused(vault.entries)

    for i, entry in enumerate(vault.entries):#for each entry create one row with 6 columns
        col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 4, 2, 2, 2])
        col1.write(entry["site"])
        col2.write(entry["username"])

        if i in st.session_state.revealed:
            col3.code(entry["password"])
        else:
            col3.code("**********")

        if entry["password"] in reused:
            col3.caption("Reused password")

        if col4.button("Show", key=f"show{i}"):
            if i in st.session_state.revealed:
                st.session_state.revealed.remove(i)
            else:
                st.session_state.revealed.append(i)
            st.rerun()

        if col5.button("Edit", key=f"edit{i}"):
            st.session_state.editing = i
            st.rerun()

        if col6.button("Delete", key=f"delete{i}"):
            st.session_state.deleting = i
            st.rerun()

        if st.session_state.deleting == i:
            st.warning(f"Delete {entry['site']}? This cannot be undone.")
            if st.button("Yes, delete", key=f"yes{i}"):
                vault.delete_entry(i)
                st.session_state.deleting = None
                st.session_state.revealed = []
                st.rerun()
            if st.button("Cancel", key=f"no{i}"):
                st.session_state.deleting = None
                st.rerun()

        if st.session_state.editing == i:
            edit_form(i, entry)


def edit_form(i, entry):
    site = st.text_input("Site", value=entry["site"], key="edit_site")
    user = st.text_input("Username", value=entry["username"], key="edit_user")
    pw = st.text_input("Password", value=entry["password"], type="password", key="edit_pw")
    show_strength(pw)

    if st.button("Save changes"):
        if site == "" or pw == "":
            st.error("Site and password cannot be empty.")
        else:
            vault.update_entry(i, site, user, pw)#to save changes 
            st.session_state.editing = None
            st.rerun()
    if st.button("Cancel edit"):
        st.session_state.editing = None
        st.rerun()


# add a new entry
def add_page():#boxes for site,username and password,with the strength label
    site = st.text_input("Site")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    show_strength(pw)

    if st.button("Add to vault"):
        if site == "" or pw == "":
            st.error("Site and password are required.")
        else:
            vault.add_entry(site, user, pw)
            st.success(f"Saved {site}.")

    st.subheader("Password generator")
    length = st.slider("Length", 8, 64, 16)#adding a slider for lenght 8-64
    symbols = st.checkbox("Include symbols", value=True)
    if st.button("Generate"):
        st.session_state.generated = generate_password(length, symbols)#the result
    if st.session_state.generated:
        st.write("Copy this password into the Password box above:")
        st.code(st.session_state.generated)


# reused and weak passwords
def security_page():
    if len(vault.entries) == 0:
        st.info("Nothing to check yet.")
        return

    reused = find_reused(vault.entries)#show sites that have the same password
    if len(reused) == 0:
        st.success("No reused passwords.")
    else:
        st.error("Some passwords are used on more than one site.")
        for pw in reused:
            sites = [e["site"] for e in vault.entries if e["password"] == pw]
            st.write("Same password on:", ", ".join(sites))

    for e in vault.entries:
        label, tips = check_strength(e["password"])#show sites with weak passwords
        if label == "Weak":
            st.warning(f"Weak password on {e['site']}")


# decide which page to show in the interface 
if not st.session_state.unlocked:
    if vault.exists():#locked and the vault exist 
        login_page()
    else:
        create_page()#locked but no vault
else:
    if st.sidebar.button("Lock vault"):
        del st.session_state.vault
        st.rerun()

    st.title("My vault")#unlocked 
    tab1, tab2, tab3 = st.tabs(["Vault", "Add entry", "Security check"])
    with tab1:
        vault_page()
    with tab2:
        add_page()
    with tab3:
        security_page()