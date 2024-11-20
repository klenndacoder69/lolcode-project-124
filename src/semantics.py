'''
Group: Detective Cunan1
Authors:
Klenn Jakek Borja
Shawn Clyde Diares
Kervin Ralph Samson

Section: ST1L
'''

def get_semantics(file_content):
    variable_storage = {}
    for line in file_content:
            # Ignore HAI and KTHXBYE
        if line.strip() == "HAI":
            continue
        if line.strip() == "KTHXBYE":
            break
            # Start the semantics
        if line.strip() == "WAZZUP":
            while(line.strip() != "BUHBYE"):
                
    pass
