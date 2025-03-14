import subprocess

def get_man_page(command_name):
    """
    Retrieve the man page for a given command.
    Falls back to alternative help sources if man page isn't available.
    """
    try:
        # First, try the standard man page
        man_page = subprocess.check_output(['man', command_name], text=True)
        return man_page
    except subprocess.CalledProcessError:
        # Man page not found, try alternative help sources
        
        # Try bash help (for shell builtins)
        try:
            help_text = subprocess.check_output(['bash', '-c', f'help {command_name} 2>/dev/null'], 
                                               text=True, stderr=subprocess.DEVNULL)
            if help_text.strip():
                return f"SHELL BUILTIN COMMAND:\n{help_text}"
        except subprocess.CalledProcessError:
            pass
        
        # Try --help flag
        try:
            help_text = subprocess.check_output([command_name, '--help'], 
                                              text=True, stderr=subprocess.DEVNULL)
            if help_text.strip():
                return f"COMMAND HELP OUTPUT:\n{help_text}"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try -h flag as last resort
        try:
            help_text = subprocess.check_output([command_name, '-h'], 
                                              text=True, stderr=subprocess.DEVNULL)
            if help_text.strip():
                return f"COMMAND HELP OUTPUT:\n{help_text}"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        # If all else fails, return a message indicating no documentation was found
        return f"NO_DOCUMENTATION: No manual page or help information found for '{command_name}'. Using general knowledge."

def parse_man_page(man_text):
    """Parse the retrieved man page text and return relevant information."""
    # This is a placeholder for parsing logic.
    # Implement parsing logic to extract summaries or specific sections as needed.
    return man_text.strip()  # For now, just return the raw text.