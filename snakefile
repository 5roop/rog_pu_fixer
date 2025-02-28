from pathlib import Path

newPUs = list(Path("new_PUs").glob("*"))
expected_files =  [f"newEXBs/{i.with_suffix(".exb.xml").name}" for i in newPUs]
print(expected_files)

rule do_one:
    input:
        inEXB = "ROG/ROG-Art/EXB/{file}.exb.xml",
        textgrid = "new_PUs/{file}.TextGrid",
    output:
        outEXB = "newEXBs/{file}.exb.xml"
    script: "do_one_file.py"

rule gather:
    default_target:True,
    input: expected_files
