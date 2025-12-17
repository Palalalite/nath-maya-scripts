import maya.cmds as cmd

# Search words go here
keywords = ["*_CTRL", "*:*_CTRL"]

keywords_ref = []

# Clear selection
cmd.select(cl = 1)

# Select items
for keyword in keywords:
    if cmd.objExists(keyword):
        print(keyword + ' ok')
        cmd.select(keyword, add = 1)