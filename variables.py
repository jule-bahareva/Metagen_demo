#!/usr/bin/env python 

class InputVariable:
    
    def __init__(self):
        self.fragments_filter = "5000" 
        self.metadata_filename = "MSU.csv"
        self.search_db = "Human Pathogens"
    
    def get_filter(self):
        return self.fragments_filter
    
    def get_metadata(self):
        return self.metadata_filename
    
    def get_search_db(self):
        return self.search_db
    
    