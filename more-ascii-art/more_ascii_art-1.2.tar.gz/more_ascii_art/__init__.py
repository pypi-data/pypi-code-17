# Importing assets
import cat
import chicken
import mouse

# Error handling variable
err = print("Something went wrong. Report a bug at https://github.com/PenetratingShot/Python-ASCII-Art/issues")

# Help section
def help():
    print("     Welcome to more_ascii_art help!      ")
    print("Usage: ")
    print("       1. Build the library with >>> pip install -e .")
    print("       2. Use the python shell to >>> import more-ascii-art")
    print("       3. Type in print and then the build name and then the function you wish to execute")
    print("            Like this: >>> print more-ascii-art.help()")
    print("Commands: ")
    print("       1. help() - Displays this help message")
    print("       2. selection() - Displays all ASCII selections and prompts you for which one you want")

# User selection and processing    
def selection():
    print("Please note that selections are case sensitive...")
    print("Here are the selections you can choose from (for now): ")
    print("1. cat ")
    print("2. chicken ")
    print("3. mouse ")
    user_input = input("Please type in your selection: ")
    
    if (user_input == "cat"):
        return cat()
    else:
        print (err)
        
    if (user_input == "chicken"):
        return chicken()
    else:
        print (err)
        
    if (user_input == "mouse"):
        return mouse()
    else:
        print (err)
