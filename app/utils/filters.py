import re

def format_content(text):
    """
    Formats content for display in templates, handling tables and markdown formatting.
    """
    lines = text.split('\n')
    
    # Check for a tree structure pattern and isolate it
    tree_section = []
    non_tree_sections = []
    in_tree = False
    current_section = []
    
    # Look for ``` code blocks which often contain trees
    if "```" in text:
        sections = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        result = []
        for section in sections:
            if section.startswith('```') and section.endswith('```'):
                # This is a code block, might be a classification tree
                tree_content = section.replace('```', '').strip()
                result.append(f'<div class="classification-scroll"><pre class="classification-tree">{tree_content}</pre></div>')
            else:
                # Process this section normally
                result.append(format_normal_text(section))
        return ''.join(result)
    
    # Check for tree patterns without code blocks
    else:
        for i, line in enumerate(lines):
            # Detect start of tree pattern
            if (('|---' in line or '|____' in line or '├─' in line or '└─' in line) or 
                line.strip() == "Machine Learning" or 
                ('|' in line and '─' in line)) and not in_tree:
                # If we were collecting non-tree content, finalize it
                if current_section:
                    non_tree_sections.append('\n'.join(current_section))
                    current_section = []
                in_tree = True
                tree_section.append(line)
            # Detect end of tree pattern - empty line after tree content
            elif in_tree and (i == len(lines) - 1 or (not line.strip() and i < len(lines) - 1 and not any(tree_char in lines[i+1] for tree_char in ['|', '├', '└']))):
                tree_section.append(line)
                in_tree = False
                # Format and add the tree section
                non_tree_sections.append(f'<div class="classification-scroll"><pre class="classification-tree">{chr(10).join(tree_section)}</pre></div>')
                tree_section = []
            elif in_tree:
                tree_section.append(line)
            else:
                current_section.append(line)
        
        # Add any remaining content
        if current_section:
            non_tree_sections.append('\n'.join(current_section))
        if tree_section:  # If we ended while still in a tree section
            non_tree_sections.append(f'<div class="classification-scroll"><pre class="classification-tree">{chr(10).join(tree_section)}</pre></div>')
        
        # Process each non-tree section
        formatted_sections = [format_normal_text(section) for section in non_tree_sections]
        return ''.join(formatted_sections)

def format_normal_text(text):
    """
    Format regular (non-tree) text with markdown-style formatting
    """
    if not text or text.strip() == '':
        return ''
        
    # Handle tables
    if '|' in text:
        lines = text.split('\n')
        table_lines = []
        in_table = False
        formatted_text = []

        for line in lines:
            if line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    table_lines = ['<div class="table-responsive"><table class="comparison-table">']
                cells = line.strip().split('|')[1:-1]
                if '-|-' in line:
                    continue
                row = '<tr>' + ''.join(f'<td>{cell.strip()}</td>' for cell in cells) + '</tr>'
                table_lines.append(row)
            else:
                if in_table:
                    in_table = False
                    table_lines.append('</table></div>')
                    formatted_text.append('\n'.join(table_lines))
                formatted_text.append(line)

        if in_table:
            table_lines.append('</table></div>')
            formatted_text.append('\n'.join(table_lines))

        text = '\n'.join(formatted_text)

    # Format headers
    # Double asterisk section headers (like **1. Definition:**)
    text = re.sub(r'\*\*(\d+\.\s+[A-Za-z].*?):\*\*', r'<h3 class="section-header">\1:</h3>', text, flags=re.MULTILINE)
    
    # Handle markdown headers (## style)
    text = re.sub(r'^(#{1,3})\s+(.*?)$', r'<h3 class="section-header">\2</h3>', text, flags=re.MULTILINE)
    
    # Handle section headers (like "1. Chapter Overview:")
    text = re.sub(r'^(\d+\.\s+[A-Za-z].*?:)$', r'<h3 class="section-header">\1</h3>', text, flags=re.MULTILINE)
    
    # Format text styles
    # Handle basic formatting for bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Handle labeled bullet points (e.g., * Main Topic:) - make them display properly
    text = re.sub(r'^\s*\*\s+([A-Za-z\s]+):(\s*)(.*?)$', 
                 r'<div class="labeled-point"><span class="label-highlight">\1:</span>\3</div>', 
                 text, 
                 flags=re.MULTILINE)
    
    # Handle regular bullet points
    text = re.sub(r'^\s*\*\s+(.*?)$', r'<ul class="bullet-list"><li>\1</li></ul>', text, flags=re.MULTILINE)
    
    # Convert single newlines to spaces for regular paragraphs, preserving line breaks for our HTML elements
    text = re.sub(r'(?<!\n)(?<!>)\n(?!<)(?!\n)', ' ', text)
    
    # Fix any double spacing that might have been introduced
    text = re.sub(r' {2,}', ' ', text)
    
    return text 