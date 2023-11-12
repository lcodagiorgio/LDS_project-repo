import xml.etree.ElementTree as ET
import csv

def get_names(root):
    """Function to extract the names of the elements (attributes in xml element format) from a xml file.

    Args:
        root (ElementTree obj): root object of the xml tree

    Returns:
        list: list of the element names (attribute names in xml element format)
    """
    # list of distinct attribute names (header) to pass to the csv.writer object
    attNames = []
    for row in root:
        for att in row:
            if att.tag not in attNames:
                attNames.append(att.tag)
    return attNames

def get_values(root):
    """Function to extract the values of the elements (attributes in xml element format) from a xml file.

    Args:
        root (ElementTree obj): root object of the xml tree

    Returns:
        list: list of the element's values (attribute values in xml element format)
    """
    data = []
    for row in root:
        rowValues = []
        for att in row:
            rowValues.append(att.text)
        data.append(rowValues)
    return data


def xml_to_csv(input_xml, output_csv):
    """Function to convert an input file in xml element format to a output file in csv format.

    Args:
        input_xml (FileDescriptorOrPath): Input file in xml element format to convert.
        output_csv (FileDescriptorOrPath): New output file in csv format.
    """
    with open(output_csv, "w+", newline = "") as csvfile:
        # parsing the xml file
        tree = ET.parse(input_xml)
        root = tree.getroot()
        # checking if the xml tree has any rows
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