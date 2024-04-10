import os
from llama_index.core.tools import FunctionTool

note_file = os.path.join("data", "notes.txt")

def clear_note():
    # if notes path exists delete notes
    if os.path.exists(note_file):
        # just create a new one?
        open(note_file, "w")

    return "notes clear"

def save_note(note):
    # if file does not exist, create it
    if not os.path.exists(note_file):
        open(note_file, "w")

    # otherwise add note to existing file
    with open(note_file, "a") as f:
        f.writelines([note + "\n"])

    return "note saved"

clear_note_engine = FunctionTool.from_defaults(
    fn=clear_note,
    name="note_clear",
    description="this tool can clear the existing note file for the user"
)

save_note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="this tool can save a text based note to a file for the user"
)