file_path='data/111_141_obj/111_141_obj_pymeshlab_textdim_4096_texres_4096.obj'
with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('v '):
        # Split the line by whitespace
        parts = line.split()
        # Remove the RGB values (indices 4 to 6) from the parts list
        parts = parts[:4] + parts[7:]
        # Join the modified parts back into a line
        new_line = ' '.join(parts) + '\n'
        # Append the new line to the list of new lines
        new_lines.append(new_line)
    else:
        # For all other lines, just append them to the list of new lines
        new_lines.append(line)

# Write the modified lines back to the file
with open(file_path, 'w') as f:
    f.writelines(new_lines)