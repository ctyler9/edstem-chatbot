import json 


def structured(in_path, out_path):
    with open(in_path, "r") as fp_in:
        data = json.load(fp_in)

    """
    new_json_template = {"threadPosts": [{"id": 1, "title": "First blog post", "content": "This is my first blog post"},], "comments": [{"id": 1, "content": "Nice post!", "threadPostId": 1},]}
    """
    new_json = {"threadPosts": [], "comments": []}

    comment_id = 0
    for enum, entry in enumerate(data):
        subject = entry["subject"]
        content = entry["content"]
        children = entry["children"]["threads"]

        thread_post = {"id": enum, "title": subject, "content": content}
        new_json["threadPosts"].append(thread_post)

        for child in children:
            if type(child) == dict:
                content = child["content"]
            elif type(child) == str:
                content = child
            comment = {"id": comment_id, "content": content, "threadPostId": enum}
            comment_id += 1
            new_json["comments"].append(comment)
    
    with open(out_path, "w") as fp_out:
        json.dump(new_json, fp_out)

def unstructured(in_path, out_path):
    with open(in_path, "r") as fp_in:
        data = json.load(fp_in)

    """
    new_json_template = {[{"threadPost": Post title, "comments": ["comment1", "comment2"]}
    """

    master_entries = []
    for enum, entry in enumerate(data):
        subject = entry["subject"]
        content = entry["content"]
        children = entry["children"]["threads"]

        thread_post = subject + content

        comments = []
        for child in children:
            if type(child) == dict:
                content = child["content"]
            elif type(child) == str:
                content = child
            comments.append(content)
        
        entry = {"threadPost": thread_post, "comments": comments}
        master_entries.append(entry)

    
    with open(out_path, "w") as fp_out:
        json.dump(master_entries, fp_out)
 
if __name__ == "__main__":
    in_path = []
    out_path = []
    for i in range(len(in_path)):
        unstructured(in_path[i], out_path[i])
