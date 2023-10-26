import xml.etree.ElementTree as ET
import csv

def get_names(root) -> list:
    # list of distinct attribute names (header) to pass to the csv.writer object
    attNames = []
    for row in root:
        for att in row:
            if att.tag not in attNames:
                attNames.append(att.tag)
    return attNames

def get_values(root) -> list:
    data = []
    for row in root:
        rowValues = []
        for att in row:
            rowValues.append(att.text)
        data.append(rowValues)
    return data


def xml_to_csv(input_xml, output_csv):  
    with open(output_csv, "w+", newline = "") as csvfile:
        # parsing the xml file
        tree = ET.parse(input_xml)
        root = tree.getroot()
        if len(root) == 0:
            raise Exception("There are no rows in the file")
        # extracting the attribute names
        attribute_names = get_names(root)
        values = get_values(root)
        # instanciating writer object on the new csv file
        csv_writer = csv.writer(csvfile, delimiter = ",")
        # writing the header
        csv_writer.writerow(attribute_names)
        # writing the values
        for line in values:
            csv_writer.writerow(line)
        print("The file has been parsed!")
        return