import os 
import pandas as pd
import datetime
import numpy as np

class DosDataFrame(pd.DataFrame):
    #def __init__(self, *args, **kwargs):
        #self.l=[]
        #l.extend(range(0,505))
        #self.read_csv(input_file, sep=',', header=None, names=l, comment='*', low_memory=False)
        #self.df.reset_index(drop=True)
        
    #    super(DosDataFrame,  self).__init__(*args, **kwargs)


    # @property
    # def _constructor(self):
    #     return MyDF

    def my_custom_method(self):
        print('This actually works!')


    def load_log(self, file):
        self.read_csv(file, sep=',', header=None, names=[], comment='*', low_memory=False)
        print(self)

    def get_metadata(self):
        print(self)
        help(self)
        metadata = self.loc[self[0]=='$DOS']
        print("METADATA")
        print(metadata)

        return(metadata)




class DetectorMetadata(dict):

    def get_sn(self):
        self.get('sn', None)

    def get_detector(self):
        self.get('detector', None)
    
    def get_version(self):
        self.get('version', None)


class DOS_parser:
    data = None
    detector = None 
    start_time = None
    spectra = None

    def __init__(self, log_file = None):
        if log_file:
            l=[]
            l.extend(range(0,1050))
            self.data = pd.read_csv(log_file, sep=',', header=None, names=l, comment='*', low_memory=False)
            print("Log loaded")
    
    def set_start_time(self, datetime_start: datetime.datetime):
        self.start_time = datetime_start
        self.data['time'] = np.concatenate(pd.to_timedelta(self.data[1], unit='s', errors='ignore'), self.start_time.timestamp())

    def get_spectra(self):
        self.spectra = self.data.loc[self.data[0]=='$HIST']
        return self.spectra

    
    def get_metadata(self):
        print(self.data)
        metadata = self.data.loc[self.data[0]=='$DOS'].iloc[0]
        

        self.detector = DetectorMetadata({
            "SW_ver": metadata[2],
            "SW_origin": metadata[5],
            "HW_ver": metadata[1],
            "HW_sn": metadata[6],
            "SW_hash": metadata[4],
            "channels": metadata[3]
        })


        return(metadata)

