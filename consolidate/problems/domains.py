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
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1]-1 and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
             return False
         
    def test_grid_nodes(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
             return False
         
    def test_grid_nodes_inner(self, mesh):
        if mesh[0] >= self.nodes[1][0] +1 and mesh[0] <= self.nodes[1][1] -1 and mesh[1] >= self.nodes[0][0] +1 and mesh[1]<= self.nodes[0][1] -1:
            return True
        else:
             return False


    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, p_x0, p_x1, p_y0, p_y1):
        self.px = [p_x0, p_x1]
        self.py = [p_y0, p_y1]

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
        self.mask_inter_nodes = {}
        self.mask_nodes_out ={}


        mnodes = np.zeros((totalpy, totalpx))
        minter_nodes = np.zeros((totalpy -1, totalpx -1))
        mnodes_out = np.zeros((totalpy+2, totalpx+2))

        mnodes_all = mnodes.copy()
        mnodes_top = mnodes.copy()
        mnodes_bottom = mnodes.copy()
        mnodes_left = mnodes.copy()
        mnodes_right = mnodes.copy()
        mnodes_inner = mnodes.copy()
        mnodes_left2 = mnodes.copy()
        mnodes_right2 = mnodes.copy()

        minter_nodes_all = minter_nodes.copy()


        for x_i in range (0,np.shape(minter_nodes)[0]):
            for y_i in range (0,np.shape(minter_nodes)[1]):
                if self.test_grid_inter_nodes( (x_i, y_i)):
                    minter_nodes_all[x_i][y_i] = 1
        self.mask_inter_nodes["All"] = minter_nodes_all.copy()


        for x_i in range (0,np.shape(mnodes)[0]):
            for y_i in range (0,np.shape(mnodes)[1]):
                if self.test_grid_nodes( (x_i, y_i)):
                    mnodes_all[x_i][y_i] = 1
                    mnodes_bottom[self.nodes[1][0]][y_i] = 1
                    mnodes_top[self.nodes[1][1]][y_i] = 1
                    mnodes_right[x_i][-1] = 1
                    mnodes_left[x_i][0] = 1
                if self.test_grid_nodes_inner((x_i, y_i)):
                    mnodes_inner[x_i][y_i] = 1
                    mnodes_right2[x_i][-1] = 1
                    mnodes_left2[x_i][0] = 1

        self.mask_nodes["All"] = mnodes_all.copy()
        self.mask_nodes["Right Edge"] = mnodes_right2.copy()
        self.mask_nodes["Left Edge"] = mnodes_left2.copy()
        self.mask_nodes["Inner"] = mnodes_inner.copy()

        self.mask_nodes_out["Left Edge"] = mnodes_out.copy()
        self.mask_nodes_out["Left Edge"][1:-1, :-2] = mnodes_left.copy()
        self.mask_nodes_out["Right Edge"] = mnodes_out.copy()
        self.mask_nodes_out["Right Edge"] [1:-1, 2:] = mnodes_right.copy()

        if self.nodes[1][0] == 0:
            self.mask_nodes["Bottom Edge"] = mnodes_bottom.copy()
            self.mask_nodes_out["Bottom Edge"] = mnodes_out.copy()
            self.mask_nodes_out["Bottom Edge"] [:-2, 1:-1] = mnodes_bottom.copy()
            self.mask_nodes_out["Left Edge"][self.nodes[1][1]+1] = 0
            self.mask_nodes_out["Right Edge"][self.nodes[1][1]+1] = 0

        if self.nodes[1][1] == totalpy-1:
            self.mask_nodes["Top Edge"] = mnodes_top.copy()
            self.mask_nodes_out["Top Edge"] = mnodes_out.copy()
            self.mask_nodes_out["Top Edge"] [2:, 1:-1] = mnodes_top.copy()
            self.mask_nodes_out["Left Edge"][self.nodes[1][0]+1] = 0
            self.mask_nodes_out["Right Edge"][self.nodes[1][0]+1] = 0

        if self.nodes[1][0] != 0 and self.nodes [1][1] != totalpy-1:
            self.mask_nodes_out["Left Edge"][self.nodes[1][0]+1] = 0
            self.mask_nodes_out["Left Edge"][self.nodes[1][1]+1] = 0
            self.mask_nodes_out["Right Edge"][self.nodes[1][0]+1] = 0
            self.mask_nodes_out["Right Edge"][self.nodes[1][1]+1] = 0

