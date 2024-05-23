def calculate_word_similarity(str1, str2):
    # Convert the strings to lowercase and split them into lists of words
    words1 = str1.lower().split()
    words2 = str2.lower().split()

    # Create sets of unique words from each list
    set1 = set(words1)
    set2 = set(words2)

    # Calculate the number of common words
    common_words = len(set1 & set2)

    # Calculate the total number of unique words across both strings
    total_words = len(set1 | set2)

    # Calculate the percentage of common words
    if total_words > 0:
        similarity_percentage = (common_words / total_words) * 100
    else:
        similarity_percentage = 0.0

    return similarity_percentage


import os
import re
import matplotlib.pyplot as plt
def create_chunks(folder_path):
    chunks = []
    chunk_sizes = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                content = content.replace('######','')

                sections = re.split(r'(?m)^#\s', content)

                for section in sections[1:]:  # Skip the first empty section
                    lines = section.strip().split('\n')
                    title = lines[0].strip()
                    text = '\n'.join(lines[1:])

                    subsections = re.split(r'(?m)^##\s', text)
                    parent_text = subsections[0].strip()

                    for subsection in subsections[1:]:
                        sublines = subsection.strip().split('\n')
                        subtitle = sublines[0].strip()
                        subtext = '\n'.join(sublines[1:])

                        chunk = {
                            'filename': filename[0:-4],
                            'page_num': 1,
                            'content': f"# {title}\n{parent_text}\n\n## {subtitle}\n{subtext}"
                        }
                        chunks.append(chunk)
                        chunk_sizes.append(len(chunk['content']))

    
                
    # Create a histogram of chunk sizes
    plt.figure(figsize=(10, 6))
    plt.hist(chunk_sizes, bins=100, edgecolor='black')
    plt.xlabel('Chunk Size (Number of Characters)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Chunk Sizes')
    plt.tight_layout()
    plt.show()

    return chunks

# Example usage
folder_path = './txt'
chunks = create_chunks(folder_path)
for chunk in chunks:
    print(chunk)


sim=0
for chunk in chunks:
    fname=chunk['filename']
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                pages=re.split(r'(?m)^######', content)
                page_num=0
                for i,page in enumerate(pages):
                    page_num=page_num+1
                    if chunk['filename'] == filename[0:-4]:
                        temp_sim=calculate_word_similarity(chunk['content'],page)
                        if temp_sim>sim:
                            sim=temp_sim
                            chunk['page_num']=page_num
        sim=0
