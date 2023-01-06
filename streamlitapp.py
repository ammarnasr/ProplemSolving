import pandas as pd
import streamlit as st
import random
from streamlit_card import card
import streamlit as st
import matplotlib.pyplot as plt
import os



filename = 'LeetCode75Proplems.csv'
df = pd.read_csv(filename)
# st.table(df)

def update_status(question, new_staus):
    index = df.loc[df['Question'] == question].index[0]
    df.at[index, 'Status'] = new_staus
    df.to_csv('LeetCode75Proplems.csv', index=False)

bgs = {
    'New': 'https://github.com/ammarnasr/ProplemSolving/blob/main/new.png?raw=true',
    'Completed': 'https://github.com/ammarnasr/ProplemSolving/blob/main/completed.png?raw=true',
    'inProgress': 'https://github.com/ammarnasr/ProplemSolving/blob/main/inProgress.png?raw=true',
}

new_only_df = df.loc[df['Status']== 'New']
rand_row = df.sample()
random_card_title = rand_row['Question'].iloc[0]
random_card_url = rand_row['Link'].iloc[0]
random_card_status = 'Random Proplem (Refresh to change)'
_ = card(title=random_card_title,text=random_card_status, image=bgs['New'],url=random_card_url)
show_topic = st.checkbox(f'Show Topic?')
if show_topic:
    st.info(rand_row['Topic'].iloc[0] )

fig, ax = plt.subplots()
available_statuses = ['New', 'Completed', 'inProgress']
counts = [len(df.loc[df.Status == s])/len(df) for s in available_statuses]
ax.pie(counts, labels=available_statuses,  autopct='%1.1f%%')
c1, c2 = st.columns([4, 2])
with c1:
    st.pyplot(fig)
with c2:
    d = {}
    for status in available_statuses:
        d[status] = counts[available_statuses.index(status)] * len(df)
    st.write(d)

topics = df.Topic.value_counts().index.tolist()
topics_options = df.Topic.value_counts().index.tolist()
topics_options.append('Random')
selected_topic = st.radio('Select an topic:', topics_options)

if selected_topic == 'Random':
    st.info('You selected the random option!')
    selected_topic = random.choice(topics)

st.success(f'You selected {selected_topic}')


questions = df.loc[df.Topic == selected_topic]['Question'].values.tolist()
links = df.loc[df.Topic == selected_topic]['Link'].values.tolist()
statuses = df.loc[df.Topic == selected_topic]['Status'].values.tolist()

for i in range(len(questions)):
    col1, col2,col3 = st.columns([6, 3, 1])
    card_title = questions[i]
    card_url = links[i]
    card_status = statuses[i]
    outputFilename = f'{selected_topic} {card_title}.py'

    with col1:
        _ = card(title=card_title,text=card_status, image=bgs[card_status],url=card_url)
    with col2:
        st.info('Update Status:')
        available_statuses = ['New', 'Completed', 'inProgress']
        available_statuses.remove(card_status)
        new_status = st.radio(f'Select New Status for {card_title}:', available_statuses)
        do_update = st.checkbox(f'Update Card : {card_title}')
        if do_update:
            update_status(card_title, new_status)
            st.success('Status Updated Successfully')
            st.warning('Reload Page to see Effects')
    # with col3 :
    #     if os.path.exists(outputFilename):
    #         with open(outputFilename, "r") as file:
    #             contents = file.read()
    #         st.code(contents, language="python")
    #     else:
    #         contents = st.text_input(f"Enter your Code for {card_title}:", value="def main:")
    #         with open(outputFilename, "w") as file:
    #             file.write(contents)
    #         st.code(contents, language="python")





subset_df = df.loc[df.Topic == selected_topic]
fig, ax = plt.subplots()
available_statuses = ['New', 'Completed', 'inProgress']
counts = [len(subset_df.loc[subset_df.Status == s])/len(subset_df) for s in available_statuses]
ax.pie(counts, labels=available_statuses)
st.pyplot(fig)

new_subset_df = subset_df.loc[subset_df.Status == 'New']
new_subset_questions = new_subset_df.Question.values.tolist()
new_random_question = random.choice(new_subset_questions)
st.info(f'Random Proplem in {selected_topic} is {new_random_question}!')
