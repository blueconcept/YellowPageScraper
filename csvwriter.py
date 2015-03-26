class CSVWriter():
    """
    Custom Writer for CSV because the Python built-in one kept giving me extra spaces
    """
    
    
    def __init__(self, csv_file, fieldnames, fillnone="NA"):
        """
        INPUT: file, String, String
        OUTPUT: None
        Iinitializes CSVWriter
        """
        self.csv_file = csv_file
        self.fieldnames = fieldnames
        self.fillnone = fillnone
    
    def write_header(self):
        """
        INPUT: None
        OUTPUT: None
        Writes the headers for the csv file
        """
        for i,name in enumerate(self.fieldnames):
            self.csv_file.write(name)
            if i < len(self.fieldnames)-1:
                self.csv_file.write(",")
        self.csv_file.write("\n")

    def write_row(self, item_dict, sep=','):
        """
        INPUT: Dictionary
        OUTPUT: None
        Writes the row based on the item_dict with the order from the fieldnames list
        """
        for i,item in enumerate(self.fieldnames):
            if item_dict[item] is None:
                self.csv_file.write(self.fillnone)
            else:
                self.csv_file.write(unicode(item_dict[item]))
            if i < len(self.fieldnames)-1:
                self.csv_file.write(sep)
        self.csv_file.write("\n")