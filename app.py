import streamlit as st
import numpy as np
import sqlite3
from scipy.optimize import linear_sum_assignment

st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.min.css" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
st.markdown("""""", unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
                header{visibility:hidden;}
                .main {
                    margin-top: -20px;
                    padding-top:10px;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: orange;">
    <a class="navbar-brand" href="#"  target="_blank">UMaT Security</a>  
    </nav>
""",
    unsafe_allow_html=True,
)

# Initialize SQLite database
conn = sqlite3.connect("base.db")
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY,
        names TEXT,
        dates TEXT,
        times TEXT,
        places TEXT
    )
''')

def hungarian_algorithm_cost_matrix(names, dates, times, places):
    # Create a cost matrix where each element represents the cost of assigning a person to a particular date, time, and place
    num_people = len(names)
    num_dates = len(dates)
    num_times = len(times)
    num_places = len(places)
    
    cost_matrix = np.zeros((num_people, num_dates, num_times, num_places))
    for i, _ in enumerate(names):
        for j, _ in enumerate(dates):
            for k, _ in enumerate(times):
                for l, _ in enumerate(places):
                    # You can implement your own logic to calculate the cost based on preferences, distances, or other factors.
                    # For this example, we will randomly generate costs.
                    cost_matrix[i, j, k, l] = np.random.randint(1, 10) # Random cost between 1 and 10
    
    return cost_matrix

def run_hungarian_algorithm(cost_matrix):
    # Use the Hungarian algorithm to solve the assignment problem
    row_ind, col_ind = linear_sum_assignment(cost_matrix.min(axis=(2, 3)))
    return row_ind, col_ind

def main():
    st.title("Job Allocation System")
    st.write("Enter the details of people and options for dates, times, and places.")
    
    names_input = st.text_area("Names (separated by commas)", "John, Alice, Bob, Sarah")
    dates_input = st.text_area("Dates (separated by commas)", "2023-07-20, 2023-07-21, 2023-07-22")
    times_input = st.text_area("Times (separated by commas)", "10:00 AM, 2:00 PM, 6:00 PM")
    places_input = st.text_area("Places (separated by commas)", "Restaurant A, Restaurant B, Park C")

    if st.button("Match"):
        names = [name.strip() for name in names_input.split(",")]
        dates = [date.strip() for date in dates_input.split(",")]
        times = [time.strip() for time in times_input.split(",")]
        places = [place.strip() for place in places_input.split(",")]
        
        st.sidebar.success("Data saved successfully!")
        cost_matrix = hungarian_algorithm_cost_matrix(names, dates, times, places)
        row_ind, col_ind = run_hungarian_algorithm(cost_matrix)
        cursor.execute('INSERT INTO assignments (names, dates, times, places) VALUES (?, ?, ?, ?)', (names_input, dates_input, times_input, places_input))
        conn.commit()
        st.subheader("Matching Results:")
        for i, person_index in enumerate(row_ind):
            person_name = names[person_index]
            date = dates[col_ind[i]]
            time = times[col_ind[i]]
            place = places[col_ind[i]]
            st.write(f"{person_name} -> Date: {date}, Time: {time}, Place: {place}")
def update_assignment(assignment_id, names_input, dates_input, times_input, places_input):
    # Update the assignment in the database
    cursor.execute('''
        UPDATE assignments
        SET names=?, dates=?, times=?, places=?
        WHERE id=?
    ''', (names_input, dates_input, times_input, places_input, assignment_id))
    conn.commit()
def view_and_edit():
    # Retrieve the assignments from the database
    cursor.execute('SELECT * FROM assignments')
    assignments = cursor.fetchall()

    # Show the assignments in the sidebar
    st.sidebar.header("View and Edit Assignments")
    selected_assignment = st.sidebar.selectbox("Select an Assignment", assignments)

    if selected_assignment:
        # Display the selected assignment details in the main area
        st.subheader("Selected Assignment Details:")
        st.write(f"Names: {selected_assignment[1]}")
        st.write(f"Dates: {selected_assignment[2]}")
        st.write(f"Times: {selected_assignment[3]}")
        st.write(f"Places: {selected_assignment[4]}")

    st.sidebar.header("Edit Assignment")
    selected_assignment = st.sidebar.selectbox("Select an Assignment to Edit", assignments)

    if selected_assignment:
        assignment_id, names, dates, times, places = selected_assignment
        st.subheader("Selected Assignment Details:")
        st.write(f"Names: {names}")
        st.write(f"Dates: {dates}")
        st.write(f"Times: {times}")
        st.write(f"Places: {places}")

        with st.expander("Edit Assignment Details", expanded=True):
            names_input = st.text_area("Names (separated by commas)", names)
            dates_input = st.text_area("Dates (separated by commas)", dates)
            times_input = st.text_area("Times (separated by commas)", times)
            places_input = st.text_area("Places (separated by commas)", places)

            update_button = st.button("Update Assignment")
            if update_button:
                update_assignment(assignment_id, names_input, dates_input, times_input, places_input)
                st.sidebar.success("Assignment updated successfully!")
                st.experimental_rerun()

# if __name__ == "__main__":
#     with st.container():
        
#         key = st.text_input("Secret Key", type="password")
#         submit = st.button("Login")

st.markdown(f"<span class='btn btn-primary btn-block ' style='border-radius:50px'>Select</span>",unsafe_allow_html=True)
check = st.checkbox("View / Edit")
if check:
    view_and_edit()
else:    
    main()
# if submit:
#     if key == "2468":
#         main()
  
#         key = None
#         submit = None
#     else:
#         st.markdown(
#             f"<span class='btn btn-danger' style='border-radius:50px'>Wrong</span>",
#             unsafe_allow_html=True,
#         )
