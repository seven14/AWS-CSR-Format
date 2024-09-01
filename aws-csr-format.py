import sys
import re

def process_file(input_file, output_file, header):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        inside_block = False
        # Buffer for data lines
        buffer = []

        for line in infile:
            # Check if the line is a header
            if header in line.strip():
              # Check if we are collecting data lines yet
              if inside_block == False:
                # Remove NEW in the header, if present
                line = re.sub("NEW ", "", line)
                # Write the header to output file
                outfile.write(line)
                # Set the flag for collecting data
                inside_block = True
                continue
                
              # Next occurance of the header should be the footer, last line
              if inside_block == True:
                # Preserve the footer to append later
                footer = line
                # Concatenate all the lines of data in the buffer
                concatenated_text = ''.join(buffer)
                # Chop the concatenated text into 64 character chunks and write them to the output file
                for chunk in [concatenated_text[i:i+64] for i in range(0, len(concatenated_text), 64)]:
                  outfile.write(chunk + '\n')
                # Write the footer to output file
                outfile.write(footer)

            # If inside the block between header and footer
            if inside_block:
                buffer.append(line.strip())  # Add the line to the buffer without leading/trailing whitespace

if __name__ == "__main__":
    # Grab the input filename for convertion to output filename
    input_file = sys.argv[1]
    temp = input_file.split('.')
    output_file = (temp[0] + "-new2.txt")
    #output_file = (output_file + "-new.txt")
    
    # Define the header regex
    header = "-----"

    process_file(input_file, output_file, header)
