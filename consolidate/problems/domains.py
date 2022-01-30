import numpy as np

class RectangularDomain:

    def __init__(self, name,x0,x1,y0,y1, nodes, power):
        self.name = name
        self.dimensions =  [[x0,x1],[y0,y1]]
        self.nodes = nodes
        self.material = {}
        self.initial_condition = {}
        self.boundary_condition = {}
        self.power = power
        
        


    def test_grid_inter_nodes(self, mesh):
        if mesh[0] >= self.nodes[1][0]+1 and mesh[0] <= self.nodes[1][1]-1 and mesh[1] >= self.nodes[0][0]+1 and mesh[1]<= self.nodes[0][1]-1:
            return True
        else:
             return False

    def test_grid_all_nodes(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
             return False      
         
    def test_grid_left(self, mesh):
        if mesh[1] == 0 and mesh[0]!=0 and mesh[0]!=self.nodes[1][1]:
            return True
        else:
             return False         
         
    def test_grid_bottom(self, mesh):
        # if mesh[0] == 0 and mesh[1]!=0 and mesh[1]!=self.nodes[0][1]:
        if mesh[0] == 0:    
            return True
        else:
             return False   
         
    def test_grid_right(self, mesh):
        if mesh[1] == self.nodes[0][1] and mesh[0]!=0 and mesh[0]!=self.nodes[1][1]:
            return True
        else:
             return False 
         
    def test_grid_top(self, mesh):
        # if mesh[0] == self.nodes[1][1] and mesh[1]!=0 and mesh[1]!=self.nodes[0][1]:
        if mesh[0] == self.nodes[1][1]:    
            return True
        else:
             return False  

    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, nodes):
        self.px = nodes[0]
        self.py = nodes[1]

    def set_material(self,material):
        self.material.update(material)

    def set_bc(self, bc):
        self.boundary_condition.update(bc)

    def set_power(self, power):
        self.power.update(power)

    def set_initial_cond(self, init_cond):
        self.initial_condition.update(init_cond)


    def generate_mask(self, i, totalpy, totalpx, total_thickness):

        self.mask_nodes = {}
        self.bc_mask_nodes = {}



        inter_nodes = np.zeros((totalpy, totalpx))
        all_nodes = np.zeros((totalpy, totalpx))
        left_nodes = np.zeros((totalpy, totalpx))
        right_nodes = np.zeros((totalpy, totalpx))
        bottom_nodes = np.zeros((totalpy, totalpx))
        top_nodes = np.zeros((totalpy, totalpx))

        for x_i in range (0,np.shape(inter_nodes)[0]):
            for y_i in range (0,np.shape(inter_nodes)[1]):
                if self.test_grid_inter_nodes( (x_i, y_i)):
                    inter_nodes[x_i][y_i] = 1
                if self.test_grid_all_nodes( (x_i, y_i)):
                    all_nodes[x_i][y_i] = 1
                if self.test_grid_left( (x_i, y_i)):
                    left_nodes[x_i][y_i] = 1    
                if self.test_grid_right( (x_i, y_i)):
                    right_nodes[x_i][y_i] = 1 
                if self.test_grid_bottom( (x_i, y_i)):
                    bottom_nodes[x_i][y_i] = 1    
                if self.test_grid_top( (x_i, y_i)):
                    top_nodes[x_i][y_i] = 1 
                    
        self.mask_nodes["All"] = all_nodes.copy()
        self.mask_nodes["Inner"] = inter_nodes.copy()
        self.bc_mask_nodes["Left"] = left_nodes
        self.bc_mask_nodes["Right"] = right_nodes
        self.bc_mask_nodes["Bottom"] = bottom_nodes
        self.bc_mask_nodes["Top"] = top_nodes