def create_chunks(markdown_text):
    chunks = []
    current_chunk = ""
    lines = markdown_text.split("\n")

    for line in lines:
        if line.startswith("# ") or line.startswith("## "):
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

# Example usage
markdown_text = """
# Introduction

Welcome to this example text file. This file contains markdown content to demonstrate the chunk creation process.

## What is Markdown?

Markdown is a lightweight markup language that allows you to format text using simple syntax. It is commonly used for documentation, web content, and more.

## Why Use Markdown?

Markdown offers several benefits:

- It is easy to learn and use.
- It produces clean and readable content.
- It can be converted to various formats like HTML, PDF, etc.

# Getting Started

To get started with Markdown, you need a text editor that supports Markdown syntax highlighting. Some popular options include:

- Visual Studio Code
- Sublime Text
- Atom

## Basic Syntax

Here are some basic Markdown syntax examples:

- Headings: Use `#` for top-level headings and `##` for subheadings.
- Bold: Wrap the text with double asterisks, like `**bold**`.
- Italic: Wrap the text with single asterisks, like `*italic*`.
- Lists: Use `-` or `*` for unordered lists and numbers for ordered lists.

# Conclusion

Markdown is a powerful and versatile markup language that simplifies the process of formatting text. By mastering the basic syntax, you can create well-structured and visually appealing documents.

## Additional Resources

For more information on Markdown, check out the following resources:

- [Markdown Guide](https://www.markdownguide.org/)
- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Happy Markdown writing!
"""

chunks = create_chunks(markdown_text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print()
