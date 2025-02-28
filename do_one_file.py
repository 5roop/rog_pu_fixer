try:
    inEXB = snakemake.input.inEXB
    outEXB = snakemake.output.outEXB
    new_PU_textgrid = snakemake.input.textgrid
except NameError:
    inEXB = "ROG/ROG-Art/EXB/Rog-Art-J-Gvecg-P500014.exb.xml"
    outEXB = "newEXBs/Rog-Art-J-Gvecg-P500014.exb.xml"
    new_PU_textgrid = "new_PUs/Rog-Art-J-Gvecg-P500014.TextGrid"

from lxml import etree
from pathlib import Path
import textgrid

doc = etree.fromstring(Path(inEXB).read_bytes())
tg = textgrid.TextGrid.fromFile(new_PU_textgrid)
putier = tg[14]
pus = []
for pu in putier:
    t = pu.mark.replace("\x7f", "").strip()
    t = t.encode("utf-8")
    while " " in t:
        t = t.replace(" ", "")
    if t.strip() == "":
        continue
    parts = t.split("Artur-")
    parts = ["Artur-" + i for i in parts if i != ""]
    pus.append(parts)

tiers = doc.findall(".//tier")
speakers = set([i.attrib["speaker"] for i in tiers])
for speaker in speakers:
    # Find PU tier
    put = doc.find(f".//tier[@display-name='{speaker} [prosodicUnits]']")
    assert put is not None, "Can't find prosodic unit tier for speaker " + speaker
    # Clear existing PUs
    for event in put.findall(".//event"):
        event.getparent().remove(event)

    tt = doc.find(f".//tier[@display-name='{speaker} [traceability]']")
    assert tt is not None, "Can't find traceability tier for speaker " + speaker

    for pu in pus:
        start_token = pu[0]
        end_token = pu[-1]
        try:
            start = [
                i for i in tt.findall(".//event") if i.text.strip() == start_token
            ][0].attrib.get("start")
            end = [i for i in tt.findall(".//event") if i.text.strip() == end_token][
                0
            ].attrib.get("end")
            newpu = etree.Element("event", attrib={"start": start, "end": end})
            newpu.text = "PU." + start_token.split(".")[-1]
            put.append(newpu)
        except IndexError:
            continue

# Validation: we need as many PUs in EXB as in TG
pu_events = [i.text for i in doc.findall(".//event") if i.text.startswith("PU.")]
if len(pu_events) < len(pus):
    for pu in pus:
        query = "PU." + pu[0].split(".")[-1]
        if not query in pu_events:
            print("Invalid PU: ")
            print("".join(pu).__repr__())
            print("\n\n")

    print("Will not save the file with missing PUs. Fix manually")
elif len(pu_events) > len(pus):
    print("There are more EXB PUs than in textgrid!")
else:
    etree.indent(doc, space="\t")
    doc.getroottree().write(
        outEXB,
        pretty_print=True,
        encoding="utf8",
        xml_declaration='<?xml version="1.0" encoding="UTF-8"?>',
    )
    Path(outEXB).write_text(
        Path(outEXB)
        .read_text()
        .replace(
            "<?xml version='1.0' encoding='UTF8'?>",
            '<?xml version="1.0" encoding="UTF-8"?>',
        )
    )

2 + 2
