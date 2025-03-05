import subprocess

def get_man_page(command_name):
    """Retrieve the man page for a given command."""
    try:
        man_page = subprocess.check_output(['man', command_name], text=True)
        return man_page
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error retrieving man page for '{command_name}': {e}")

def parse_man_page(man_text):
    """Parse the retrieved man page text and return relevant information."""
    # This is a placeholder for parsing logic.
    # Implement parsing logic to extract summaries or specific sections as needed.
    return man_text.strip()  # For now, just return the raw text.