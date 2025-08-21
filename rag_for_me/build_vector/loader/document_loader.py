import re
from langchain.schema import Document   

def split_markdown_by_heading(file_path="rag_for_me/knowledge_base/personal_information.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    sections = re.split(r'(?m)^# ', md_text)
    docs = []

    for section in sections:
        if not section.strip():
            continue
        # Add '#' to keep old format
        content = "# " + section.strip()
        docs.append(Document(
            page_content=content,
            metadata={"category": content.split("\n")[0].replace("# ", "").strip()}
        ))
    return docs


# chunks = split_markdown_by_heading()
# for index, doc in enumerate(chunks, 1):
#     print(f"--- Chunk {index} ---")
#     print("Category:", doc.metadata["category"])
#     print("Content:")
#     print(doc.page_content)
#     print()
