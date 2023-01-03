import pandas as pd
import streamlit as st
import random
from streamlit_card import card
import streamlit as st
import matplotlib.pyplot as plt




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

fig, ax = plt.subplots()
available_statuses = ['New', 'Completed', 'inProgress']
counts = [len(df.loc[df.Status == s])/len(df) for s in available_statuses]
ax.pie(counts, labels=available_statuses)
st.pyplot(fig)

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
    col1, col2 = st.columns([3, 1])
    card_title = questions[i]
    card_url = links[i]
    card_status = statuses[i]

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
