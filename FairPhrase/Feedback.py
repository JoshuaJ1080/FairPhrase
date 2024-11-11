import csv
import os

def append_feedback_to_csv(name, email, message, filename='data/Feedback.csv'):
    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.isfile(filename)

    # Read existing lines to ensure no empty lines at the end
    if file_exists:
        with open(filename, mode='r', newline='') as csvfile:
            lines = csvfile.readlines()
            # Remove any empty lines at the end
            while lines and lines[-1].strip() == '':
                lines.pop()

        # If the file is empty, we need to write the header
        if not lines:
            file_exists = False

    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['name', 'email', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()

        writer.writerow({'name': name, 'email': email, 'message': message})