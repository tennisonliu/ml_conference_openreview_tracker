import os
import openreview
import pickle
import json

conference = 'NeurIPS_2023'
venueid = 'NeurIPS.cc/2023/Conference'


# download or load submissions
if os.path.exists(f'{conference}_submissions.pkl'):
    with open(f'{conference}_submissions.pkl', 'rb') as f:
        submissions = pickle.load(f)
else:
    client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')
    submissions = client.get_all_notes(content={'venueid':venueid} )

    with open(f'{conference}_submissions.pkl', 'wb') as f:
        pickle.dump(submissions, f)

# print paper status list
print(set([s.content['venue']['value'] for s in submissions]))

# create author_to_paper dictionary
author_to_paper = {}
for s in submissions:
    paper_title = s.content['title']['value']
    paper_status = s.content['venue']['value']
    author_list = s.content['authors']['value']
    assert isinstance(author_list, list)

    for author in author_list:
        if author in author_to_paper:
            author_to_paper[author].append(paper_title)
        else:
            author_to_paper[author] = [paper_title]

# save as JSON
with open(f'{conference}_author_to_paper.json', 'w') as f:
    json.dump(author_to_paper, f)

# sort authors by number of papers
author_to_paper_num = {k: len(v) for k, v in sorted(author_to_paper.items(), key=lambda item: len(item[1]), reverse=True)}

# save as JSON
import json
with open(f'{conference}_author_to_paper_num.json', 'w') as f:
    json.dump(author_to_paper_num, f)

# print first 20 authors
for k, v in list(author_to_paper_num.items())[:20]:
    print(k, v)