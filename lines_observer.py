import supervision as sv 
import pandas as pd

class LineObserver:
    
    class_dict = {2:'car',3:'motorcycle',5:'bus',7:'truck'}
    

    def __init__(self):
        self.lines = dict()
        self.target_objects = dict()
        self.id = 0

        self.info_table = pd.DataFrame() 

    def add_line(self, line:sv.LineZone):
        self.id += 1
        self.lines[self.id] = line
    
    def upd_directions(self,obj_id):
        if len(self.target_objects[obj_id]['lines'])==2:
            
            line_id1, line_id2 = self.target_objects[obj_id]['lines'][0], self.target_objects[obj_id]['lines'][1]
            direction = f'{line_id1}->{line_id2}'

            if direction not in self.info_table.columns:
                self.info_table[direction] = {'car':0, 'truck':0, 'bus':0, 'motorcycle':0}
            
            class_id = self.target_objects[obj_id]['class_id']
            class_name = LineObserver.class_dict[class_id]
            self.info_table[direction][class_name] += 1

        elif len(self.target_objects[obj_id]['lines'])==1:
            ##для дебага
            print("--",self.target_objects[obj_id]['lines'], obj_id)
            

    def update(self, detections:sv.Detections):
        for lz_id, lz in self.lines.items():
            crossed_in, crossed_out = lz.trigger(detections)

            for obj_id, class_id in zip(detections[crossed_in].tracker_id, detections[crossed_in].class_id):
                if obj_id not in self.target_objects.keys():
                    self.target_objects[obj_id] = {'lines':[lz_id], 'class_id':class_id}
                else:
                    self.target_objects[obj_id]['lines'].append(lz_id)
                self.upd_directions(obj_id)
                
            
            for obj_id, class_id in zip(detections[crossed_out].tracker_id, detections[crossed_out].class_id):
                if obj_id not in self.target_objects.keys():
                    self.target_objects[obj_id] = {'lines':[lz_id], 'class_id':class_id}
                else:
                    self.target_objects[obj_id]['lines'].append(lz_id)
                self.upd_directions(obj_id)

          

            #print(detections[crossed_in].tracker_id)
            #print(detections[crossed_out].tracker_id)
    def info(self):
        print(self.info_table)
    
    
            
           